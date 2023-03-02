import asyncio
from pyrogram import Client, filters
import os
import openai
import logging
import time
import json

# set up logging
logging.basicConfig(filename='chatgpt-bot-errors.txt', level=logging.ERROR,
                    format='[%(asctime)s] [%(levelname)s] [%(funcName)s] %(message)s',
                    datefmt='%Y-%m-%d %H:%M:%S')

# your openai key goes here :)
openai.api_key = "APIKEYHERE"

# telegram api_id and hash
api_id = 12345678
api_hash = 'APIHASHHERE'
bot_token = 'BOTTOKENHERE'

app = Client(
    "my_bot",
    api_id=api_id, api_hash=api_hash,
    bot_token=bot_token
)

# on /start bot sends what he can

@app.on_message(filters.command(["start"]))
def startcmd(client, message):
    message.reply('🤖 ChatGPT now in Telegram! It\'s absolutely free, You don\'t need to subscribe anywhere.\n\nCommands:\n/gpt request - generates request')

# on /gpt it sends request to ChatGPT and sends answer 
@app.on_message(filters.command(["gpt"]))
def gpt_handler(client, message):
    myprompt = message.text.split(None, 1)[1]
    message.reply('🤖 ChatGPT generating answer...')
    try:
        rawresponse = openai.Completion.create(
          model="text-davinci-003",
          prompt=myprompt,
          temperature=0,
          max_tokens=60,
          top_p=1,
          frequency_penalty=0,
          presence_penalty=0
       )
        jsstr = json.dumps(rawresponse)
        response_dict = json.loads(jsstr)
        response = response_dict.get("choices", [{"text": "Error"}])[0].get("text")
        if response:
            message.reply(f'{response}\n\n Your request for ChatGPT: {myprompt}')
        else:
            message.reply(f'🚫 Error found!\nResponse from API does not contain text property: {response_dict}')
            logging.error(f'Response from API does not contain text property: {response_dict}', exc_info=False)
    except Exception as e:
        message.reply('🚫 Error found!\nError: %s' % e)
        logging.error('Error: %s' % e, exc_info=False)

if __name__ == "__main__":
    print('[ChatGPT] Running')
    app.run()