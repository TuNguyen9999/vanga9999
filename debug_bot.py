#!/usr/bin/env python3
"""
Script debug cho Stock News Bot
Tuân thủ chuẩn PTB 20.7
"""

import os
import sys
import subprocess
import time
import requests
from pathlib import Path

def check_python_version():
    """Kiểm tra phiên bản Python."""
    if sys.version_info < (3, 8):
        print("❌ Cần Python 3.8 trở lên")
        return False
    print(f"✅ Python version: {sys.version}")
    return True

def check_dependencies():
    """Kiểm tra dependencies."""
    required_packages = [
        "telegram",
        "httpx", 
        "beautifulsoup4",
        "schedule",
        "flask",
        "requests"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - CHƯA CÀI ĐẶT")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n🔄 Đang cài đặt packages thiếu: {', '.join(missing_packages)}")
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + missing_packages)
            print("✅ Đã cài đặt packages thành công")
            return True
        except subprocess.CalledProcessError:
            print("❌ Không thể cài đặt packages")
            return False
    
    return True

def check_telegram_token():
    """Kiểm tra Telegram Bot Token."""
    token = os.getenv("TELEGRAM_BOT_TOKEN", "7200591128:AAFtBUbfLpp-OoI9II9hQArMTZFwelTT6_Y")
    
    if not token or token == "your_bot_token":
        print("❌ TELEGRAM_BOT_TOKEN chưa được cấu hình")
        return False
    
    try:
        response = requests.get(f"https://api.telegram.org/bot{token}/getMe", timeout=10)
        if response.status_code == 200:
            bot_info = response.json()
            if bot_info.get("ok"):
                print(f"✅ Telegram Bot: {bot_info['result']['first_name']} (@{bot_info['result']['username']})")
                return True
            else:
                print(f"❌ Lỗi Telegram API: {bot_info.get('description', 'Unknown error')}")
                return False
        else:
            print(f"❌ Lỗi HTTP: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Không thể kết nối Telegram API: {e}")
        return False

def check_network_connection():
    """Kiểm tra kết nối mạng."""
    test_urls = [
        "https://api.telegram.org",
        "https://cafef.vn",
        "https://vietnambiz.vn",
        "https://www.tinnhanhchungkhoan.vn"
    ]
    
    print("🌐 Kiểm tra kết nối mạng...")
    for url in test_urls:
        try:
            response = requests.get(url, timeout=5)
            print(f"✅ {url} - {response.status_code}")
        except Exception as e:
            print(f"❌ {url} - {e}")
            return False
    
    return True

def check_file_structure():
    """Kiểm tra cấu trúc file."""
    required_files = [
        "main.py",
        "requirements.txt",
        "start_bot.py"
    ]
    
    print("📁 Kiểm tra cấu trúc file...")
    for file in required_files:
        if Path(file).exists():
            print(f"✅ {file}")
        else:
            print(f"❌ {file} - KHÔNG TỒN TẠI")
            return False
    
    return True

def test_bot_startup():
    """Test khởi động bot."""
    print("🤖 Test khởi động bot...")
    try:
        # Import main module
        import main
        print("✅ Import main.py thành công")
        
        # Test các hàm chính
        if hasattr(main, 'check_telegram_connection'):
            print("✅ Hàm check_telegram_connection tồn tại")
        
        if hasattr(main, 'cleanup_old_instances'):
            print("✅ Hàm cleanup_old_instances tồn tại")
        
        return True
    except Exception as e:
        print(f"❌ Lỗi khi test bot: {e}")
        return False

def main():
    """Hàm chính debug."""
    print("🔍 Stock News Bot - Debug Tool")
    print("=" * 50)
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("File Structure", check_file_structure),
        ("Network Connection", check_network_connection),
        ("Telegram Token", check_telegram_token),
        ("Bot Startup", test_bot_startup)
    ]
    
    results = []
    for check_name, check_func in checks:
        print(f"\n🔍 {check_name}:")
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"❌ Lỗi trong {check_name}: {e}")
            results.append((check_name, False))
    
    # Tổng kết
    print("\n" + "=" * 50)
    print("📊 KẾT QUẢ DEBUG:")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for check_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {check_name}")
    
    print(f"\n🎯 Tổng kết: {passed}/{total} checks passed")
    
    if passed == total:
        print("🎉 Tất cả checks đều thành công! Bot sẵn sàng chạy.")
        print("\n🚀 Để khởi động bot:")
        print("   python start_bot.py")
    else:
        print("⚠️ Có một số vấn đề cần khắc phục trước khi chạy bot.")
        print("\n💡 Gợi ý:")
        print("   1. Kiểm tra internet connection")
        print("   2. Cài đặt lại dependencies: pip install -r requirements.txt")
        print("   3. Kiểm tra Telegram Bot Token")
        print("   4. Chạy lại debug: python debug_bot.py")

if __name__ == "__main__":
    main() 