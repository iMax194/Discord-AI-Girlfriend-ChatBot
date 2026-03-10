import discord
from config import DISCORD_TOKEN
from utils.db_handler import get_chat_history, save_message
from utils.ai_handler import get_ai_response
from utils.game_handler import BlackjackView

from keep_alive import keep_alive
keep_alive() # Gọi Web server để giữ bot sống

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
            # KIỂM TRA TỪ KHÓA ĐỂ KÍCH HOẠT GAME XÌ DÁCH
            if "chơi xì dách" in user_text.lower() or "chơi blackjack" in user_text.lower():
                view = BlackjackView()
                msg, _, _ = view.format_game_state()
                await message.channel.send(msg, view=view)
                return # Dừng ở đây để không gửi tin nhắn này cho Gemini

            save_message(user_id, "user", user_text)
            history = get_chat_history(user_id, limit=10)
            ai_reply = get_ai_response(user_text, history)
            save_message(user_id, "model", ai_reply)
            
            await message.channel.send(ai_reply)
        except Exception as e:
            print(f"Lỗi: {e}")
            await message.channel.send("*bối rối* Mạng lag quá anh ơi, nhắn lại em với 🥺")

client.run(DISCORD_TOKEN)