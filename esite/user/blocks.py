from django.utils.functional import cached_property
from django.utils.html import format_html
from wagtail.core.blocks import ChooserBlock


class UserChooserBlock(ChooserBlock):
    @cached_property
    def target_model(self):
        from django.contrib.auth import get_user_model

        return get_user_model()

    @cached_property
    def widget(self):
        from .widgets import UserChooser

        return UserChooser

    def render_basic(self, value, context=None):
        if value:
            return format_html('<a href="{0}">{1}</a>', value.username, value.email)
        else:
            return ""

    class Meta:
        icon = "user"
        name = "user"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
