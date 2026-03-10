# Discord-AI-Girlfriend-ChatBot

# 💖 Discord AI Girlfriend ChatBot

Một dự án Bot Discord nhập vai "Bạn gái ảo" được xây dựng bằng Python. Bot sử dụng sức mạnh của **Google Gemini API** để tạo ra các đoạn hội thoại tự nhiên, có cảm xúc, kết hợp với **Firebase Firestore** để ghi nhớ ngữ cảnh cuộc trò chuyện.

## ✨ Tính năng nổi bật

- 🧠 **Trí tuệ nhân tạo (LLM):** Sử dụng mô hình `gemini-2.5-flash` cho tốc độ phản hồi cực nhanh và hoàn toàn miễn phí.
- 🎭 **Nhập vai sinh động:** AI được thiết lập (System Prompt) để luôn xưng hô chuẩn mực và miêu tả cử chỉ, hành động trong dấu `*...*` (ví dụ: `*mỉm cười*, *ôm chầm lấy anh*`).
- 💾 **Trí nhớ thông minh (Sliding Window):** Tích hợp cơ sở dữ liệu Firebase. Bot có khả năng ghi nhớ 10 tin nhắn gần nhất của từng người dùng riêng biệt để hiểu ngữ cảnh câu chuyện mà không làm quá tải Token.
- 🔒 **Cấu trúc module hóa:** Code được chia nhỏ thành các file riêng biệt (`ai_handler`, `db_handler`), dễ dàng nâng cấp và bảo trì.

---

## 🛠️ Yêu cầu hệ thống (Prerequisites)

Trước khi cài đặt, hãy đảm bảo máy tính của bạn đã có:

- **Python 3.12** (Khuyên dùng bản 3.12 để tương thích tốt nhất với các thư viện AI).
- **Discord Bot Token:** Lấy tại [Discord Developer Portal](https://discord.com/developers/applications).
- **Gemini API Key:** Lấy tại [Google AI Studio](https://aistudio.google.com/).
- **Firebase Service Account Key:** File `firebase_key.json` lấy từ [Firebase Console](https://console.firebase.google.com/).

---

## 🚀 Hướng dẫn cài đặt (Installation)

**Bước 1: Tải mã nguồn về máy**

```bash
git clone [https://github.com/iMax194/Discord-AI-Girlfriend-ChatBot.git](https://github.com/iMax194/Discord-AI-Girlfriend-ChatBot.git)
cd Discord-AI-Girlfriend-ChatBot
```

**Bước 2: Tạo và kích hoạt môi trường ảo (Virtual Environment)**

Trên Windows:

```bash
python -m venv venv
venv\Scripts\activate
```

Trên MacOS/Linux:

```bash
python3 -m venv venv
source venv/bin/activate
```

**Bước 3: Cài đặt các thư viện cần thiết**

```bash
pip install -r requirements.txt
```

**Bước 4: Thiết lập biến môi trường và Database**

Tạo một file tên là .env ở thư mục gốc của dự án.

Dán các mã bí mật của bạn vào file .env theo định dạng sau:

```
DISCORD_TOKEN="dán_token_discord_của_bạn_vào_đây"
GEMINI_API_KEY="dán_api_key_gemini_của_bạn_vào_đây"
```

Đưa file chìa khóa của Firebase (đã đổi tên thành firebase_key.json) vào cùng thư mục gốc.

⚠️ CẢNH BÁO QUAN TRỌNG: Tuyệt đối KHÔNG đưa file .env và firebase_key.json lên GitHub để tránh lộ thông tin bảo mật! (Dự án đã có sẵn file .gitignore để chặn việc này).

### 📅 Phụ lục: Hướng dẫn thiết lập Google Calendar API (Bắt buộc để dùng tính năng Đặt lịch)

Để Bot có quyền xem và ghi sự kiện vào lịch của bạn, bạn cần tạo một "Service Account" (Tài khoản dịch vụ robot) trên hệ thống của Google và chia sẻ lịch cá nhân cho robot này.

**Bước 1: Bật API và tạo Service Account**

1. Truy cập [Google Cloud Console](https://console.cloud.google.com/).
2. Tạo một Project mới (hoặc chọn Project đang chứa Gemini API của bạn).
3. Tìm kiếm **Google Calendar API** trên thanh tìm kiếm và bấm **Enable** (Bật).
4. Điều hướng tới menu **IAM & Admin** > **Service Accounts**.
5. Bấm **Create Service Account**, đặt tên (ví dụ: `bot-calendar`) và bấm **Done**.
6. **[Quan trọng]** Copy lại địa chỉ email của Service Account vừa tạo (có đuôi dạng `...iam.gserviceaccount.com`).

**Bước 2: Lấy chìa khóa (File JSON)**

1. Bấm vào tên Service Account bạn vừa tạo.
2. Chuyển sang tab **Keys** > **Add Key** > **Create new key** > Chọn định dạng **JSON**.
3. File sẽ tự động tải về. Hãy đổi tên file đó thành **`google_calendar.json`** và copy vào thư mục gốc của dự án này.
   _(Lưu ý: File này đã được thêm vào `.gitignore` để bảo mật)._

**Bước 3: Chia sẻ quyền ghi Lịch cá nhân cho Bot (Bước quyết định)**

1. Mở [Google Calendar](https://calendar.google.com/) cá nhân của bạn trên trình duyệt.
2. Bấm vào biểu tượng Bánh răng (Cài đặt) góc trên bên phải > **Cài đặt**.
3. Ở cột bên trái, tìm và nhấp vào lịch chính của bạn (thường mang tên bạn).
4. Cuộn xuống mục **Chia sẻ với những người hoặc nhóm cụ thể** > Bấm **Thêm người và nhóm**.
5. Dán địa chỉ email Service Account (đã copy ở Bước 1) vào ô trống.
6. Ở mục Quyền, bạn **bắt buộc phải chọn**: **"Thực hiện thay đổi đối với sự kiện"** (Make changes to events).
7. Bấm **Gửi**.

Vậy là xong! Bây giờ Bot đã được ủy quyền hợp lệ để tự động ghi lịch hẹn trực tiếp vào Google Calendar của bạn.

🎮 Cách sử dụng (Usage)
Để khởi động Bot, hãy chắc chắn bạn đang ở trong môi trường ảo (venv) và chạy lệnh sau:

Bash
python main.py
Nếu Terminal hiện dòng chữ 💖 Bạn gái ảo ... đã thức dậy và online!, nghĩa là bot đã hoạt động thành công. Bạn có thể vào server Discord và bắt đầu trò chuyện!

📁 Cấu trúc dự án (Project Structure)

```
Plaintext
Discord-AI-Girlfriend-ChatBot/
├── .env                  # (Bạn tự tạo) Chứa Token và API Key
├── firebase_key.json     # (Bạn tự thêm) Chìa khóa kết nối Firebase
├── google_calendar.json  # (Bạn tự thêm) Chìa khóa kết nối Google Calendar
├── requirements.txt      # Danh sách thư viện
├── config.py             # Nạp biến môi trường
├── keep_alive.py         # Giúp Render nhận diện Bot đang chạy
├── main.py               # File chạy chính của Bot
└── utils/
    ├── ai_handler.py     # Xử lý giao tiếp với Gemini API & Tính cách
    ├── calendar_handler.py # Xử lý đặt lịch với Google Calendar API
    ├── db_handler.py     # Xử lý lưu/đọc lịch sử chat với Firebase
    └── game_handler.py   # Xủ lý trò chơi trong Discord
```

Dự án được xây dựng với mục đích học tập và giải trí cá nhân.
