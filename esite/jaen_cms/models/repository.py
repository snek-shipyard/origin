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

# Create your publish related models here.

class JaenRepository(ClusterableModel):

    jaen_account = ParentalKey(
        "jaen_cms.JaenAccount", blank=False, on_delete=models.CASCADE, related_name="jaen_repository"
    )

    git_remote = models.URLField(
        "git remote",
        null=True,
        blank=False,
        unique=True,
        max_length = 255
    )

    # Panels/fields to fill in the Add enterprise form
    panels = [
        MultiFieldPanel(
            [
                FieldPanel("jaen_account"),
                FieldPanel("git_remote_type"),
                FieldPanel("git_remote"),
                FieldPanel("git_user"),
                FieldPanel("git_token"),
            ],
            "Details",
        ),
    ]

    graphql_fields = [
        GraphQLString("jaen_account"),
        GraphQLString("git_remote_type"),
        GraphQLString("git_remote"),
        GraphQLString("git_user"),
        GraphQLString("git_token"),
    ]

    def __str__(self):
        return f"{self.git_remote}"



class JaenPublishFormField(AbstractFormField):
    page = ParentalKey(
        "JaenPublishFormPage",
        on_delete=models.CASCADE,
        related_name="form_fields",
    )


class JaenPublishFormPage(AbstractEmailForm):
    # template = "patterns/pages/forms/form_page.html"
    # Only allow creating HomePages at the root level
    #parent_page_types = []
    #subpage_types = []

    class Meta:
        verbose_name = "Jaen Publish Form Page"

    # When creating a new Form page in Wagtail
    publish_head = models.CharField(null=True, blank=False, max_length=255)
    publish_privacy_text = RichTextField(null=True, blank=False,)
    publish_info_text = RichTextField(null=True, blank=False,)
    thank_you_text = RichTextField(null=True, blank=False,)

    graphql_fields = [
        GraphQLString("publish_head"),
        GraphQLString("publish_privacy_text"),
        GraphQLString("publish_info_text"),
        GraphQLString("thank_you_text"),
    ]

    content_panels = [
        MultiFieldPanel(
            [
                FieldPanel("publish_head", classname="full title"),
                FieldPanel("publish_privacy_text", classname="full"),
                FieldPanel("publish_info_text", classname="full"),
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
                JaenPublishFormField(
                    label="git_user", field_type="singleline", required=True,
                ),
                JaenPublishFormField(
                    label="git_token", field_type="singleline", required=True,
                ),
                JaenPublishFormField(
                    label="git_remote", field_type="singleline", required=True,
                ),
                JaenPublishFormField(
                    label="jaen_data", field_type="singleline", required=True,
                ),
            )

        # after call the built-in cleanups (including default form fields)
        super(JaenPublishFormPage, self).save(*args, **kwargs)

    def get_submission_class(self):
        return JaenPublishFormSubmission

    # Publish to git remote
    def publish(
        self, user, git_user, git_token, git_remote, jaen_data
    ):
        # Add user data
        # user = get_user_model()(username=username, is_active=False)

        # user.set_password(password)

        url = f"https://api.github.com/repos/{git_remote}/dispatches"

        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/vnd.github.everest-preview+json"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = git_token

        test_data = '{"event_type":"update-jaen-data", "client_payload": { "dataLayer": { "quiz": { "sport": { "q1": { "question": "Which one is correct team name in NBA?", "options": [ "New York Bulls", "Los Angeles Kings", "Golden State Warriros", "Huston Rocket" ], "answer": "Huston Rocket" } }, "maths": { "q1": { "question": "5 + 7 = ?", "options": [ "10", "11", "12", "13" ], "answer": "12" }, "q2": { "question": "12 - 8 = ?", "options": [ "1", "2", "3", "4" ], "answer": "4" } } } }}'


        resp = requests.post(url, headers=headers, data=jaen_data)

        print(resp.status_code)


        return user

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

        user = self.publish(
            user=user,
            git_user=form.cleaned_data["git_user"],
            git_token=form.cleaned_data["git_token"],
            git_remote=form.cleaned_data["git_remote"],
            jaen_data=form.cleaned_data["jaen_data"],
        )

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            user=user,
        )

        if self.to_address:
            self.send_mail(form)

class JaenPublishFormSubmission(AbstractFormSubmission):
    user = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)