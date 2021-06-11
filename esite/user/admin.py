from django.contrib.auth import get_user_model
from wagtail.contrib.modeladmin.options import (
    ModelAdmin,
    ModelAdminGroup,
    modeladmin_register,
)


class UserAdmin(ModelAdmin):
    model = get_user_model()
    menu_label = "User"
    menu_icon = "user"
    menu_order = 290
    add_to_settings_menu = False
    exclude_from_explorer = False

    # Listed in the user overview
    list_display = ("date_joined", "username", "email")
    search_fields = ("date_joined", "username", "email")


class UserManagementAdmin(ModelAdminGroup):
    menu_label = "User Management"
    menu_icon = "group"
    menu_order = 110
    add_to_settings_menu = False
    exclude_from_explorer = False
    items = (UserAdmin,)


# modeladmin_register(UserManagementAdmin)

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at

