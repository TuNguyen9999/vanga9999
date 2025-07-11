# Stock News Bot

Bot tự động thu thập và gửi tin tức chứng khoán từ các trang web tài chính Việt Nam.

## Tính năng

- 🔍 Thu thập tin tức từ Cafef, Vietnambiz, Tin nhanh chứng khoán
- 📈 Theo dõi hơn 200 mã cổ phiếu VN30 và các cổ phiếu khác
- 📧 Gửi email tự động với định dạng HTML đẹp mắt
- 🤖 Bot Telegram với lệnh `/news [dd-mm-yyyy]`
- ⏰ Lập lịch tự động gửi tin tức hàng ngày
- 🌐 Web server để giữ bot hoạt động

## Cài đặt

1. Clone repository:
```bash
git clone <repository-url>
cd stock-news-bot
```

2. Cài đặt dependencies:
```bash
pip install -r requirements.txt
```

3. Cấu hình environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export EMAIL_SENDER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECIPIENT="recipient@email.com"
export VIETCAPITAL_EMAILS="email1@vietcapital.com.vn,email2@vietcapital.com.vn"
```

## Sử dụng

### Chạy bot:
```bash
python main.py
```

### Lệnh Telegram:
- `/news` - Lấy tin tức hôm nay
- `/news 21-04-2025` - Lấy tin tức cho ngày cụ thể

## Cấu trúc project

```
stock-news-bot/
├── main.py              # File chính chứa logic bot
├── requirements.txt     # Dependencies
├── README.md           # Tài liệu hướng dẫn
└── .env               # Environment variables (optional)
```

## Cấu hình

### Danh sách mã cổ phiếu
Chỉnh sửa `TICKER_COMPANY_MAP` trong `main.py` để thêm/bớt mã cổ phiếu cần theo dõi.

### Lịch gửi tin tức
Mặc định bot sẽ gửi tin tức vào:
- 13:15 hàng ngày
- 20:00 hàng ngày

### URL nguồn tin tức
Bot thu thập tin tức từ:
- https://cafef.vn
- https://vietnambiz.vn  
- https://www.tinnhanhchungkhoan.vn

## Tuân thủ chuẩn PTB 20.7

- ✅ Type hints cho tất cả functions
- ✅ Docstrings với format chuẩn
- ✅ Error handling đầy đủ
- ✅ Logging và monitoring
- ✅ Code formatting với Black
- ✅ Static type checking với MyPy
- ✅ Linting với Pylint

## License

MIT License 
