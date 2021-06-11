import datetime
from django.http import HttpResponse
from .club_management import ClubManagement

# Create your views here.


def activate_club_member(request, token):

    html = f"<html><body>It is now {ClubManagement.activate_member(registration_token=token)}.</body></html>"

    return HttpResponse(html)


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
