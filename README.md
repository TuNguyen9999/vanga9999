# Stock News Bot 🤖

Bot tự động thu thập và gửi tin tức chứng khoán qua Telegram và Email.

## Tính năng

- 🔍 Tự động crawl tin tức từ các trang tài chính Việt Nam
- 📧 Gửi email tự động vào 12:00 và 20:00 hàng ngày
- 💬 Bot Telegram để tra cứu tin tức theo ngày
- ⏰ Chạy 24/7 trên cloud server

## Cấu hình

### Biến môi trường cần thiết:

```bash
TELEGRAM_BOT_TOKEN=your_bot_token_here
EMAIL_SENDER=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
EMAIL_RECIPIENT=recipient_email@gmail.com
VIETCAPITAL_EMAILS=email1@domain.com,email2@domain.com
```

## Deploy lên Render

1. **Tạo tài khoản Render**: Đăng ký tại [render.com](https://render.com)

2. **Tạo Web Service**:
   - Connect với GitHub repository
   - Chọn Python runtime
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `python main.py`

3. **Cấu hình Environment Variables**:
   - Thêm tất cả biến môi trường cần thiết
   - Đặc biệt là `TELEGRAM_BOT_TOKEN` và email credentials

4. **Deploy**:
   - Click "Create Web Service"
   - Render sẽ tự động deploy và chạy bot

## Lịch trình tự động

- ⏰ **12:00**: Gửi tin tức buổi trưa
- ⏰ **20:00**: Gửi tin tức buổi tối
- 🔄 **Ping server**: Mỗi 15 phút để giữ hoạt động

## Sử dụng

### Telegram Bot Commands:
- `/news` - Lấy tin tức hôm nay
- `/news 21-04-2025` - Lấy tin tức theo ngày cụ thể

### Email:
Bot sẽ tự động gửi email HTML đẹp mắt với:
- 📈 Mã cổ phiếu được đề cập
- 📄 Tiêu đề bài viết
- 🔗 Link đọc thêm

## Các trang web được crawl

- cafef.vn
- vietnambiz.vn  
- tinnhanhchungkhoan.vn

## Hỗ trợ

Nếu có vấn đề, hãy kiểm tra:
1. Token Telegram Bot có hợp lệ không
2. Email credentials có đúng không
3. Logs trong Render dashboard 
