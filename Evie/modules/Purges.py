from Evie import tbot, CMD_HELP, MONGO_DB_URI
from telethon import events, Button
from Evie.function import can_del, is_admin
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError
from pymongo import MongoClient

Mark = []
client = MongoClient()
client = MongoClient(MONGO_DB_URI)
db = client["evie"]
pugre = db.purge

def get_chat(id):
    return pugre.find_one({"id": id})

@tbot.on(events.NewMessage(pattern="^[!/]purge ?(.*)"))
async def purge(event):
 args = event.pattern_match.group(1)
 try:
  k = int(args)
 except:
   return
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing DelMessage rights to use this command!")
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 if args:
  limit = int(args)
  if limit == 1:
    return await event.reply("Oh please use `/del` ಥ‿ಥ")
 else:
  limit = 300
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")

@tbot.on(events.NewMessage(pattern="^[!/]purgefrom"))
async def mm(event):
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing delmessage rights to use this command!")
 global Mark
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 msg_id = reply_msg.id
 chats = pugre.find({})
 for c in chats:
  if event.chat_id == c["id"]:
    to_check = get_chat(id=event.chat_id)
    pugre.update_one(
           {
              "_id": to_check["_id"],
              "id": to_check["id"],
              "msg_id": to_check["msg_id"],
            },
             {"$set": {"msg_id": msg_id}},
            )
    return await tbot.send_message(event.chat_id, "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", reply_to=msg_id)
 pugre.insert_one(
        {"id": event.chat_id, "msg_id": msg_id}
    )
 await tbot.send_message(event.chat_id, "Message marked for deletion. Reply to another message with /purgeto to delete all messages in between.", replt_to=msg_id)

 

