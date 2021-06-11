from django.db.models import Q
from django.contrib.admin import SimpleListFilter
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)
from .models import Member


class HasTelegramnameFilter(SimpleListFilter):
    """
    This filter is being used in wagtail admin panel in member model.
    """

    title = "has telegram username"
    parameter_name = "telegram_username__has"

    def lookups(self, request, model_admin):
        return (
            ("1", "Yes"),
            ("0", "No"),
        )

    def queryset(self, request, queryset):
        if not self.value():
            return queryset
        if self.value() == "1":
            return queryset.filter().exclude(
                Q(telegram_username__isnull=True) | Q(telegram_username__exact="")
            )
        elif self.value() == "0":
            return queryset.filter(
                Q(telegram_username__isnull=True) | Q(telegram_username__exact="")
            )


class MemberAdmin(ModelAdmin):
    model = Member
    menu_label = "Member"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the user overview
    list_display = ("date_joined", "matrikelnummer", "email", "telegram_username")
    list_filter = ("is_member", HasTelegramnameFilter)
    search_fields = ("date_joined", "matrikelnummer", "email", "telegram_username")

    # export_filename = 'people_spreadsheet'
    # list_export = ("date_joined", "matrikelnummer", "email", "telegram_username"),


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
