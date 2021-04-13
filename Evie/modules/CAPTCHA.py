from Evie import tbot, CMD_HELP, MONGO_DB_URI
import os, asyncio
from telethon import Button, events
from Evie.events import register
from random import shuffle
from pyrogram import emoji
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
captcha = db.captch


from telethon.tl.types import ChatBannedRights
from telethon.tl.functions.channels import EditBannedRequest

MUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=True)
UNMUTE_RIGHTS = ChatBannedRights(until_date=None, send_messages=False)

def get_chat(id):
    return captcha.find_one({"id": id})

async def kick_restricted_after_delay(delay, event, user_id):
    await asyncio.sleep(delay)
    k = await tbot.get_permissions(event.chat_id, user_id)
    if not k.is_banned:
      return
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
          time = c["time"]
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
  WELCOME_DELAY_KICK_SEC = time
  await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
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
    await tbot(EditBannedRequest(event.chat_id, user_id, UNMUTE_RIGHTS))
    await event.edit(buttons=None)

@register(pattern="^/captchakicktime ?(.*)")
async def t(event):
 try:
  time = int(event.pattern_match.group(1))
 except:
  return await event.reply("Please Specify in Seconds **For Now**")
 chats = captcha.find({})
 for c in chats:
      if event.chat_id == c["id"]:
          to_check = get_chat(id=event.chat_id)
          captcha.update_one(
                {
                    "_id": to_check["_id"],
                    "id": to_check["id"],
                    "type": to_check["type"],
                    "time": to_check["time"],
                },
                {"$set": {"time": time}},
            )
          return
 captcha.insert_one(
        {"id": event.sender_id, "type": 'text', "time": time}
    )
            
 
