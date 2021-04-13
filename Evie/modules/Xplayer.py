from telethon import Button


@register(pattern="^/ano")
async def k(event):
 buttons= Button.inline('test', data='tp')
 text = 'anonindian'
 await event.reply(text, buttons=buttons)

@tbot.on(events.CallbackQuery(pattern=r"tp"))
async def cbot(event):
 await tbot.send_message(event.chat_id, f'{event.sender_id}')
