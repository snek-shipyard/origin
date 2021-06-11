import json
import hashlib
from django.core.serializers.json import DjangoJSONEncoder
from asgiref.sync import sync_to_async
from django.contrib.auth import get_user_model


class DBIO:
    # ctor
    # props

    # meths
    @staticmethod
    def register(
        matrikelnummer: str,
        user_id: int,
        username: str,
        first_name: str,
        last_name: str,
        email: str,
        registration_token: str,
        add_res: bool = False,
    ) -> bool:
        from django.contrib.auth.models import Group
        from esite.members.models import Member

        try:
            user = get_user_model().objects.create(
                username=f"snek-{matrikelnummer}",
                first_name=first_name,
                last_name=last_name,
                email=email,
                is_active=False,
            )

            user.set_password(hashlib.sha256(str.encode(matrikelnummer)).hexdigest())
            # user.groups.add(Group.objects.get(name="ohrwurm-supervisor"))
            user.groups.add(Group.objects.get(name="snek-member"))

            user.save()

            member = Member.objects.create(
                user=user,
                matrikelnummer=matrikelnummer,
                telegram_user_id=user_id,
                telegram_username=username,
                registration_token=registration_token,
            )

            member.save()

            add_res = True

        except Exception as e:
            print(e)

        return add_res

    @staticmethod
    def check_blacklist(matrikelnummer: str, check_res: bool = True) -> bool:
        from .models import SnekSettings

        blacklist = json.loads(SnekSettings.for_site(1).blacklist)["blacklist"]

        if not matrikelnummer in blacklist:
            check_res = False

        return check_res

    @staticmethod
    def check_user(check_res: bool = False) -> bool:
        return check_res

    @staticmethod
    def check_matrikelnummer(check_res: bool = False) -> bool:
        return check_res

    @staticmethod
    def check_user_id(user_id, check_res: bool = False) -> bool:
        from esite.members.models import Member

        if Member.objects.filter(telegram_user_id=user_id).exists():
            check_res = True

        return check_res

    @staticmethod
    def activate_member(registration_token: str, activate_res: bool = False) -> bool:
        from esite.members.models import Member

        wannabemember = Member.objects.filter(
            registration_token=registration_token
        ).first()
        if wannabemember:

            wannabemember.is_member = True
            wannabemember.registration_token = ""
            wannabemember.save()

            activate_res = True
            print("hell yeah")

        return activate_res

    @staticmethod
    def disable_user(disable_res: bool = False) -> bool:
        return disable_res
