# Create your models here.

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at

from django.db import models
from wagtail.contrib.settings.models import BaseSetting, register_setting
from bifrost.api.models import (
    GraphQLCollection,
    GraphQLDocument,
    GraphQLForeignKey,
    GraphQLImage,
    GraphQLMedia,
    GraphQLPage,
    GraphQLSnippet,
    GraphQLStreamfield,
    GraphQLString,
)
from wagtail.admin.edit_handlers import (
    FieldPanel,
    MultiFieldPanel,
    ObjectList,
    PageChooserPanel,
    StreamFieldPanel,
    TabbedInterface,
)
from bifrost.publisher.actions import register_publisher

# Create your models here.


@register_setting
@register_publisher(
    read_singular=True,
    delete=False,
)
class SnekSettings(BaseSetting):
    class Meta:
        verbose_name = "Snek Config"

    snek_name = models.CharField(
        max_length=255,
        blank=True,
        help_text="Your Twitter username without the @, e.g. katyperry",
    )
    bot_id = models.CharField(
        max_length=255, blank=True, help_text="Your Facebook app ID."
    )
    group_ids = models.CharField(
        max_length=255,
        blank=True,
        help_text="Default sharing text to use if social text has not been set on a page.",
    )
    admins = models.CharField(
        max_length=255,
        blank=True,
        help_text="Site name, used by Open Graph.",
    )
    from_address = models.CharField(
        max_length=255,
        blank=True,
        help_text="Site name, used by Open Graph.",
    )
    debug_addres = models.CharField(
        max_length=255,
        blank=True,
        help_text="Site name, used by Open Graph.",
    )
    blacklist = models.TextField(
        blank=False,
        default="{}",
        help_text="Site name, used by Open Graph.",
    )

    graphql_fields = [
        GraphQLString("snek_name"),
        GraphQLString("bot_id"),
        GraphQLString("group_ids"),
        GraphQLString("admins"),
        GraphQLString("from_address"),
        GraphQLString("debug_addres"),
        GraphQLString("blacklist"),
    ]

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("snek_name"),
                FieldPanel("bot_id"),
                FieldPanel("group_ids"),
                FieldPanel("admins"),
                FieldPanel("from_address"),
                FieldPanel("debug_addres"),
            ],
            "Settings",
        ),
        MultiFieldPanel(
            [
                FieldPanel("blacklist"),
            ],
            "Blacklist",
        ),
    ]


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
