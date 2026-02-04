import logging
import random
import string
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ✅ BOT TOKEN from Railway Environment Variable
BOT_TOKEN = os.getenv("BOT_TOKEN")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Generate username
def generate_username():
    names = ['aarav', 'vivaan', 'aditya', 'arjun', 'sai', 'reyansh', 'dhruv', 'kabir',
             'krishna', 'rohan', 'ishaan', 'yash', 'aryan', 'dev', 'raj', 'prem',
             'anaya', 'diya', 'ira', 'anika', 'myra', 'sara', 'aaradhya', 'avni',
             'alex', 'max', 'leo', 'noah', 'liam', 'oliver', 'elijah', 'james',
             'william', 'benjamin', 'lucas', 'henry', 'alexander', 'sebastian']
    
    name = random.choice(names)
    name_part = name[:random.randint(4, 7)]
    numbers = str(random.randint(10, 999))
    letters = ''.join(random.choices(string.ascii_lowercase, k=2))
    
    return f"{name_part}{numbers}_{letters}"

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎯 GENERATE USERNAME", callback_data='generate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        "🤖 *Instagram Username Generator*\n\n"
        "Tap button to generate unique username:",
        parse_mode='Markdown',
        reply_markup=reply_markup
    )

# Button handler
async def generate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    username = generate_username()
    
    message = f"""
✅ *Indo created succesfully*

Username = `{username}`

━━━━━━━━━━━━
Password = `0plm0plm`
━━━━━━━━━━━━
"""
    
    keyboard = [
        [InlineKeyboardButton("🔄 GENERATE ANOTHER", callback_data='generate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

# Quick /gen command
async def quick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = generate_username()
    
    await update.message.reply_text(
        f"⚡ *Quick Generate*\n\n"
        f"```{username}```\n\n"
        f"📋 Tap & hold to copy",
        parse_mode='Markdown'
    )

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN not found! Set it in Railway Variables.")
        return

    app = Application.builder().token(BOT_TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("gen", quick_command))
    app.add_handler(CallbackQueryHandler(generate_handler, pattern='^generate$'))
    
    print("🤖 BOT RUNNING ON RAILWAY...")
    app.run_polling()

if __name__ == '__main__':
    main()
