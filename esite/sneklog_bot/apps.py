# -*- coding: utf-8 -*-
import os
import io
import logging
import json
import hashlib
import uuid
import time
import datetime
import asyncio
import threading

from django.conf import settings
from django.apps import AppConfig
from telethon import TelegramClient, events, functions

#from .snek_management import SnekManagement


class SnekBotConfig(AppConfig):
    name = "esite.sneklog_bot"

    def ready(self: object) -> None:
        """Start the client."""
        print("snek bot started...")
        sneklog_bot_thread = threading.Thread(
            name="sneklog_bot-main-thread", target=SnekBot.main
        )
        sneklog_bot_thread.daemon = False  # -> dies after main thread is closed
        sneklog_bot_thread.start()


class SnekBot:
    def main() -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        client = TelegramClient(
            "client", settings.TELEGRAM_API_ID, settings.TELEGRAM_API_HASH, loop=loop
        ).start(bot_token=settings.TELEGRAM_BOT_TOKEN)

        @client.on(events.NewMessage(pattern="/start"))
        @client.on(events.NewMessage(pattern="/help"))
        async def start(event: object) -> None:
            """Send a message when the command /start is issued."""
            await event.respond(
                """**Willkommen bei TUWien.snek**\n\nUm unseren Studierendengruppen beitreten zu können, musst du dich vorab mit deiner Matrikelnummer identifizieren.
                \nDazu musst du mir deine Matrikelnummer (z.B.: `11700000`) senden. Anschließend bekommst du einen Aktivierungslink per Mail an deine Studierendenmailadresse gesendet.
                \n\nBei Problemen melde dich bitte bei @vileslide"""
            )
            raise events.StopPropagation

        @client.on(events.NewMessage(pattern="/register"))
        async def register(event: object) -> None:
            await client.forward_messages(
                677357231, f"de neie registrierte gruppn event.chat_id"
            )

        @client.on(events.NewMessage)
        async def registration_handler(event):
            # Log all communication with the snek bot
            await client.forward_messages(-1001464884999, event.message)

            try:
                if event.message.text.isnumeric():
                    if SnekManagement.register_user(
                        matrikelnummer=event.message.text,
                        telegram_user=event.message.sender,
                    ):
                        await event.reply(
                            f"**Vielen Dank!**\n\nEin Aktivierungslink wurde an deine Studierendenmailadresse gesendet."
                            + "Sobald der Link bestätigt wurde, kannst du allen Gruppen uneingeschränkt beitreten. Bitte halte dich an die Regeln (www.tuwien.snek/rules)."
                        )
                    else:
                        raise Exception(
                            "Die angegebene Matrikelnummer wird bereits verwendet oder ist keine gültige Matrikelnummer. (Wenn dieser Fehler trotz richtiger Matrikelnummer auftritt, melde dich bitte bei @vileslide und wir schalten dich frei)"
                        )
                else:
                    raise Exception(
                        "Deine Eingabe konnte leider nicht erkannt werden. Um dich zu registrieren, sende mir bitte deine Matrikelnummer."
                    )

            except Exception as e:
                await event.reply(
                    # f"Shit happens! Something has gone wrong.\n\n**Error:** {e}"
                    f"{e}"
                )
                # Log all communication with the snek bot
                await client.forward_messages(-1001175848537, event.message)

        @client.on(events.ChatAction)
        async def join_handler(event: object) -> None:
            # Check every new user
            if event.user_joined:
                res: bool = await SnekManagement.check_new_member(event.user)
                await event.action_message.delete()
                # await event.reply('Welcome to the group!')

        with client:
            client.run_until_disconnected()


# SPDX-License-Identifier: (EUPL-1.2)
# Copyright © 2021 snek.at
