#!/usr/bin/env python3
"""
Script test đơn giản cho bot
"""

import os
import sys
import asyncio
from telegram import Application
from telegram.ext import CommandHandler

# Import từ main.py
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from main import TELEGRAM_BOT_TOKEN

async def test_bot():
    """Test bot đơn giản"""
    print("🧪 Test bot đơn giản...")
    
    try:
        # Tạo Application
        app = Application.builder().token(TELEGRAM_BOT_TOKEN).build()
        print("✅ Application tạo thành công")
        
        # Test handler đơn giản
        async def test_handler(update, context):
            await update.message.reply_text("Test thành công!")
        
        app.add_handler(CommandHandler("test", test_handler))
        print("✅ Handler thêm thành công")
        
        # Test polling ngắn
        print("🔄 Test polling (10 giây)...")
        await app.initialize()
        await app.start()
        
        # Chạy trong 10 giây
        await asyncio.sleep(10)
        
        await app.stop()
        await app.shutdown()
        
        print("✅ Test hoàn thành!")
        return True
        
    except Exception as e:
        print(f"❌ Lỗi: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    asyncio.run(test_bot()) 
