import hashlib

from django.apps import AppConfig
from django.db.models.signals import post_migrate
from django.apps import AppConfig


# This defines the name of the app.
class MembersConfig(AppConfig):
    name = "members"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2019-2020 Simon Prast
