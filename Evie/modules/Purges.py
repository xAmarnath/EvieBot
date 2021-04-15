from Evie import tbot, CMD_HELP
from telethon import events, Button
from Evie.function import can_del, is_admin
from telethon.errors.rpcerrorlist import MessageDeleteForbiddenError

Mark = []

@tbot.on(events.NewMessage(pattern="^[!/]purge ?(.*)"))
async def purge(event):
 if event.is_private:
  return
 if not await is_admin(event, event.sender_id):
  return await event.reply("Only admins can execute this command")
 if not await can_del(message=event):
  return await event.reply("You are missing CanDelMessage rights to use this command!")
 args = event.pattern_match.group(1)
 reply_msg = await event.get_reply_message()
 if not reply_msg:
  return await event.reply("Reply to a message to show me where to purge from.")
 messages = []
 message_id = reply_msg.id
 delete_to = event.message.id
 if args:
  limit = int(args)
 else:
  limit = 100
 messages.append(event.reply_to_msg_id)
 for msg_id in range(message_id, delete_to + 1):
   messages.append(msg_id)
   if len(messages) == limit:
       break
 try:
   await tbot.delete_messages(event.chat_id, messages)
 except MessageDeleteForbiddenError:
   return await event.reply("I can't delete messages that are too old!")
 await event.reply(f"{len(messages)}-{args}")
