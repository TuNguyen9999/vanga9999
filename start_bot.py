#!/usr/bin/env python3
"""
Script khởi động an toàn cho Stock News Bot
Tuân thủ chuẩn PTB 20.7
"""

import os
import sys
import subprocess
import time
import signal
from pathlib import Path

def check_dependencies():
    """Kiểm tra và cài đặt dependencies."""
    try:
        import telegram
        import httpx
        import bs4
        import schedule
        import flask
        import requests
        print("✅ Tất cả dependencies đã được cài đặt")
        return True
    except ImportError as e:
        print(f"❌ Thiếu dependency: {e}")
        print("🔄 Đang cài đặt dependencies...")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
            print("✅ Đã cài đặt dependencies thành công")
            return True
        except subprocess.CalledProcessError:
            print("❌ Không thể cài đặt dependencies")
            return False

def kill_existing_processes():
    """Tắt các process bot đang chạy."""
    try:
        # Tìm và tắt các process Python đang chạy main.py
        result = subprocess.run(
            ["tasklist", "/FI", "IMAGENAME eq python.exe", "/FO", "CSV"],
            capture_output=True, text=True, shell=True
        )
        
        if "main.py" in result.stdout:
            print("🔄 Đang tắt các instance bot cũ...")
            subprocess.run(
                ["taskkill", "/F", "/IM", "python.exe"],
                shell=True
            )
            time.sleep(2)  # Chờ process tắt hoàn toàn
    except Exception as e:
        print(f"⚠️ Không thể tắt process cũ: {e}")

def start_bot():
    """Khởi động bot với error handling."""
    print("🚀 Khởi động Stock News Bot...")
    
    # Kiểm tra file main.py
    if not Path("main.py").exists():
        print("❌ Không tìm thấy file main.py")
        return False
    
    # Tắt các process cũ
    kill_existing_processes()
    
    # Kiểm tra dependencies
    if not check_dependencies():
        return False
    
    try:
        # Khởi động bot
        subprocess.run([sys.executable, "main.py"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Lỗi khi khởi động bot: {e}")
        return False
    except KeyboardInterrupt:
        print("\n🛑 Bot được tắt bởi người dùng")
        return True

def main():
    """Hàm chính."""
    print("🤖 Stock News Bot - Script Khởi động")
    print("=" * 50)
    
    # Kiểm tra Python version
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        return
    
    # Khởi động bot
    success = start_bot()
    
    if not success:
        print("❌ Không thể khởi động bot")
        sys.exit(1)
    else:
        print("✅ Bot đã được tắt an toàn")

if __name__ == "__main__":
    main() 