from wagtail.core import hooks

from .views import UserChooserViewSet


@hooks.register("register_admin_viewset")
def register_user_chooser_viewset():
    return UserChooserViewSet("user_chooser", url_prefix="user-chooser")


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
