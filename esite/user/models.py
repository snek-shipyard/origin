import django.contrib.auth.validators
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


class SNEKUser(AbstractUser, ClusterableModel):
    username = models.CharField(
        "username",
        null=True,
        blank=False,
        error_messages={"unique": "A user with that username already exists."},
        help_text="Required. 36 characters or fewer. Letters, digits and @/./+/-/_ only.",
        max_length=36,
        unique=True,
        validators=[django.contrib.auth.validators.UnicodeUsernameValidator()],
    )

    panels = [
        MultiFieldPanel(
            [
                FieldPanel("username"),
                FieldPanel("first_name"),
                FieldPanel("last_name"),
                FieldPanel("email"),
            ],
            "Details",
        ),
        MultiFieldPanel(
            [
                FieldPanel("is_active"),
            ],
            "Settings",
        ),
    ]

    graphql_fields = [
        GraphQLString("username"),
        GraphQLString("first_name"),
        GraphQLString("last_name"),
        GraphQLString("email"),
        GraphQLBoolean("is_active"),
    ]

    # Custom save function
    def save(self, *args, **kwargs):
        super(SNEKUser, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.username}"


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
