import os
import json
import firebase_admin
from firebase_admin import credentials, firestore
import time
from dotenv import load_dotenv

# Đảm bảo nạp biến môi trường
load_dotenv()

# 1. Tìm xem có biến môi trường FIREBASE_CREDENTIALS trên hệ thống không
firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS")

# 2. Xử lý logic kết nối
if firebase_creds_json:
    # Nếu chạy trên Render, nó sẽ thấy biến này và dịch chuỗi JSON đó ra
    creds_dict = json.loads(firebase_creds_json)
    cred = credentials.Certificate(creds_dict)
else:
    # Nếu chạy trên máy tính của bạn, nó sẽ không thấy biến trên và quay về đọc file local
    cred = credentials.Certificate("firebase_key.json")

# 3. Khởi tạo Firebase (có kiểm tra để tránh lỗi khởi tạo 2 lần)
if not firebase_admin._apps:
    firebase_admin.initialize_app(cred)

# Gọi database ra để chuẩn bị làm việc
db = firestore.client()

def get_chat_history(user_id, limit=10):
    """
    Hàm này lấy ra N tin nhắn gần nhất của người dùng (Cửa sổ trượt).
    Mỗi người dùng (user_id) sẽ có một "ngăn kéo" trí nhớ riêng.
    """
    # Lấy dữ liệu, sắp xếp theo thời gian mới nhất, và chỉ lấy số lượng = limit
    docs = db.collection('chats').document(str(user_id)).collection('messages')\
             .order_by('timestamp', direction=firestore.Query.DESCENDING)\
             .limit(limit).stream()
    
    history = []
    for doc in docs:
        history.append(doc.to_dict())
    
    # Vì lấy từ mới đến cũ, nên ta cần đảo ngược list lại để đúng mạch thời gian (cũ -> mới)
    return history[::-1]

def save_message(user_id, role, content):
    """
    Hàm này dùng để lưu tin nhắn mới vào Firebase.
    role: 'user' (bạn nhắn) hoặc 'model' (AI nhắn).
    """
    db.collection('chats').document(str(user_id)).collection('messages').add({
        'role': role,
        'content': content,
        'timestamp': time.time() # Đánh dấu thời gian để sau này biết tin nào gửi trước
    })