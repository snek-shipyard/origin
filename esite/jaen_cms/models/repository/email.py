import json
import uuid
import requests

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
from graphql import GraphQLError
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

# Create your email related models here.
class JaenEmailFormField(AbstractFormField):
    page = ParentalKey(
        "JaenEmailFormPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )

class JaenEmailFormPage(AbstractEmailForm):
    # template = "patterns/pages/forms/form_page.html"
    # Only allow creating HomePages at the root level
    #parent_page_types = []
    #subpage_types = []

    class Meta:
        verbose_name = "Jaen Email Form Page"

    # When creating a new Form page in Wagtail
    email_head = models.CharField(null=True, blank=False, max_length=255)
    email_privacy_text = RichTextField(null=True, blank=False,)
    email_info_text = RichTextField(null=True, blank=False,)
    thank_you_text = RichTextField(null=True, blank=False,)

    graphql_fields = [
        GraphQLString("email_head"),
        GraphQLString("email_privacy_text"),
        GraphQLString("email_info_text"),
        GraphQLString("thank_you_text"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("email_head", classname="full title"),
                FieldPanel("email_privacy_text", classname="full"),
                FieldPanel("email_info_text", classname="full"),
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

    def full_clean(self, *args, **kwargs):
        # first call the built-in cleanups (including default slug generation)
        super(JaenEmailFormPage, self).full_clean(*args, **kwargs)

        # now make your additional modifications
        # if not self.slug.startswith("jaen-"):
        #     self.slug = f"jaen-{self.slug}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.form_fields.add(
                JaenEmailFormField(
                    label="user", field_type="hidden", required=False,
                ),
                JaenEmailFormField(
                    label="git_user", field_type="hidden", required=False,
                ),
                JaenEmailFormField(
                    label="git_remote", field_type="singleline", required=True,
                ),
                JaenEmailFormField(
                    label="form_first_name", field_type="singleline", required=True,
                ),
                JaenEmailFormField(
                    label="form_last_name", field_type="singleline", required=True,
                ),
            )

        # after call the built-in cleanups (including default form fields)
        super(JaenEmailFormPage, self).save(*args, **kwargs)

    def get_submission_class(self):
        return JaenEmailFormSubmission

    # Email to git remote
    def dispatch(
        self, user, git_remote, form_data
    ):
        # Get GitHub token from jaen account
        git_token = user.jaen_account.git_token

        # message = html_message

        url = f"https://api.github.com/repos/{git_remote}/dispatches"

        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/vnd.github.everest-preview+json"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = f"token {git_token}"

        data = '{"event_type":"send_mail", "client_payload":' + form_data + ' }'

        resp = requests.post(url, headers=headers, data=data.encode('utf-8'))

        #resp.raise_for_status()

        return user.jaen_account

    # Called when a user registers
    def send_mail(self, form):
        pass
        # addresses = [x.strip() for x in self.to_address.split(",")]

        # emailheader = "New publish via SNEK Website"

        # content = []
        # for field in form:
        #     value = field.value()
        #     if isinstance(value, list):
        #         value = ", ".join(value)
        #     content.append("{}: {}".format(field.label, value))
        # content = "\n".join(content)

        # content += "\n\nMade with ❤ by a tiny SNEK"

        # # emailfooter = '<style>@keyframes pulse { 10% { color: red; } }</style><p>Made with <span style="width: 20px; height: 1em; color:#dd0000; animation: pulse 1s infinite;">&#x2764;</span> by <a style="color: lightgrey" href="https://www.aichner-christian.com" target="_blank">Werbeagentur Christian Aichner</a></p>'

        # # html_message = f"{emailheader}\n\n{content}\n\n{emailfooter}"

        # send_mail(
        #     self.subject, f"{emailheader}\n\n{content}", addresses, self.from_address
        # )

    def process_form_submission(self, form, user, *args, **kwargs):

        form.cleaned_data["user"] = user.username
        form.cleaned_data["git_user"] = user.jaen_account.git_user

        jaen_account = self.dispatch(
            user=user,
            git_remote=form.cleaned_data["git_remote"],
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            jaen_account=jaen_account,
            page=self,
        )

        if self.to_address:
            self.send_mail(form)

class JaenEmailFormSubmission(AbstractFormSubmission):
    jaen_account = ParentalKey("jaen_cms.JaenAccount", on_delete=models.CASCADE, related_name="email_submissions")