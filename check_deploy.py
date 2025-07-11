#!/usr/bin/env python3
"""
Script kiểm tra cấu hình trước khi deploy
"""

import os
import sys
from pathlib import Path

def check_files():
    """Kiểm tra các file cần thiết cho deployment"""
    print("🔍 Kiểm tra files cần thiết...")
    
    required_files = [
        "main.py",
        "requirements.txt", 
        "Procfile",
        "runtime.txt",
        ".gitignore",
        "render.yaml"
    ]
    
    missing_files = []
    for file in required_files:
        if not Path(file).exists():
            missing_files.append(file)
        else:
            print(f"✅ {file}")
    
    if missing_files:
        print(f"❌ Thiếu files: {', '.join(missing_files)}")
        return False
    else:
        print("✅ Tất cả files cần thiết đã có")
        return True

def check_requirements():
    """Kiểm tra file requirements.txt"""
    print("\n📦 Kiểm tra requirements.txt...")
    
    try:
        with open("requirements.txt", "r") as f:
            content = f.read()
            lines = content.strip().split("\n")
            
        print(f"✅ Có {len(lines)} dependencies:")
        for line in lines:
            if line.strip() and not line.startswith("#"):
                print(f"  - {line.strip()}")
        
        return True
    except FileNotFoundError:
        print("❌ Không tìm thấy requirements.txt")
        return False

def check_procfile():
    """Kiểm tra file Procfile"""
    print("\n⚙️ Kiểm tra Procfile...")
    
    try:
        with open("Procfile", "r") as f:
            content = f.read().strip()
        
        if "web: python main.py" in content:
            print("✅ Procfile đúng cấu hình")
            return True
        else:
            print("❌ Procfile không đúng format")
            return False
    except FileNotFoundError:
        print("❌ Không tìm thấy Procfile")
        return False

def check_env_vars():
    """Kiểm tra environment variables"""
    print("\n🔐 Kiểm tra environment variables...")
    
    required_vars = [
        "TELEGRAM_BOT_TOKEN",
        "EMAIL_SENDER", 
        "EMAIL_PASSWORD",
        "EMAIL_RECIPIENT"
    ]
    
    missing_vars = []
    for var in required_vars:
        value = os.getenv(var)
        if not value or value in ["your_bot_token", "your_email@gmail.com", "your_app_password"]:
            missing_vars.append(var)
        else:
            print(f"✅ {var}: {'*' * len(value)}")
    
    if missing_vars:
        print(f"⚠️ Cần cấu hình: {', '.join(missing_vars)}")
        print("💡 Hãy thêm vào Environment Variables trên Render")
        return False
    else:
        print("✅ Tất cả environment variables đã cấu hình")
        return True

def main():
    """Hàm chính kiểm tra"""
    print("🚀 Kiểm tra cấu hình deployment...")
    print("=" * 50)
    
    # Kiểm tra files
    files_ok = check_files()
    
    # Kiểm tra requirements
    req_ok = check_requirements()
    
    # Kiểm tra Procfile
    proc_ok = check_procfile()
    
    # Kiểm tra env vars
    env_ok = check_env_vars()
    
    print("\n" + "=" * 50)
    print("📊 Kết quả kiểm tra:")
    print(f"Files: {'✅' if files_ok else '❌'}")
    print(f"Requirements: {'✅' if req_ok else '❌'}")
    print(f"Procfile: {'✅' if proc_ok else '❌'}")
    print(f"Environment: {'✅' if env_ok else '❌'}")
    
    if all([files_ok, req_ok, proc_ok]):
        print("\n🎉 Sẵn sàng deploy!")
        print("💡 Lưu ý: Environment variables sẽ được cấu hình trên Render")
    else:
        print("\n⚠️ Cần sửa lỗi trước khi deploy")

if __name__ == "__main__":
    main() 
