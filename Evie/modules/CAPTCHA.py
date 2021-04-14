from Evie import tbot, CMD_HELP, MONGO_DB_URI
import os, asyncio
from telethon import Button, events
from Evie.function import gen_captcha
from Evie.events import register
from captcha.image import ImageCaptcha
image_captcha = ImageCaptcha(width = 400, height = 270)
from random import shuffle
import random
from pyrogram import emoji
from pymongo import MongoClient
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
captcha = db.capt

chat = None
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
       if event.chat_id == c["id"]:
          type = c["type"]
          time = c["time"]
  if not type:
    return
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
  if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
  if not event.user_joined:
          return
  user_id = event.user_id
  chats = captcha.find({})
  for c in chats:
       if event.chat_id == c["id"]:
          type = c["type"]
          time = c["time"]
  if not type:
    return
  if not type == "math":
     return
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  buttons = Button.url("Click here to prove you are human", "t.me/MissEvie_Robot?start=math_{}".format(event.chat_id))
  await event.reply(text, buttons=buttons)


@register(pattern="^/start math_(.*)")
async def h(event):
 try:
  if not event.is_private:
   return
  chat = int(event.pattern_match.group(1))
  x = random.randint(1,100)
  y = random.randint(1,100)
  a = x + y
  d = random.randint(1, 100)
  b = random.randint(1, 100)
  c = random.randint(1, 100)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='sikle_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='babe'
            ),],
            [Button.inline(
                f"{c}",
                data='nide'
            ),
            Button.inline(
                f"{d}",
                data='nipa'
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.5)
  await tbot.send_message(event.chat_id, f"**What is the sum of {x} + {y}?**\n\nChoose the correct option from Below to get verified.", buttons=keyboard)
 except Exception as e:
   await event.reply(f"{e}")

@tbot.on(events.ChatAction())  # pylint:disable=E0602
async def _(event):
  if not event.user_joined:
          return
  user_id = event.user_id
  chats = captcha.find({})
  for c in chats:
       if event.chat_id == c["id"]:
          type = c["type"]
          time = c["time"]
  if not type:
    return
  if not type == "text":
     return
  try:
    await tbot(EditBannedRequest(event.chat_id, user_id, MUTE_RIGHTS))
  except:
    pass
  text = f"Hey {event.user.first_name} Welcome to {event.chat.title}!"
  buttons = Button.url("Click here to prove you are human", "t.me/MissEvie_Robot?start=captcha_{}".format(event.chat_id))
  await event.reply(text, buttons=buttons)
  WELCOME_DELAY_KICK_SEC = time
  if not time == 0:
    asyncio.create_task(kick_restricted_after_delay(
            WELCOME_DELAY_KICK_SEC, event, user_id))
    await asyncio.sleep(0.5)

chance = 3
 
@register(pattern="^/start captcha_(.*)")
async def h(event):
  if not event.is_private:
   return
  chat = int(event.pattern_match.group(1))
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip_{}'.format(chat)
            ),
            Button.inline(
                f"{b}",
                data='exec'
            ),],
            [Button.inline(
                f"{c}",
                data='sli'
            ),
            Button.inline(
                f"{d}",
                data='paku'
            )]
        ]
  shuffle(keyboard)
  await asyncio.sleep(0.5)
  await tbot.send_message(event.chat_id, "Please choose the text from image", file='./captcha.png', buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"pip(\_(.*))"))
async def bak(event):
 tata = event.pattern_match.group(1)
 data = tata.decode()
 chat_id = int(data.split("_", 1)[1])
 user_id = event.sender_id
 await event.edit("Successfully Verified✅, now you can message in the chat!", buttons=None)
 try:
   await tbot(EditBannedRequest(chat_id, user_id, UNMUTE_RIGHTS))
 except:
   pass
 global chance
 chance = 3

@tbot.on(events.CallbackQuery(pattern=r"exec"))
async def bak(event):
  global chance
  chance -= 1
  await event.answer("Wrong try again!")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip'
            ),
            Button.inline(
                f"{b}",
                data='exec'
            ),],
            [Button.inline(
                f"{c}",
                data='sli'
            ),
            Button.inline(
                f"{d}",
                data='paku'
            )]
        ]
  shuffle(keyboard)
  shuffle(keyboard)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"sli"))
async def bak(event):
  global chance
  chance -= 1
  await event.answer("Wrong try again❌")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip'
            ),
            Button.inline(
                f"{b}",
                data='exec'
            ),],
            [Button.inline(
                f"{c}",
                data='sli'
            ),
            Button.inline(
                f"{d}",
                data='paku'
            )]
        ]
  shuffle(keyboard)
  shuffle(keyboard)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)

@tbot.on(events.CallbackQuery(pattern=r"paku"))
async def bak(event):
  global chance
  chance -= 1
  await event.answer("Wrong try again❌")
  if chance == 0:
     chance += 3
     return await event.edit("Your chances are exchausted, verification failed❌", buttons=None)
  a = gen_captcha(8)
  b = gen_captcha(8)
  c = gen_captcha(8)
  d = gen_captcha(8)
  image = image_captcha.generate_image(a)
  image_file = "./"+ "captcha.png"
  image_captcha.write(a, image_file)
  keyboard = [
            [Button.inline(
                f"{a}",
                data='pip'
            ),
            Button.inline(
                f"{b}",
                data='exec'
            ),],
            [Button.inline(
                f"{c}",
                data='sli'
            ),
            Button.inline(
                f"{d}",
                data='paku'
            )]
        ]
  shuffle(keyboard)
  shuffle(keyboard)
  text = f"Try again you have {chance} chances left"
  await event.edit(text, file="./captcha.png", buttons=keyboard)


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
 try:
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
        {"id": event.chat_id, "type": 'text', "time": time}
    )
 except Exception as e:
  print(e)
            
 
@register(pattern="^/captchamode ?(.*)")
async def t(event):
 arg = event.pattern_match.group(1)
 chats = captcha.find({})
 if not arg:
   for c in chats:
      if event.chat_id == c["id"]:
         type = c["type"]
   if type:
     return await event.reply(f"Current captcha mode is **{type}**")
   else:
     return await event.reply("Captcha is off for this Chat")
 if not arg == "button" and not arg == "text" and not arg == "math":
   return await event.reply(f"'{arg}' is not a recognised CAPTCHA mode! Try one of: button/math/text")
 type = arg
 try:
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
                {"$set": {"type": type}},
            )
          return
  captcha.insert_one(
        {"id": event.chat_id, "type": type, "time": 0}
    )
 except Exception as e:
  print(e)
            
 

