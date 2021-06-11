from django.contrib.auth.validators import UnicodeUsernameValidator
from bifrost.api.models import (
    GraphQLBoolean,
    GraphQLInt,
    GraphqlDatetime,
    GraphQLString,
)
from django.contrib.auth.models import AbstractUser
from django.db import models
from modelcluster.models import ClusterableModel
from wagtail.admin.edit_handlers import FieldPanel, MultiFieldPanel
from django.contrib.auth.models import AbstractUser, BaseUserManager
from modelcluster.fields import ParentalKey
from modelcluster.models import ClusterableModel

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission
from django.contrib.auth.models import Group

User = get_user_model()


class Member(ClusterableModel):
    user = ParentalKey(
        "user.SNEKUser", blank=True, on_delete=models.CASCADE, related_name="member"
    )

    matrikelnummer = models.CharField(
        "matrikelnummer",
        blank=True,
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters and digits only.",
        max_length=36,
        validators=[UnicodeUsernameValidator],
    )

    telegram_username = models.CharField(
        "telegram username",
        blank=True,
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 150 characters or fewer. Letters and digits only.",
        max_length=36,
        validators=[UnicodeUsernameValidator],
    )

    telegram_user_id = models.IntegerField(
        "user id",
        error_messages={"unique": "A user with that user_id already exists."},
        help_text="Required. 64 Bit Integer. Digits only.",
    )

    registration_token = models.CharField(
        "registration token",
        null=True,
        blank=True,
        error_messages={"unique": "A user with that matrikelnummer already exists."},
        help_text="Required. 36 digits long. Digits only.",
        max_length=36,
    )

    is_member = models.BooleanField(
        "is member",
        default=False,
        help_text="Designates whether this member should be treated as active. "
        + "Unselect this instead of deleting accounts.",
    )

    def is_club_member(self, info, **kwargs):
        return self.user.groups.filter(name="club-member").exists()

    def is_club_supervisor(self, info, **kwargs):
        return self.user.groups.filter(name="club-supervisor").exists()

    def date_joined(self, **kwargs):
        return self.user.date_joined

    def email(self, **kwargs):
        return self.user.email

    # Panels/fields to fill in the Add enterprise form
    panels = [
        FieldPanel("user"),
        MultiFieldPanel(
            [
                FieldPanel("matrikelnummer"),
                FieldPanel("telegram_user_id"),
                FieldPanel("telegram_username"),
                FieldPanel("registration_token"),
            ],
            "Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("is_member"),
            ],
            "Settings",
        ),
    ]

    graphql_fields = [
        GraphQLBoolean("is_club_member"),
        GraphQLBoolean("is_club_supervisor"),
        GraphQLInt("telegram_user_id"),
        GraphQLString("telegram_username"),
        GraphQLString("registration token"),
        GraphQLBoolean("is_member"),
    ]

    def __str__(self):
        return f"{self.matrikelnummer}"


# Model manager to use in Proxy model
class InactiveProxyManager(models.Manager):
    def get_queryset(self):
        # filter the objects for non-customer datasets based on the User model
        return super(InactiveProxyManager, self).get_queryset().filter(is_member=False)


# Model manager to use in Proxy model
# class MemberProxyManager(BaseUserManager):
#     def get_queryset(self):
#         # filter the objects for non-customer datasets based on the User model
#         return super(MemberProxyManager, self).get_queryset().filter(is_active=True).filter(groups__name='club-member')

# class Inactive(Member):
#     # call the model manager on user objects
#     objects = InactiveProxyManager()

#     # Panels/fields to fill in the Add enterprise form
#     panels = [
#         FieldPanel("user"),
#         MultiFieldPanel(
#             [
#                 FieldPanel("matrikelnummer"),
#                 FieldPanel("telegram_user_id"),
#                 FieldPanel("telegram_username"),
#                 FieldPanel("registration_token"),
#             ],
#             "Details",
#         ),
#         MultiFieldPanel(
#             [
#                 FieldPanel("is_member"),
#             ],
#             "Settings",
#         ),
#     ]

#     graphql_fields = [
#         GraphQLBoolean("is_club_member"),
#         GraphQLBoolean("is_club_supervisor"),
#         GraphQLInt("telegram_user_id"),
#         GraphQLString("telegram_username"),
#         GraphQLString("registration token"),
#         GraphQLBoolean("is_member"),
#     ]


#     # Custom save function
#     def save(self, *args, **kwargs):
#         super(Member, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"{self.matrikelnummer}"

#     class Meta:
#         proxy = True


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 Nico Schett
