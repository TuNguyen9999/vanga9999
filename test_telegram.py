#!/usr/bin/env python3
"""
Script test kết nối Telegram bot
"""

import os
import sys
import requests
from telegram import Application
from telegram.ext import CommandHandler, MessageHandler, filters

# Import từ main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import news_command_handler, help_message_handler, TELEGRAM_BOT_TOKEN

async def test_telegram_connection():
    """Test kết nối Telegram API"""
    print("🔍 Đang test kết nối Telegram...")
    
    try:
        # Test 1: Kiểm tra token
        response = requests.get(f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get('ok'):
                print(f"✅ Token hợp lệ - Bot: @{bot_info['result']['username']}")
                print(f"📝 Bot name: {bot_info['result']['first_name']}")
                return True
            else:
                print(f"❌ Token không hợp lệ: {bot_info.get('description')}")
                return False
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Lỗi kết nối: {e}")
        return False

async def test_application():
    """Test tạo Application"""
    print("\n🔧 Đang test tạo Application...")
    
    try:
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        
        # Thêm handlers
        app.add_handler(CommandHandler("news", news_command_handler))
        app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, help_message_handler))
        
        print("✅ Application được tạo thành công")
        print("✅ Handlers được thêm thành công")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi tạo Application: {e}")
        import traceback
        traceback.print_exc()
        return False

async def main():
    """Hàm chính test"""
    print("🧪 Test Telegram Bot Connection")
    print("=" * 40)
    
    # Test 1: Kết nối API
    api_ok = await test_telegram_connection()
    
    if api_ok:
        # Test 2: Tạo Application
        app_ok = await test_application()
        
        if app_ok:
            print("\n🎉 Tất cả tests thành công!")
            print("✅ Bot sẵn sàng deploy")
        else:
            print("\n❌ Lỗi tạo Application")
    else:
        print("\n❌ Lỗi kết nối Telegram API")
        print("💡 Kiểm tra lại TELEGRAM_BOT_TOKEN")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main()) 
