from .. import bot
from telethon import events
import requests
from config import vars

def send_message(number, message):
    base_url = 'http://enterprise.smsgupshup.com/GatewayAPI/rest?method=sendMessage'
    params = {
        'send_to':number,
        'msg': f'{message} is your CollegeSearch Mobile Verification OTP',
        'userid':'2000192767',
        'password':'YYyzU9YC',
        'v':'1.1',
        'msg_type':'TEXT',
        'auth_scheme':'PLAIN'
            }
    if len(message) <= vars.max:
        result = requests.get(base_url, params=params) 
        result_text = result.text
        status_code = result.status_code
    else:
        result_text = f'Max message length should be {vars.max} letters.'
        status_code = None
    return result_text, status_code

@bot.on(events.NewMessage(pattern='/send$', func=lambda e: e.is_private))
async def send(event):
    async with bot.conversation(await event.get_chat(), exclusive=False, total_timeout=600) as conv:
        await conv.send_message("Send me INDIAN 🇮🇳 number without +91 in 60 seconds.")
        phone_number = await conv.get_response(timeout=(60))
        await conv.send_message(f"Now send me message to send to +91{phone_number.text}. (Less than {vars.max} words.)")
        message = await conv.get_response(timeout=(60))
        sms_resp, status_code = send_message(phone_number.text,  message.text)
        await conv.send_message(f"**Response from API** : `{sms_resp}`.\n**Status code** : `{status_code}`\nThanks for using this bot.")

