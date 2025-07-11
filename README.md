# Stock News Bot

Bot Telegram tự động thu thập và gửi tin tức chứng khoán Việt Nam.

## Yêu cầu hệ thống

- **Python**: 3.11.x (khuyến nghị Python 3.11.10)
- **Hệ điều hành**: Windows, macOS, Linux
- **RAM**: Tối thiểu 512MB
- **Dung lượng**: Tối thiểu 100MB

## Cài đặt Python 3.11

### Windows
1. Tải Python 3.11.10 từ [python.org](https://www.python.org/downloads/release/python-31110/)
2. Chạy installer và đảm bảo tích "Add Python to PATH"
3. Kiểm tra: `python --version`

### macOS
```bash
# Sử dụng Homebrew
brew install python@3.11

# Hoặc tải từ python.org
```

### Linux (Ubuntu/Debian)
```bash
sudo apt update
sudo apt install python3.11 python3.11-pip
```

### Kiểm tra phiên bản
```bash
python --version
# Hoặc
python3.11 --version
```

## Cài đặt và chạy

### 1. Clone repository
```bash
git clone <your-repository-url>
cd <repository-name>
```

### 2. Cài đặt dependencies
```bash
pip install -r requirements.txt
```

### 3. Cấu hình biến môi trường
Tạo file `.env` hoặc set environment variables:
```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export EMAIL_SENDER="your_email@gmail.com"
export EMAIL_PASSWORD="your_app_password"
export EMAIL_RECIPIENT="recipient@email.com"
export VIETCAPITAL_EMAILS="tu.nguyen@vietcapital.com.vn,ngoc.truong@vietcapital.com.vn,son.pham@vietcapital.com.vn,minh.tran@vietcapital.com.vn,tien.huynh@vietcapital.com.vn,tam.nguyen@vietcapital.com.vn,diem.ngo@vietcapital.com.vn,vy.phan@vietcapital.com.vn"
```

### 4. Chạy bot
```bash
python main.py
```

## Tính năng

- Tự động thu thập tin tức chứng khoán từ các nguồn tin tức
- Gửi tin tức qua Telegram và email
- Lập lịch tự động gửi tin tức vào 10:45 và 20:00 hàng ngày
- Hỗ trợ tìm kiếm tin tức theo ngày cụ thể

## Deploy lên Render

### Bước 1: Chuẩn bị

1. Đảm bảo code đã được push lên GitHub
2. Có tài khoản Render (miễn phí)

### Bước 2: Tạo service trên Render

1. Đăng nhập vào [Render](https://render.com)
2. Click "New +" → "Web Service"
3. Connect với GitHub repository
4. Cấu hình:
   - **Name**: stock-news-bot
   - **Environment**: Python
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `python main.py`

### Bước 3: Cấu hình Environment Variables

Trong Render dashboard, thêm các biến môi trường:

- `TELEGRAM_BOT_TOKEN`: Token của Telegram bot
- `EMAIL_SENDER`: Email gửi (Gmail)
- `EMAIL_PASSWORD`: Mật khẩu ứng dụng Gmail
- `EMAIL_RECIPIENT`: Email nhận chính
- `VIETCAPITAL_EMAILS`: Danh sách email VietCapital (phân cách bằng dấu phẩy)

### Bước 4: Deploy

1. Click "Create Web Service"
2. Render sẽ tự động build và deploy
3. Bot sẽ chạy 24/7 trên Render

## Cấu hình Gmail

Để sử dụng Gmail, bạn cần:

1. Bật "2-Step Verification"
2. Tạo "App Password"
3. Sử dụng App Password thay vì mật khẩu thường

## Sử dụng

- `/news` - Lấy tin tức hôm nay
- `/news dd-mm-yyyy` - Lấy tin tức theo ngày cụ thể

## Lưu ý

- Render free tier có thể sleep sau 15 phút không hoạt động
- Bot sẽ tự động ping server mỗi 15 phút để giữ hoạt động
- Bot sẽ tự động gửi tin tức vào 10:45 và 20:00 hàng ngày
- Đảm bảo các biến môi trường được cấu hình đúng

## Endpoints

- `/` - Trang chủ
- `/ping` - Kiểm tra bot có hoạt động không
- `/health` - Thông tin sức khỏe bot 
