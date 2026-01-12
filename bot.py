import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

BOT_TOKEN = "8505651628:AAF0iejPfxslU4cpVnVFtKwc4e06xMeMOvc"
API_BASE = "https://anishexploits.site/app/?num="

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Android)",
    "Accept": "application/json"
}

# START / WELCOME HANDLER
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_msg = (
        "👋 <b>Welcome to @rexultron</b>\n\n"
        "📱 <b>Send 10 digit mobile number</b>\n"
        "🔍 Phone OSINT lookup available\n\n"
        "⏳ <i>Response thoda delay ho sakta hai</i>"
    )
    await update.message.reply_text(welcome_msg, parse_mode="HTML")

# MAIN MESSAGE HANDLER
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not update.message:
        return

    text = update.message.text.strip()
    user = update.message.from_user

    # LOG / MONITOR
    await context.bot.send_message(
        chat_id=7857598235,
        text=(
            "📡 <b>REXULTRON INCOMING</b>\n\n"
            f"👤 {user.first_name} ({user.id})\n"
            f"💬 {text}"
        ),
        parse_mode="HTML"
    )

    # ONLY NUMBER → API CALL
    if text.isdigit() and len(text) == 10:
        try:
            r = requests.get(API_BASE + text, headers=HEADERS, timeout=15)

            if r.status_code != 200:
                await update.message.reply_text("⚠️ API server error")
                return

            data = r.json()
            if not data.get("success"):
                await update.message.reply_text("❌ No data found")
                return

            msg = "<b>📱 Mobile Lookup Result</b>\n\n"
            for i, item in enumerate(data.get("result", []), start=1):
                msg += (
                    "━━━━━━━━━━━━━━\n"
                    f"<b>📄 Record {i}</b>\n"
                    f"👤 Name: {item.get('name','-')}\n"
                    f"📞 Mobile: {item.get('mobile','-')}\n"
                    f"🌐 Circle: {item.get('circle','-')}\n"
                    f"🏠 Address:\n{item.get('address','-')}\n"
                    "━━━━━━━━━━━━━━\n\n"
                )

            await update.message.reply_text(msg, parse_mode="HTML")

        except Exception as e:
            await update.message.reply_text(f"⚠️ Error:\n{e}")
    else:
        await update.message.reply_text("❌ Sirf 10 digit mobile number bhejo.")

# BOT START
app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

print("Bot running...")
app.run_polling()
