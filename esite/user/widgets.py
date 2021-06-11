from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from generic_chooser.widgets import AdminChooser


class UserChooser(AdminChooser):
    choose_one_text = _("Choose a User")
    model = get_user_model()
    choose_modal_url_name = "user_chooser:choose"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
