from bifrost.api.models import GraphQLString
from django.db import models
from wagtail.documents.models import AbstractDocument
from wagtail.documents.models import Document as WagtailDocument


class SNEKDocument(AbstractDocument):
    description = models.TextField(max_length=255, blank=True, null=True)
    admin_form_fields = WagtailDocument.admin_form_fields + ("description",)

    graphql_fields = (GraphQLString("description"),)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
