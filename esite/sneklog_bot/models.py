from django.db import models
from bifrost.decorators import login_required
from modelcluster.fields import ParentalKey
from wagtail.admin.edit_handlers import (
    FieldPanel,
    InlinePanel,
    StreamFieldPanel,
    MultiFieldPanel,
)
from wagtail.contrib.settings.models import BaseSetting, register_setting
from wagtail.core.fields import StreamField
from wagtail.core.models import Orderable, Page
from wagtail.documents.edit_handlers import DocumentChooserPanel
from wagtail.images.edit_handlers import ImageChooserPanel
from wagtail.snippets.edit_handlers import SnippetChooserPanel
from wagtail.snippets.models import register_snippet
from wagtail_headless_preview.models import HeadlessPreviewMixin
from wagtailmedia.edit_handlers import MediaChooserPanel
from bifrost.api.models import (
    GraphQLCollection,
    GraphQLDocument,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLInt,
    GraphQLMedia,
    GraphQLPage,
    GraphQLSnippet,
    GraphQLStreamfield,
    GraphQLString,
)
from bifrost.publisher.actions import register_publisher
from bifrost.publisher.options import PublisherOptions


# @register_publisher(
#     read_singular=True,
#     read_singular_permission=login_required,
# )
class TelegramChat(models.Model):
    chat_id = models.IntegerField(null=True, blank=True)

    graphql_fields = [
        GraphQLString(
            "chat_id",
            publisher_options=PublisherOptions(read=True, update=True, create=True),
            required=True,
        ),
    ]

    class Meta:
        abstract = True


# @register_publisher(
#     read_singular=True,
#     read_singular_permission=login_required,
# )
class TelegramChatGroup(TelegramChat):
    name = models.CharField(null=True, blank=True, max_length=39)

    graphql_fields = TelegramChat.graphql_fields + [
        GraphQLString(
            "name",
            publisher_options=PublisherOptions(read=True, update=True, create=True),
            required=True,
        ),
    ]

    class Meta:
        abstract = True


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
