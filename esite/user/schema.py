import graphene
from bifrost.registry import registry
from django.contrib.auth import get_user_model
from graphql_jwt.decorators import login_required


class Query(graphene.ObjectType):
    me = graphene.Field(
        registry.models[get_user_model()], token=graphene.String(required=False)
    )

    @login_required
    def resolve_me(self, info, **_kwargs):
        user = info.context.user

        return user


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
