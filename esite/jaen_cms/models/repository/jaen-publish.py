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

# Create your publish related models here.
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

    def full_clean(self, *args, **kwargs):
        # first call the built-in cleanups (including default slug generation)
        super(JaenPublishFormPage, self).full_clean(*args, **kwargs)

        # now make your additional modifications
        # if not self.slug.startswith("jaen-"):
        #     self.slug = f"jaen-{self.slug}"

    def save(self, *args, **kwargs):
        if self.pk is None:
            self.form_fields.add(
                JaenPublishFormField(
                    label="user", field_type="hidden", required=False,
                ),
                JaenPublishFormField(
                    label="git_user", field_type="hidden", required=False,
                ),
                JaenPublishFormField(
                    label="git_remote", field_type="singleline", required=True,
                ),
                JaenPublishFormField(
                    label="jaendata_url", field_type="singleline", required=True,
                ),
            )

        # after call the built-in cleanups (including default form fields)
        super(JaenPublishFormPage, self).save(*args, **kwargs)

    def get_submission_class(self):
        return JaenPublishFormSubmission

    # Publish to git remote
    def publish(
        self, user, git_remote, jaendata_url
    ):
        # Get GitHub token from jaen account 
        git_token = user.jaen_account.git_token
        encryption_token = user.jaen_account.encryption_token

        url = f"https://api.github.com/repos/{git_remote}/dispatches"

        headers = requests.structures.CaseInsensitiveDict()
        headers["Accept"] = "application/vnd.github.everest-preview+json"
        headers["Content-Type"] = "application/x-www-form-urlencoded"
        headers["Authorization"] = f"token {git_token}"
        
        jaen_payload = '{"jaendata_url":' + jaendata_url +', "encryption_token":' + encryption_token + ' }'

        data = '{"event_type":"update-jaen-data", "client_payload":' + jaen_payload + ' }'
        test_data = '{"event_type":"update-jaen-data", "client_payload": { "dataLayer": { "origin": { "pages": { "home": { "fields": { "body": { "blocks": { "0": { "content": "Original Heading Content", "typeName": "heading" }, "1": { "content": "<p>Original Subheading Content</p>", "typeName": "subheading" } } } }, "typeName": "HomePage" } } } }, "index": { "checksum": "d716d3da6493f8e1ad5c9dc480ea595b0402355815f25c5353c6e37413516f32d", "rootPageSlug": "home", "pages": { "home": { "slug": "home", "title": "My HomePage Updated4", "typeName": "HomePage", "childSlugs": ["blog-1"] } } } }}'


        resp = requests.post(url, headers=headers, data=data.encode('utf-8'))

        resp.raise_for_status()

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

        jaen_account = self.publish(
            user=user,
            git_remote=form.cleaned_data["git_remote"],
            jaendata_url=form.cleaned_data["jaendata_url"],
        )

        form.cleaned_data["user"] = user.username
        form.cleaned_data["git_user"] = user.jaen_account.git_user

        self.get_submission_class().objects.create(
            form_data=json.dumps(form.cleaned_data, cls=DjangoJSONEncoder),
            page=self,
            jaen_account=jaen_account,
        )

        if self.to_address:
            self.send_mail(form)

class JaenPublishFormSubmission(AbstractFormSubmission):
    jaen_account = ParentalKey("jaen_cms.JaenAccount", on_delete=models.CASCADE, related_name="publish_submissions")