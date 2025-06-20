from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, ContextTypes, filters

# 🔑 Token bot bạn lấy từ BotFather
TELEGRAM_TOKEN = "7200591128:AAFtBUbfLpp-OoI9II9hQArMTZFwelTT6_Y"

# 📊 Nội dung trả về khi người dùng nhắn "phân tích cổ phiếu HAH"
analysis_text = """
🔍 Phân Tích Cổ Phiếu HAH:

- Giá hiện tại đang test kháng cự 77,905 VND (Fibo 23.6%).
- Hỗ trợ mạnh tại vùng 70,422 - 73,300 VND (MA20 + Fibo 38.2%).
- Khối lượng ngắn hạn giảm → có thể điều chỉnh, nhưng dài hạn vẫn tích cực.
- Đặt cắt lỗ dưới 69,000 VND. Mục tiêu: 84,000 - 90,000 VND.

⚠️ Đây không phải khuyến nghị đầu tư. Hãy cân nhắc rủi ro!
"""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_message = update.message.text.lower()

    if "phân tích cổ phiếu hah" in user_message:
        await update.message.reply_text(analysis_text)
    else:
        await update.message.reply_text("❓ Gõ: 'phân tích cổ phiếu HAH' để nhận thông tin.")

if __name__ == "__main__":
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("🤖 Bot đang chạy... Gõ 'phân tích cổ phiếu HAH' trên Telegram để kiểm tra.")
    app.run_polling()
