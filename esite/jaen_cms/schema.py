import hashlib

import graphene
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.models import Group
from graphene_django import DjangoObjectType
from graphql import GraphQLError
from graphql_jwt.decorators import (
    login_required,
    permission_required,
    staff_member_required,
    superuser_required,
)

from esite.jaen_cms.models import JaenAccount

class JaenAccountType(DjangoObjectType):
    class Meta:
        model = JaenAccount
        exclude_fields = ["git_token"]

    is_snek_supervisor = graphene.Boolean()

    def resolve_is_snek_supervisor(instance, info, **kwargs):
        return instance.is_snek_supervisor(info)

class Query(graphene.ObjectType):
    my_jaen_account = graphene.Field(
        JaenAccountType, token=graphene.String(required=False)
    )

    @login_required
    def resolve_my_jaen_account(self, info, **_kwargs):
        jaen_account = info.context.user.jaen_account

        return jaen_account