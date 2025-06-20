from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "YOUR_BOT_TOKEN_HERE"  # <-- THAY TOKEN TẠI ĐÂY

# Nội dung phản hồi khi người dùng gửi "phân tích cổ phiếu HAH"
ANALYSIS_TEXT = """
Phân Tích Cổ Phiếu HAH (Cập nhật 06-06-2025)
🔍 Xu Hướng Giá
- Ngắn hạn (<20 phiên): Điều chỉnh nhẹ (MA5 < MA10) nhưng vẫn trên MA20 hỗ trợ (73,793 VND). Giá hiện tại (76,000 VND) đang test kháng cự 77,905 VND (Fibonacci 23.6%).  
- Trung hạn (20-50 phiên): Tăng mạnh (MA20 > MA50 > MA100) với đà tăng +38% từ MA50.  
- Dài hạn (>50 phiên): Xu hướng tăng vững (MA200 = 50,934 VND → giá hiện tại cao hơn +49%).  
... (rút gọn vì quá dài) ...
💎 Kết Luận  
Các vùng 70,422 VND (hỗ trợ) và 77,905 VND (kháng cự) là mốc then chốt để xác định xu hướng ngắn hạn. Luôn kiểm tra:  
1️⃣ Khối lượng tại điểm phá vỡ/hồi về,  
2️⃣ Mức độ giữ vững của MA20,  
3️⃣ Tín hiệu phân kỳ rủi ro với thị trường chung.  
"""

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Xin chào! Gõ 'phân tích cổ phiếu HAH' để nhận báo cáo.")

async def reply_hah(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if "phân tích cổ phiếu HAH" in update.message.text.lower():
        await update.message.reply_text(ANALYSIS_TEXT[:4000])  # Telegram giới hạn 4096 ký tự

if __name__ == '__main__':
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("hah", reply_hah))
    app.add_handler(CommandHandler("phan_tich", reply_hah))
    app.add_handler(CommandHandler("pt", reply_hah))

    from telegram.ext import MessageHandler, filters
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, reply_hah))

    print("Bot is running...")
    app.run_polling()