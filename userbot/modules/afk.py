# Copyright (C) 2019 The Raphielscape Company LLC.
#
# Licensed under the Raphielscape Public License, Version 1.c (the "License");
# you may not use this file except in compliance with the License.
#
""" Userbot module which contains afk-related commands """

from datetime import datetime
import time
from random import choice, randint
from asyncio import sleep

from telethon.events import StopPropagation

from userbot import (AFKREASON, COUNT_MSG, CMD_HELP, ISAFK, BOTLOG,
                     BOTLOG_CHATID, USERS, PM_AUTO_BAN)
from userbot.events import register

# ========================= CONSTANTS ============================
AFKSTR = [
    "Sorry bray, ane gak lagi mantengin hp :v",
    "Sedang tidak membuka telegram :)",
    "Hola! Kalo ente liat pesan ini, berarti ane lagi gak buka telegram",
    "Kalo lagi gabut biasanya beberapa menit lagi ane bales. Kalo enggak...,\ntunggu lebih lama. awikwok :v",
    "I'm not here right now, so I'm probably somewhere else.",
    "Roses are red,\nViolets are blue,\nLeave me a message,\nAnd I'll get back to you.",
    "Terkadang menunggu adalah hal yang tepat\nMakanya tunggu ampe ane buka pesan lu napa >:(.",
    "I'll be right back,\nbut if I'm not right back,\nI'll be back later.",
    "I'll tell u something bruh,\nI'm not here. awikwok :V",
    "Hei hei, welcome to my away message, gimana rasanya menunggu sesuatu yang tak pasti?",
    "I'm away over 7 seas and 7 countries,\n7 waters and 7 continents,\n7 mountains and 7 hills,\n7 plains and 7 mounds,\n7 pools and 7 lakes,\n7 springs and 7 meadows,\n7 cities and 7 neighborhoods,\n7 blocks and 7 houses...\n\nWhere not even your messages can reach me!",
    "Ane lagi AFK, tapi kalo ente coba teriak di hp ente, mungkin ane bakal denger suara ente :V",
    "Yah telat dah ente :v\nAne lagi AFK sekarang",
    "Orang sabar pantadnya lebar\nMakanya tunggu ane baca pesan lu.\nAwikwok :v",
    "Silahkan tinggalkan pesan. Kalo gak penting, ane baca pas kebetulan buka telegram.\nKalo penting, ya sama ae ane baca pas kebetulan buka telegram.\n awikwok :V",
    "I am not here so stop writing to me,\nor else you will find yourself with a screen full of your own messages.",
    "Ane lagi AFK sekarang. Kalo mau lansung dibales pesannya, bisa send pulsa 50K ke 0895358957539",
    "Hang on!\nI'm on my way",
    "Lagi , silahkan tinggalin nomer, alamat rumah, semua akun sosmed ente. Entar ane stalk kalo gabut",
    "Sorry bray, ane lagi AFK.\nSilahkan chat ama bot ane kalo lagi gabut.\nEntar ane baca pesan ente pas buka telegram.",
    "Tjie berharap ane balas yak? :v\n Tapi maap beribu maap ane lagi AFK sekarang",
    "Hidup ntu singkat bre. Ada banyak hal yang bisa dilakuin\nDan ane lagi ngelakuin salah satu dari hal ntu",
    "Terkadang kita terlena dengan dunia dan melupakan tujuan untuk hidup. Dan sekarang ane belum baca pesan ente karena lagi tafakkur hidup buat apaan yak tujuannya? :"",
]

global USER_AFK  # pylint:disable=E0602
global afk_time  # pylint:disable=E0602
global afk_start
global afk_end
USER_AFK = {}
afk_time = None
afk_start = {}

# =================================================================
@register(outgoing=True, pattern="^.afk(?: |$)(.*)", disable_errors=True)
async def set_afk(afk_e):
    """ For .afk command, allows you to inform people that you are afk when they message you """
    message = afk_e.text
    string = afk_e.pattern_match.group(1)
    global ISAFK
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    global reason
    USER_AFK = {}
    afk_time = None
    afk_end = {}
    start_1 = datetime.now()
    afk_start = start_1.replace(microsecond=0)
    if string:
        AFKREASON = string
        await afk_e.edit(f"__Going AFK!__\
        \nReason: `{string}`")
    else:
        await afk_e.edit("__Going AFK!__")
    if BOTLOG:
        await afk_e.client.send_message(BOTLOG_CHATID, "#AFK\nAne lagi AFK!")
    ISAFK = True
    afk_time = datetime.now()  # pylint:disable=E0602
    raise StopPropagation


@register(outgoing=True)
async def type_afk_is_not_true(notafk):
    """ This sets your status as not afk automatically when you write something while being afk """
    global ISAFK
    global COUNT_MSG
    global USERS
    global AFKREASON
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alive = datetime.now()
    afk_end = back_alive.replace(microsecond=0)
    if ISAFK:
        ISAFK = False
        msg = await notafk.respond("Ane dah gak AFK lagi.")
        time.sleep(3)
        await msg.delete()
        if BOTLOG:
            await notafk.client.send_message(
                BOTLOG_CHATID,
                "You've recieved " + str(COUNT_MSG) + " messages from " +
                str(len(USERS)) + " chats while you were away",
            )
            for i in USERS:
                name = await notafk.client.get_entity(i)
                name0 = str(name.first_name)
                await notafk.client.send_message(
                    BOTLOG_CHATID,
                    "[" + name0 + "](tg://user?id=" + str(i) + ")" +
                    " sent you " + "`" + str(USERS[i]) + " messages`",
                )
        COUNT_MSG = 0
        USERS = {}
        AFKREASON = None


@register(incoming=True, disable_edited=True)
async def mention_afk(mention):
    """ This function takes care of notifying the people who mention you that you are AFK."""
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if mention.message.mentioned and not (await mention.get_sender()).bot:
        if ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Yesterday"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h:{int(minutes)}m` ago"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m:{int(seconds)}s` ago"
            else:
                afk_since = f"`{int(seconds)}s` ago"
            if mention.sender_id not in USERS:
                if AFKREASON:
                    await mention.reply(f"{str(choice(AFKSTR))}"
    f"\n\nI'm AFK right now since {afk_since}"
    f"\nReason: `{AFKREASON}`")
                else:
                    await mention.reply(str(choice(AFKSTR)))
                USERS.update({mention.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif mention.sender_id in USERS:
                    if AFKREASON:
                        await mention.reply(f"{str(choice(AFKSTR))}"
    f"\n\nI'm AFK right now since {afk_since}"
    f"\nReason: `{AFKREASON}`")
                    else:
                        await mention.reply(str(choice(AFKSTR)))
                    USERS[mention.sender_id] = USERS[mention.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


@register(incoming=True, disable_errors=True)
async def afk_on_pm(sender):
    """ Function which informs people that you are AFK in PM """
    global ISAFK
    global USERS
    global COUNT_MSG
    global COUNT_MSG
    global USERS
    global ISAFK
    global USER_AFK  # pylint:disable=E0602
    global afk_time  # pylint:disable=E0602
    global afk_start
    global afk_end
    back_alivee = datetime.now()
    afk_end = back_alivee.replace(microsecond=0)
    afk_since = "a while ago"
    if sender.is_private and sender.sender_id != 777000 and not (
            await sender.get_sender()).bot:
        if PM_AUTO_BAN:
            try:
                from userbot.modules.sql_helper.pm_permit_sql import is_approved
                apprv = is_approved(sender.sender_id)
            except AttributeError:
                apprv = True
        else:
            apprv = True
        if apprv and ISAFK:
            now = datetime.now()
            datime_since_afk = now - afk_time  # pylint:disable=E0602
            time = float(datime_since_afk.seconds)
            days = time // (24 * 3600)
            time = time % (24 * 3600)
            hours = time // 3600
            time %= 3600
            minutes = time // 60
            time %= 60
            seconds = time
            if days == 1:
                afk_since = "Yesterday"
            elif days > 1:
                if days > 6:
                    date = now + \
                        datetime.timedelta(
                            days=-days, hours=-hours, minutes=-minutes)
                    afk_since = date.strftime("%A, %Y %B %m, %H:%I")
                else:
                    wday = now + datetime.timedelta(days=-days)
                    afk_since = wday.strftime('%A')
            elif hours > 1:
                afk_since = f"`{int(hours)}h:{int(minutes)}m` ago"
            elif minutes > 0:
                afk_since = f"`{int(minutes)}m:{int(seconds)}s` ago"
            else:
                afk_since = f"`{int(seconds)}s` ago"
            if sender.sender_id not in USERS:
                if AFKREASON:
                    await sender.reply(f"{str(choice(AFKSTR))}\n"
    f"\n\nI'm AFK right now since {afk_since}"
    f"\nReason: `{AFKREASON}`")
                else:
                    await sender.reply(str(choice(AFKSTR)))
                USERS.update({sender.sender_id: 1})
                COUNT_MSG = COUNT_MSG + 1
            elif apprv and sender.sender_id in USERS:
                if USERS[sender.sender_id] % randint(2, 4) == 0:
                    if AFKREASON:
                        await sender.reply(f"**As I said, my Mastor is not online since** {afk_since}.\
                        \n**Leave your Message here and I'll go back soon..**\
                            \nAFK Reason: `{AFKREASON}`")
                    else:
                        await sender.reply(str(choice(AFKSTR)))
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1
                else:
                    USERS[sender.sender_id] = USERS[sender.sender_id] + 1
                    COUNT_MSG = COUNT_MSG + 1


CMD_HELP.update({
    "afk":
    ".afk [Optional Reason]\
\nUsage: Sets you as afk.\nReplies to anyone who tags/PM's \
you telling them that you are AFK(reason).\n\nSwitches off AFK when you type back anything, anywhere.\
"
})
