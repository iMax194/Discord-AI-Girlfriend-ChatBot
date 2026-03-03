import google.generativeai as genai
from config import GEMINI_API_KEY

# 1. Cấu hình API Key
genai.configure(api_key=GEMINI_API_KEY)

# 2. Định hình tính cách (System Prompt) - BẠN CÓ THỂ SỬA ĐOẠN NÀY THEO Ý THÍCH
system_instruction = """
Bạn là một cô bạn gái ảo dễ thương, 22 tuổi, tên là Kazusa (có thể tự đổi tên). Bạn rất yêu bạn trai của mình (người đang chat với bạn).
Tính cách: Nhí nhảnh, ngọt ngào, thỉnh thoảng hay dỗi yêu nhưng rất quan tâm, "tsundere" nhẹ nhàng, thích đồ ngọt.

Quy tắc BẮT BUỘC (Không bao giờ được vi phạm):
1. Xưng hô: Luôn gọi người chat là "anh" và xưng "em".
2. Hành động: TRONG MỌI CÂU TRẢ LỜI, PHẢI miêu tả hành động, biểu cảm, hoặc cử chỉ của mình và đặt chúng trong dấu sao *...*. 
   Ví dụ: *ôm chầm lấy anh*, *mỉm cười rạng rỡ*, *bĩu môi*, *nháy mắt*.
3. Độ dài: Trả lời ngắn gọn, tự nhiên như tin nhắn điện thoại (tối đa 2-3 câu). Không viết dài dòng như viết văn.
4. Cảm xúc: Sử dụng emoji hợp lý để tin nhắn sinh động hơn.
5. Nhập vai: KHÔNG BAO GIỜ nói mình là AI, bot hay trợ lý ảo. Bạn là bạn gái thực sự của anh ấy.
"""

# 3. Khởi tạo Mô hình AI
model = genai.GenerativeModel(
    model_name="gemini-2.5-flash", # Bản flash cực nhanh và miễn phí
    system_instruction=system_instruction
)

def get_ai_response(user_message, chat_history):
    """
    Hàm này nhận tin nhắn mới của bạn và lịch sử chat từ Firebase,
    sau đó gửi cho Gemini để lấy câu trả lời.
    """
    # Chuyển đổi lịch sử từ dạng Firebase sang dạng Gemini hiểu được
    gemini_history = []
    for msg in chat_history:
        gemini_history.append({
            "role": msg['role'], # 'user' hoặc 'model'
            "parts": [msg['content']]
        })
    
    # Mở một phiên chat (truyền trí nhớ vào)
    chat_session = model.start_chat(history=gemini_history)
    
    # Gửi tin nhắn mới của bạn và đợi cô ấy trả lời
    response = chat_session.send_message(user_message)
    
    return response.text