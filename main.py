import os
import logging
import random
import string
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# Railway से environment variable से token लें
BOT_TOKEN = os.environ.get("BOT_TOKEN", "YOUR_BOT_TOKEN_HERE")

# Setup logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

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

# Start command
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

# Generate username with MONOSPACE for easy copy
async def generate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    username = generate_username()
    
    # MONOSPACE TEXT - EASY TO COPY
    message = f"""
✅ *Indo created successfully*

Username = `{username}`

━━━━━━━━━━━━
Password = `0plm0plm`
━━━━━━━━━━━━
"""
    
    # Button to show username in popup
    keyboard = [
        [InlineKeyboardButton("🔄 GENERATE ANOTHER", callback_data='generate')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await query.message.reply_text(message, parse_mode='Markdown', reply_markup=reply_markup)

# Show username in popup
async def show_popup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    data = query.data
    
    if data.startswith('show_'):
        username = data.replace('show_', '')
        # Show in popup with copy instructions
        await query.answer(
            f"👤 USERNAME:\n\n"
            f"{username}\n\n"
            f"📋 Copy steps:\n"
            f"1. Long press here\n"
            f"2. Select 'Copy'\n"
            f"3. Or go back and copy from main message",
            show_alert=True
        )

# Quick generate command
async def quick_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    username = generate_username()
    
    # Direct monospace text
    await update.message.reply_text(
        f"⚡ *Quick Generate*\n\n"
        f"```{username}```\n\n"
        f"📋 *Tap & hold to copy*",
        parse_mode='Markdown'
    )

# Error handler
async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.error(f"Exception while handling an update: {context.error}")

# Main function
def main():
    if BOT_TOKEN == "YOUR_BOT_TOKEN_HERE":
        print("❌ ERROR: Set BOT_TOKEN as environment variable!")
        print("1. Go to Railway dashboard")
        print("2. Add BOT_TOKEN environment variable")
        print("3. Get token from @BotFather on Telegram")
        return
    
    try:
        app = Application.builder().token(BOT_TOKEN).build()
        
        # Handlers
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CommandHandler("gen", quick_command))
        app.add_handler(CallbackQueryHandler(generate_handler, pattern='^generate$'))
        app.add_handler(CallbackQueryHandler(show_popup, pattern='^show_'))
        
        # Error handler
        app.add_error_handler(error_handler)
        
        print("🤖 BOT STARTING...")
        print(f"✅ Token: {BOT_TOKEN[:10]}...")
        
        # Railway के लिए PORT variable check करें
        port = int(os.environ.get("PORT", 8080))
        
        # Use webhook for Railway
        if "RAILWAY_STATIC_URL" in os.environ:
            url = os.environ.get("RAILWAY_STATIC_URL")
            app.run_webhook(
                listen="0.0.0.0",
                port=port,
                url_path=BOT_TOKEN,
                webhook_url=f"{url}/{BOT_TOKEN}"
            )
        else:
            # Local polling for development
            print("🔄 Running in polling mode...")
            app.run_polling()
            
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        raise

if __name__ == '__main__':
    main()
