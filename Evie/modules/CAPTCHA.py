from Evie import tbot, CMD_HELP, MONGO_DB_URI
import os, asyncio
from telethon import Button, events
from random import shuffle
from pyrogram import emoji
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
captcha = db.captcha

async def kick_restricted_after_delay(delay, event, user_id):
    await asyncio.sleep(delay)
    user_id = user_id
    await event.delete()
    await tbot.kick_participant(event.chat_id, user_id)

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
  
  if not event.user_joined:
          return
  user_id = event.user_id
  chats = captcha.find({})
  for c in chats:
       if not event.chat_id == c["id"]:
          return
       if event.chat_id == c["id"]:
          type = c["type"]
  if not type == "button":
     return
  a_user = await event.get_user()
  mention = "[{}](tg://user?id={})".format(a_user.first_name, a_user.id)
  text = (f"Welcome, {mention}\nAre you human?\n\nClick on the button which include this emoji {emoji.CHECK_MARK_BUTTON}.")
  keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data=f'pep-{a_user.id}'
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data=f'pro-{a_user.id}'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data=f"fk-{a_user.id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data=f'yu-{a_user.id}'
            )
        ]
  shuffle(keyboard)
  button_message = await event.reply(
            text,
            buttons=keyboard
        )
  WELCOME_DELAY_KICK_SEC = 20
  asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
  await asyncio.sleep(0.5)


@tbot.on(events.CallbackQuery(pattern=r"fk-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data=f"pep-{user_id}"
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data=f'pro-{user_id}'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"pep-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data=f"pep-{user_id}"
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data=f'pro-{user_id}'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)
    
@tbot.on(events.CallbackQuery(pattern=r"yu-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("❌ Wrong Try Again!")
    keyboard = [
            Button.inline(
                f"{emoji.BRAIN}",
                data=f"pep-{user_id}"
            ),
            Button.inline(
                f"{emoji.CHECK_MARK_BUTTON}",
                data=f'pro-{user_id}'
            ),
            Button.inline(
                f"{emoji.CROSS_MARK}",
                data=f"fk-{user_id}"
            ),
            Button.inline(
                f"{emoji.ROBOT}",
                data=f'yu-{user_id}'
            )
        ]
    shuffle(keyboard)
    await event.edit(buttons=keyboard)
  
@tbot.on(events.CallbackQuery(pattern=r"pro-(\d+)"))
async def cbot(event):
    user_id = int(event.pattern_match.group(1))
    chat_id = event.chat_id
    if not event.sender_id == user_id:
        await event.answer("You aren't the person whom should be verified.")
        return
    await event.answer("Verified Successfully ✅")
    await event.edit(buttons=None)
  
  

    
          
  
  
  
