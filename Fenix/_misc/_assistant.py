# Ultroid - UserBot
# Copyright (C) 2021-2022 TeamUltroid
#
# This file is a part of < https://github.com/TeamUltroid/Ultroid/ >
# PLease read the GNU Affero General Public License in
# <https://github.com/TeamUltroid/Fenix/blob/main/LICENSE>.

import inspect
import re

from telethon import Button
from telethon.events import CallbackQuery, InlineQuery, NewMessage
from telethon.tl.types import InputWebDocument

from .. import LOGS, asst, ultroid_bot
from ..functions.admins import admin_check
from . import append_or_update, owner_and_sudos

OWNER = ultroid_bot.full_name

MSG = f"""
ᥴᥣiᥴκ ᴛɦᥱ δᥙᴛᴛ᧐ᥒ δᥱᥣ᧐ᥕ ᴛ᧐ ᥴ᧐ᥒᴛᥲᥴᴛ !
"""

IN_BTTS = [
    [
        Button.url("✗ ᴅᴇᴠ ✗", url="https://t.me/DarkPentesterX"),
    ]
]


# decorator for assistant


def asst_cmd(pattern=None, load=None, owner=False, **kwargs):
    """Decorator for assistant's command"""
    name = inspect.stack()[1].filename.split("/")[-1].replace(".py", "")
    kwargs["forwards"] = False

    def ult(func):
        if pattern:
            kwargs["pattern"] = re.compile("^/" + pattern)
        if owner:
            kwargs["from_users"] = owner_and_sudos
        asst.add_event_handler(func, NewMessage(**kwargs))
        if load is not None:
            append_or_update(load, func, name, kwargs)

    return ult


def callback(data=None, from_users=[], admins=False, owner=False, **kwargs):
    """Assistant's callback decorator"""
    if "me" in from_users:
        from_users.remove("me")
        from_users.append(ultroid_bot.uid)

    def ultr(func):
        async def wrapper(event):
            if admins and not await admin_check(event):
                return
            if from_users and event.sender_id not in from_users:
                return await event.answer("Not for You!", alert=True)
            if owner and event.sender_id not in owner_and_sudos():
                return await event.answer(f"This is {OWNER}'s bot!!")
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, CallbackQuery(data=data, **kwargs))

    return ultr


def in_pattern(pattern=None, owner=False, **kwargs):
    """Assistant's inline decorator."""

    def don(func):
        async def wrapper(event):
            if owner and event.sender_id not in owner_and_sudos():
                res = [
                    await event.builder.article(
                        title="𝒉𝒆𝒂𝒓𝒕𝒍𝒆𝒔𝒔",
                        url="https://t.me/DarkPentesterX",
                        description="• 𝒖𝒏 𝒂𝒎𝒂𝒏𝒕 𝒔𝒂𝒏𝒔 𝒄𝒐𝒆𝒖𝒓 | 𝒆𝒏𝒔 𝒑𝒂𝒓𝒊𝒔 🎭",
                        text=MSG,
                        thumb=InputWebDocument(
                            "https://telegra.ph/file/2def97874a6005606d5a4.jpg",
                            0,
                            "image/jpeg",
                            [],
                        ),
                        buttons=IN_BTTS,
                    )
                ]
                return await event.answer(
                    res,
                    switch_pm=f"👨🏻‍💻 𝒂𝒔𝒔𝒊𝒔𝒕𝒂𝒏𝒕 𝒐𝒇 {OWNER}",
                    switch_pm_param="start",
                )
            try:
                await func(event)
            except Exception as er:
                LOGS.exception(er)

        asst.add_event_handler(wrapper, InlineQuery(pattern=pattern, **kwargs))

    return don
