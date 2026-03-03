import discord
from config import DISCORD_TOKEN
from utils.db_handler import get_chat_history, save_message
from utils.ai_handler import get_ai_response

# 1. Thiết lập quyền hạn
intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)

# 2. Khi Bot online
@client.event
async def on_ready():
    print("="*40)
    print(f'💖 Bạn gái ảo {client.user} đã thức dậy và online!')
    print("="*40)

# 3. Khi có tin nhắn
@client.event
async def on_message(message):
    if message.author == client.user:
        return

    user_id = str(message.author.id)
    user_text = message.content

    async with message.channel.typing():
        try:
            save_message(user_id, "user", user_text)
            history = get_chat_history(user_id, limit=10)
            ai_reply = get_ai_response(user_text, history)
            save_message(user_id, "model", ai_reply)
            
            await message.channel.send(ai_reply)
        except Exception as e:
            print(f"Lỗi: {e}")
            await message.channel.send("*bối rối* Mạng lag quá anh ơi, nhắn lại em với 🥺")

client.run(DISCORD_TOKEN)