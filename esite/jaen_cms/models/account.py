import json
import uuid

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.core.serializers.json import DjangoJSONEncoder
from django.db import models

from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import (
    FieldPanel,
    FieldRowPanel,
    InlinePanel,
    MultiFieldPanel,
    ObjectList,
    StreamFieldPanel,
    TabbedInterface,
)
from wagtail.admin.mail import send_mail
from wagtail.contrib.forms.models import (
    AbstractEmailForm,
    AbstractForm,
    AbstractFormField,
    AbstractFormSubmission,
)
from wagtail.core import blocks
from wagtail.core.fields import RichTextField, StreamField
from wagtail.core.models import Page
from wagtail.snippets.edit_handlers import SnippetChooserPanel

from bifrost.publisher.actions import register_publisher
from bifrost.publisher.options import PublisherOptions
from bifrost.api.models import (
    GraphQLBoolean,
    GraphQLCollection,
    GraphQLDocument,
    GraphQLEmbed,
    GraphQLField,
    GraphQLFloat,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLInt,
    GraphQLSnippet,
    GraphQLStreamfield,
    GraphQLString,
)

# Create your registration related models here.

class JaenAccount(ClusterableModel):
    user = models.OneToOneField(
        "user.SNEKUser", blank=True, on_delete=models.CASCADE, related_name="jaen_account"
    )

    git_user = models.CharField(
        "git username",
        blank=True,
        help_text="Required. 255 characters or fewer. Letters and digits only.",
        max_length=255,
    )

    git_token = models.CharField(
        "git token",
        blank=True,
        help_text="Required. 255 characters or fewer. Letters and digits only.",
        max_length=255,
    )
    
    def is_snek_member(self, info, **kwargs):
        return self.user.groups.filter(name="snek-member").exists()

    def is_snek_supervisor(self, info, **kwargs):
        return self.user.groups.filter(name="snek-supervisor").exists()

    def date_joined(self, **kwargs):
        return self.user.date_joined

    def email(self, **kwargs):
        return self.user.email


    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        FieldPanel("git_user"),
        FieldPanel("git_token"),
    ]

    graphql_fields = [
        GraphQLForeignKey(
            "user",
            get_user_model(),
            publisher_options=PublisherOptions(read=True, create=True),
            required=True,
        ),
        GraphQLString("git_user"),
    ]

    def __str__(self):
        return f"{self.user.username}"


class JaenRegistrationFormField(AbstractFormField):
    page = ParentalKey(
        "JaenRegistrationFormPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class JaenRegistrationFormPage(AbstractEmailForm):
    # template = "patterns/pages/forms/form_page.html"
    # Only allow creating HomePages at the root level
    parent_page_types = []
    subpage_types = []

    class Meta:
        verbose_name = "Jaen Registration Form Page"

    # When creating a new Form page in Wagtail
    registration_head = models.CharField(null=True, blank=False, max_length=255)
    registration_privacy_text = RichTextField(null=True, blank=False,)
    registration_info_text = RichTextField(null=True, blank=False,)
    thank_you_text = RichTextField(null=True, blank=False,)

    graphql_fields = [
        GraphQLString("registration_head"),
        GraphQLString("registration_privacy_text"),
        GraphQLString("registration_info_text"),
        GraphQLString("thank_you_text"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("registration_head", classname="full title"),
                FieldPanel("registration_privacy_text", classname="full"),
                FieldPanel("registration_info_text", classname="full"),
                FieldPanel("thank_you_text", classname="full"),
            ],
            heading="content",
        ),
        MultiFieldPanel(
            [
                FieldRowPanel(
                    [
                        FieldPanel("from_address", classname="col6"),
                        FieldPanel("to_address", classname="col6"),
                    ]
                ),
                FieldPanel("subject"),
            ],
            heading="Email Settings",
        ),
        MultiFieldPanel(
            [InlinePanel("form_fields", label="Form fields")], heading="data",
        ),
    ]

    edit_handler = TabbedInterface(
        [
            ObjectList(
                AbstractEmailForm.content_panels + content_panels, heading="Content",
            ),
            ObjectList(
                AbstractEmailForm.promote_panels + AbstractEmailForm.settings_panels,
                heading="Settings",
                classname="settings",
            ),
        ]
    )

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.form_fields.add(
                PersonRegistrationFormField(
                    label="username", field_type="singleline", required=True
                ),
                PersonRegistrationFormField(
                    label="first_name", field_type="singleline", required=True,
                ),
                PersonRegistrationFormField(
                    label="last_name", field_type="singleline", required=True,
                ),
                PersonRegistrationFormField(
                    label="email", field_type="email", required=True,
                ),
                PersonRegistrationFormField(
                    label="password", field_type="singleline", required=True,
                ),
            )

        # after call the built-in cleanups (including default form fields)
        super(JaenRegistrationFormPage, self).save(*args, **kwargs)

    def get_submission_class(self):
        return JaenRegistrationFormSubmission

    # Create a new user
    def create_user(
        self, username, first_name, last_name, email, password
    ):
        # Add user data
        user = get_user_model()(username=username, is_active=False)

        user.set_password(password)
        

        # Add jaen data
        user.jaen_account = JaenAccount.objects.create(user=user)
        
        user.save()

        return user

    # Called when a user registers
    def send_mail(self, form):
        addresses = [x.strip() for x in self.to_address.split(",")]

        emailheader = "New registration via SNEK Website"

        content = []
        for field in form:
            value = field.value()
            if isinstance(value, list):
                value = ", ".join(value)
            content.append("{}: {}".format(field.label, value))
        content = "\n".join(content)

        content += "\n\nMade with ❤ by a tiny SNEK"

        # emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'

        # html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"

        send_mail(
            self.subject, f"{emailheader}\n\n{content}", addresses, self.from_address
        )

    def process_form_submission(self, form):

        user = self.create_user(
            username=form.cleaned_data["username"],
            first_name=form.cleaned_data["first_name"],
            last_name=form.cleaned_data["last_name"],
            email=form.cleaned_data["email"],
            password=form.cleaned_data["password"],
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)


class JaenRegistrationFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
