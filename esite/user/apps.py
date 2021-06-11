import hashlib

from django.apps import AppConfig
from django.db.models.signals import post_migrate


def create_group(name, permissions=[]):
    from django.contrib.auth.models import Group

    group, created = Group.objects.get_or_create(name=name)
    [group.permissions.add(permission) for permission in permissions]


def create_user(username, password, groups=[], **kwargs):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Group

    User = get_user_model()

    user = User.objects.create(username=username, **kwargs)
    user.set_password(password)
    user.save()

    [user.groups.add(Group.objects.get(name=group)) for group in groups]


def define_club_groups(sender, **kwargs):
    from django.contrib.auth import get_user_model
    from django.contrib.auth.models import Permission
    from django.contrib.contenttypes.models import ContentType

    User = get_user_model()

    user_ct = ContentType.objects.get_for_model(User)
    supervisor_permissions = [
        # User permissions
        Permission.objects.get_or_create(
            codename="can_add_members",
            name="Can add club members",
            content_type=user_ct,
        )[0],
        Permission.objects.get_or_create(
            codename="can_delete_members",
            name="Can delete club members",
            content_type=user_ct,
        )[0],
        Permission.objects.get_or_create(
            codename="can_update_members",
            name="Can update club members",
            content_type=user_ct,
        )[0],
        Permission.objects.get_or_create(
            codename="can_view_members",
            name="Can view club members",
            content_type=user_ct,
        )[0],
    ]
    member_permissions = [
        # Project permissions
        Permission.objects.get_or_create(
            codename="can_view_members",
            name="Can view club members",
            content_type=user_ct,
        )[0],
    ]

    create_group("snek-supervisor", supervisor_permissions)
    create_group("snek-member", member_permissions)


def define_users(sender, **kwargs):
    from django.contrib.auth import get_user_model

    User = get_user_model()

    if not User.objects.exists():
        create_user(username="admin", password="ciscocisco", is_superuser=True)
        create_user(username="cisco", password="ciscocisco")


class UsersConfig(AppConfig):
    name = "esite.user"

    def ready(self):
        post_migrate.connect(define_club_groups, sender=self)
        post_migrate.connect(define_users, sender=self)

        # if you have other signals e.g. post_save, you can include it
        # like the one below.
        # from .signals import (create_site_profile)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
