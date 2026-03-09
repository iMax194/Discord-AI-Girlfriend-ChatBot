import os
import json
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()

SCOPES = ['https://www.googleapis.com/auth/calendar']

# 1. Tìm xem có biến môi trường GOOGLE_CALENDAR_CREDS trên hệ thống không
calendar_creds_json = os.getenv("GOOGLE_CALENDAR_CREDS")

# 2. Xử lý logic kết nối
if calendar_creds_json:
    # Nếu chạy trên Render
    creds_dict = json.loads(calendar_creds_json)
    creds = service_account.Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
else:
    # Nếu chạy trên máy tính của bạn
    creds = service_account.Credentials.from_service_account_file('google_calendar.json', scopes=SCOPES)

service = build('calendar', 'v3', credentials=creds)

# ĐÂY LÀ HÀM MÀ AI SẼ TỰ ĐỘNG GỌI KHI BẠN NHỜ ĐẶT LỊCH
def add_calendar_event(title: str, date: str, time: str, duration_minutes: int = 60) -> str:
    """
    Sử dụng công cụ này để tạo sự kiện vào Google Calendar.
    - title: Tiêu đề sự kiện (ví dụ: "Họp nhóm", "Đi chơi với Yumi")
    - date: Ngày diễn ra theo định dạng YYYY-MM-DD (ví dụ: 2026-03-10)
    - time: Giờ diễn ra theo định dạng HH:MM (ví dụ: 14:30)
    - duration_minutes: Thời lượng (mặc định 60 phút)
    """
    try:
        # Xử lý ngày giờ
        start_time_str = f"{date}T{time}:00"
        start_time = datetime.datetime.strptime(start_time_str, "%Y-%m-%dT%H:%M:%S")
        end_time = start_time + datetime.timedelta(minutes=duration_minutes)

        event = {
            'summary': title,
            'start': {
                'dateTime': start_time.isoformat(),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
            'end': {
                'dateTime': end_time.isoformat(),
                'timeZone': 'Asia/Ho_Chi_Minh',
            },
        }

        # ĐIỀN EMAIL CỦA BẠN VÀO ĐÂY (Email mà bạn đã cấp quyền cho robot ở Bước 1)
        calendar_id = "namphamat2017@gmail.com" 

        service.events().insert(calendarId=calendar_id, body=event).execute()
        return f"Hệ thống: Đã đặt lịch thành công '{title}' vào lúc {time} ngày {date}."
    
    except Exception as e:
        return f"Hệ thống báo lỗi: {str(e)}"