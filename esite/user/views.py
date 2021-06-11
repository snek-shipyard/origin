from django import forms
from django.contrib.auth import get_user_model
from django.utils.translation import ugettext_lazy as _
from generic_chooser.views import ModelChooserViewSet


class UserForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ["username", "first_name", "last_name", "email", "is_staff"]


class UserChooserViewSet(ModelChooserViewSet):
    icon = "pilcrow"
    model = get_user_model()
    page_title = _("Choose a User")
    per_page = 10
    form_class = UserForm


# Create your views here.

# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
