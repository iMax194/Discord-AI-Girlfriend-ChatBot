import discord
import random

# Hàm tạo bộ bài 52 lá
def create_deck():
    suits = ['♠️', '♥️', '♣️', '♦️']
    ranks = ['2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A']
    return [f"{rank}{suit}" for suit in suits for rank in ranks]

# Hàm tính điểm Xì Dách
def calculate_score(hand):
    score = 0
    aces = 0
    for card in hand:
        rank = card[:-2] # Lấy phần số/chữ, bỏ cái hình chất đi
        if rank in ['J', 'Q', 'K']:
            score += 10
        elif rank == 'A':
            aces += 1
            score += 11
        else:
            score += int(rank)
            
    # Xử lý lá Át (A) nếu bị quắc (quá 21 điểm) thì tính là 1
    while score > 21 and aces > 0:
        score -= 10
        aces -= 1
    return score

# Giao diện Nút bấm cho game Xì Dách
class BlackjackView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=120) # Ván bài hết hạn sau 2 phút nếu không bấm
        self.deck = create_deck()
        random.shuffle(self.deck)
        
        # Chia mỗi người 2 lá
        self.player_hand = [self.deck.pop(), self.deck.pop()]
        self.bot_hand = [self.deck.pop(), self.deck.pop()]

    # Hàm định dạng tin nhắn gửi lên Discord
    def format_game_state(self, reveal_bot=False, end_msg=""):
        player_score = calculate_score(self.player_hand)
        bot_score = calculate_score(self.bot_hand)
        
        player_str = "  ".join(self.player_hand)
        
        if reveal_bot:
            bot_str = "  ".join(self.bot_hand)
            bot_score_str = f"(Điểm: {bot_score})"
        else:
            bot_str = f"{self.bot_hand[0]}  🎴 (Úp 1 lá)"
            bot_score_str = ""
            
        msg = f"**🎲 SÒNG BÀI XÌ DÁCH CỦA KAZUSA**\n\n"
        msg += f"🤖 **Yumi:** {bot_str} {bot_score_str}\n"
        msg += f"👤 **Anh:** {player_str} (Điểm: {player_score})\n\n"
        
        if end_msg:
            msg += f"**Kết quả:** *{end_msg}*"
        else:
            msg += "*Anh rút thêm hay dằn bài đây? (Dưới 16 là phải rút nha)*"
            
        return msg, player_score, bot_score

    @discord.ui.button(label="Rút bài 🃏", style=discord.ButtonStyle.primary)
    async def hit(self, interaction: discord.Interaction, button: discord.ui.Button):
        self.player_hand.append(self.deck.pop())
        msg, p_score, b_score = self.format_game_state()
        
        # Nếu người chơi Quắc
        if p_score > 21:
            msg, _, _ = self.format_game_state(reveal_bot=True, end_msg="Quắc rồi nha anh trai! Đưa tiền đây lêu lêu 😜")
            for child in self.children: child.disabled = True # Tắt nút
            
        await interaction.response.edit_message(content=msg, view=self)

    @discord.ui.button(label="Dằn bài 🛑", style=discord.ButtonStyle.danger)
    async def stand(self, interaction: discord.Interaction, button: discord.ui.Button):
        p_score = calculate_score(self.player_hand)
        b_score = calculate_score(self.bot_hand)
        
        # Yumi tự động rút bài nếu điểm của cô ấy dưới 17 (luật chuẩn Dealer)
        while b_score < 17:
            self.bot_hand.append(self.deck.pop())
            b_score = calculate_score(self.bot_hand)
            
        # So điểm
        if b_score > 21:
            end_msg = "Á á em quắc rồi! Anh ăn may thôi nhé 😤"
        elif b_score > p_score:
            end_msg = "Hehe điểm em cao hơn, em thắng nha! *chìa tay xin tiền* 🤑"
        elif b_score < p_score:
            end_msg = "Huhuhu thua rồi, anh ăn gian đúng không? Bắt đền 😭"
        else:
            end_msg = "Hòa rồiiii, ván sau em phục thù! 🤝"
            
        msg, _, _ = self.format_game_state(reveal_bot=True, end_msg=end_msg)
        for child in self.children: child.disabled = True
        await interaction.response.edit_message(content=msg, view=self)