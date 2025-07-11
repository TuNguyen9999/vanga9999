# 🤖 Stock News Bot

Bot tự động thu thập và gửi tin tức chứng khoán qua Telegram và Email.

## 🚀 Tính năng

- ✅ Thu thập tin tức từ Cafef, Vietnambiz, Tin nhanh chứng khoán
- ✅ Tự động gửi email hàng ngày (13:15 và 20:00)
- ✅ Bot Telegram với lệnh `/news [dd-mm-yyyy]`
- ✅ Web server để giữ bot hoạt động
- ✅ Xử lý lỗi và khởi động lại an toàn

## 📋 Yêu cầu

- Python 3.8+
- Telegram Bot Token
- Gmail App Password

## 🛠️ Cài đặt

1. **Clone repository:**
```bash
git clone <repository-url>
cd stock-news-bot
```

2. **Cài đặt dependencies:**
```bash
pip install -r requirements.txt
```

3. **Cấu hình:**
   - Tạo bot Telegram và lấy token
   - Tạo Gmail App Password
   - Cập nhật thông tin trong `main.py`

## 🚀 Khởi động

### Cách 1: Sử dụng script khởi động (Khuyến nghị)
```bash
python start_bot.py
```

### Cách 2: Khởi động trực tiếp
```bash
python main.py
```

## 📱 Sử dụng Bot

### Telegram Commands:
- `/news` - Lấy tin tức hôm nay
- `/news 21-04-2025` - Lấy tin tức ngày cụ thể

### Email:
Bot sẽ tự động gửi email vào:
- 13:15 hàng ngày
- 20:00 hàng ngày

## 🔧 Cấu hình

### Environment Variables:
```bash
TELEGRAM_BOT_TOKEN=your_bot_token
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient@email.com
VIETCAPITAL_EMAILS=email1@domain.com,email2@domain.com
```

### Cấu hình trong code:
Chỉnh sửa các biến trong `main.py`:
```python
TELEGRAM_BOT_TOKEN = "your_bot_token"
EMAIL_SENDER = "your_email@gmail.com"
EMAIL_PASSWORD = "your_app_password"
EMAIL_RECIPIENT = "recipient@email.com"
```

## 🐛 Xử lý lỗi

### Lỗi "conflict: terminated by other get updates request":
- Bot đã được cải tiến để xử lý lỗi này
- Sử dụng `start_bot.py` để khởi động an toàn
- Bot sẽ tự động dọn dẹp các instance cũ

### Lỗi kết nối:
- Kiểm tra internet connection
- Kiểm tra Telegram Bot Token
- Kiểm tra Gmail App Password

## 📊 Monitoring

### Web Endpoints:
- `http://localhost:8000/` - Trang chủ
- `http://localhost:8000/ping` - Health check
- `http://localhost:8000/health` - Status

### Logs:
Bot sẽ hiển thị logs chi tiết trong console:
- ✅ Thành công
- ❌ Lỗi
- 🔄 Đang xử lý
- ⏰ Lập lịch

## 🔄 Tự động khởi động lại

Bot có thể được cấu hình để tự động khởi động lại khi gặp lỗi:

```bash
# Sử dụng PM2 (Node.js)
npm install -g pm2
pm2 start main.py --name stock-news-bot --interpreter python

# Sử dụng systemd (Linux)
sudo systemctl enable stock-news-bot
sudo systemctl start stock-news-bot
```

## 📝 Changelog

### v2.0.0
- ✅ Sửa lỗi "conflict: terminated by other get updates request"
- ✅ Thêm signal handling
- ✅ Cải thiện error handling
- ✅ Thêm script khởi động an toàn
- ✅ Cập nhật dependencies

### v1.0.0
- ✅ Bot Telegram cơ bản
- ✅ Thu thập tin tức từ Cafef
- ✅ Gửi email tự động

## 🤝 Đóng góp

1. Fork repository
2. Tạo feature branch
3. Commit changes
4. Push to branch
5. Tạo Pull Request

## 📄 License

MIT License - xem file LICENSE để biết thêm chi tiết.

## 📞 Hỗ trợ

Nếu gặp vấn đề, vui lòng:
1. Kiểm tra logs
2. Đọc phần Troubleshooting
3. Tạo issue trên GitHub

---

**Lưu ý:** Bot này chỉ dành cho mục đích giáo dục và nghiên cứu. Vui lòng tuân thủ các quy định về sử dụng API và web scraping. 
