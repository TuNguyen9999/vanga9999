#!/usr/bin/env python3
"""
Script test để kiểm tra bot trước khi deploy
"""

import asyncio
import os
import sys
from datetime import datetime

# Thêm thư mục hiện tại vào Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from main import fetch_news, format_news_for_email, send_email

async def test_fetch_news():
    """Test hàm fetch_news"""
    print("🔍 Đang test fetch_news...")
    
    # Test với ngày hôm nay
    news_data = await fetch_news()
    
    if news_data:
        print(f"✅ Tìm thấy {len(news_data)} bài viết")
        for i, item in enumerate(news_data[:3]):  # Chỉ hiển thị 3 bài đầu
            print(f"  {i+1}. {item['Mã cổ phiếu']}: {item['Tiêu đề'][:50]}...")
    else:
        print("❌ Không tìm thấy tin tức nào")
    
    return news_data

def test_email_format(news_data):
    """Test định dạng email"""
    print("📧 Đang test định dạng email...")
    
    if not news_data:
        print("❌ Không có dữ liệu để test")
        return
    
    display_date = datetime.now().strftime('%d/%m/%Y')
    html_content = format_news_for_email(news_data[:3], display_date)
    
    print("✅ Định dạng email thành công")
    print(f"📏 Độ dài HTML: {len(html_content)} ký tự")
    
    return html_content

def test_email_send(html_content):
    """Test gửi email (chỉ test kết nối)"""
    print("📤 Đang test kết nối email...")
    
    # Kiểm tra credentials
    email_sender = os.getenv("EMAIL_SENDER", "vcamnews@gmail.com")
    email_password = os.getenv("EMAIL_PASSWORD", "dsel ocad nqqj hdxy")
    email_recipient = os.getenv("EMAIL_RECIPIENT", "tunguyen3214@gmail.com")
    
    if email_sender == "your_email@gmail.com" or email_password == "your_app_password":
        print("⚠️ Email credentials chưa được cấu hình đầy đủ")
        return False
    
    try:
        # Test với nội dung đơn giản
        success, message = send_email(
            "Test Email - Stock News Bot",
            "<h1>Test Email</h1><p>Đây là email test từ bot.</p>",
            email_sender,
            [email_recipient],
            email_password
        )
        
        if success:
            print("✅ Kết nối email thành công")
        else:
            print(f"❌ Lỗi email: {message}")
        
        return success
    except Exception as e:
        print(f"❌ Lỗi test email: {e}")
        return False

async def main():
    """Hàm chính test"""
    print("🧪 Bắt đầu test bot...")
    print(f"⏰ Thời gian: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 50)
    
    # Test 1: Fetch news
    news_data = await test_fetch_news()
    print()
    
    # Test 2: Email format
    if news_data:
        html_content = test_email_format(news_data)
        print()
        
        # Test 3: Email send
        test_email_send(html_content)
    
    print("-" * 50)
    print("✅ Test hoàn thành!")

if __name__ == "__main__":
    asyncio.run(main()) 