import os
import json
from dotenv import load_dotenv
from fastapi import FastAPI, Header, HTTPException, Depends, Request
from telegram import Bot

app = FastAPI()

# Load variables from .env file if present
load_dotenv()

# Read the variable from the environment (or .env file)
bot_token = os.getenv('BOT_TOKEN')
secret_token = os.getenv("SECRET_TOKEN")
# webhook_url = os.getenv('CYCLIC_URL', 'http://localhost:8181') + "/webhook/"

bot = Bot(token=bot_token)


# bot.set_webhook(url=webhook_url)
# webhook_info = bot.get_webhook_info()
# print(webhook_info)

def auth_telegram_token(x_telegram_bot_api_secret_token: str = Header(None)) -> str:
    # return true # uncomment to disable authentication
    if x_telegram_bot_api_secret_token != secret_token:
        raise HTTPException(status_code=403, detail="Not authenticated")
    return x_telegram_bot_api_secret_token


@app.post("/webhook/")
async def handle_webhook(request: Request, token: str = Depends(auth_telegram_token)):
    print("Request:", request)
    title = ""
    try:
        update = await request.json()
        user = update["message"]["from"]["first_name"]
        chat_id = update["message"]["chat"]["id"]
        message_id = update["message"]["message_id"]
        message =  user + " не пости Труху! Ми тут такого не любимо!!!"
        title = update["message"]["forward_origin"]["chat"]["title"]
        if "Труха⚡️" in title:
            await bot.deleteMessage(chat_id=chat_id, message_id=message_id)
            await bot.send_message(chat_id=chat_id, text=message)
            with open('cat.png', 'rb') as photo:
                await bot.send_photo(chat_id=chat_id, photo=photo)
    except Exception as e:
        print('Error', str(e))
    return {"ok": True}
