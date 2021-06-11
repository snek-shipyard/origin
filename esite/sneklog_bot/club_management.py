from django.conf import settings
from django.template.loader import render_to_string
import uuid

from asgiref.sync import sync_to_async

from .db_management import DBIO


class SnekManagement:
    # fields
    name: str = ""
    botid: str = ""
    groupids: list = []
    admins: list = []
    blacklist: list = []
    from_address: str = "noreply@neurons.at"
    debug_address: str = "backup@neurons.at"

    # ctor
    # props

    # meths
    @classmethod
    def send_mail(self, addresses: str, registration_link: str) -> None:
        from wagtail.admin.mail import send_mail

        emailheader: str = "Snek - NoTuSpam"

        content = "registration_link: {registration_link}"

        html_message: str = render_to_string(
            "registration/registration_mail_template.html",
            {"registration_link": registration_link},
        )

        send_mail(
            "Registrierung TUWien Snek - NoTuSpam",
            f"{emailheader}\n\n{content}",
            addresses,
            "noreply@neurons.at",
            html_message=html_message,
        )

    @classmethod
    def check_matrikelnummer(cls, matrikelnummer: str) -> bool:

        # Check if black listed
        if matrikelnummer in []:
            return False
        # Check if 6, 7 or 8 digits and for validity

        # Pre 2017 numbers
        if matrikelnummer < 10000000:
            # Pre 2010 numbers
            if matrikelnummer < 100000:
                return False

            # Invalid numbers due to change in 2017
            if matrikelnummer > 1679999:
                return False

            return True

        if matrikelnummer > 64000000:
            return False

        return True

    @classmethod
    def register_user(
        cls, matrikelnummer: str, telegram_user: object, register_res=False
    ) -> bool:
        # Mail versenden -> format string -> uni spezifisch e[matrikelnummer]@student.tuwien.ac.at
        # Datenbank -> existiert userid mit matrikelnummer? existiert matrikelnummer und existiert userid?
        # Authentication URL erstellen
        # in Mail gepackt und verschickt

        matrikelnummer_int = int(matrikelnummer)

        if cls.check_matrikelnummer(matrikelnummer_int):
            if not DBIO.check_blacklist(matrikelnummer=matrikelnummer):
                if not DBIO.check_user_id(telegram_user.id):

                    # Generate correct mailaddress
                    address = f"{matrikelnummer}@student.tuwien.ac.at"

                    # Add e to email address to match correct format
                    address = "e" + address

                    addresses: tuple = (address,)

                    registration_token: str = str(uuid.uuid4())

                    if DBIO.register(
                        matrikelnummer=matrikelnummer,
                        user_id=telegram_user.id,
                        username=telegram_user.username,
                        first_name=telegram_user.first_name,
                        last_name=telegram_user.first_name,
                        email=address,
                        registration_token=registration_token,
                    ):

                        registration_link: str = (
                            f"{settings.BASE_URL}/{registration_token}"
                        )

                        cls.send_mail(addresses, registration_link)

                        register_res = True

        return register_res

    @staticmethod
    def activate_member(registration_token: str, activate_res: bool = False) -> bool:
        if DBIO.activate_member(registration_token):
            activate_res = True

        return activate_res

    @staticmethod
    @sync_to_async
    def check_new_member(telegram_user: object) -> bool:
        if DBIO.check_user_id(telegram_user.id):
            pass

        return False
