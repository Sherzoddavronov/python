import logging
from telegram import Update, KeyboardButton, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Logging tizimini sozlash
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Foydalanuvchilar ma'lumotlarini saqlash uchun ro'yxat
users_data = []

# /start buyrug'i
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [[KeyboardButton("📲 Kontaktni ulashish", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, one_time_keyboard=True)
    
    await update.message.reply_text("Assalomu alaykum! Iltimos, kontakt ma'lumotlaringizni ulashing:", reply_markup=reply_markup)

# Kontaktni qabul qilish
async def handle_contact(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    user_info = {
        'user_id': contact.user_id,
        'user_name': update.message.from_user.username,
        'phone_number': contact.phone_number
    }
    users_data.append(user_info)
    await update.message.reply_text("Rahmat, kontakt ma'lumotlaringiz qabul qilindi! 4-kundan keyin g'liblar aniqlanadi sizga (SABR)\n HOZIRDA UzTelecomda 20GB ==78,000== SO'MNI TASHKIL ETADI\n HOZIRDA BELINEDA 20GB ==98,400== SO'MNI TASHKIL ETADI\n HOZIRDA MOBIUZDA 20GB==65,000== SO'MNI TASHKIL ETADI")

# Maxsus "users" buyrug'i uchun funksiya
async def show_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.args and context.args[0] == "507032249":
        if users_data:
            users_info = "\n".join([f"Username: {user['user_name']}, ID: {user['user_id']}, Telefon: {user['phone_number']}" for user in users_data])
            await update.message.reply_text(f"Foydalanuvchilar:\n{users_info}")
        else:
            await update.message.reply_text("Hozircha foydalanuvchilar ro'yxati bo'sh.")
    else:
        await update.message.reply_text("Noto'g'ri parol.")

# Xatolarni log qilish
async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    logger.warning(f'Update "{update}" caused error "{context.error}"')

# Asosiy kod
if __name__ == '__main__':
    # Bot tokenini kiriting
    TOKEN = '6518197119:AAH8IQZ7wul_iY9gT-JnNcnzy0uo1xp33tc'

    # Botni yaratish
    application = ApplicationBuilder().token(TOKEN).build()

    # Handlerlarni qo'shish
    application.add_handler(CommandHandler('start', start))
    application.add_handler(MessageHandler(filters.CONTACT, handle_contact))
    application.add_handler(CommandHandler('users', show_users))

    # Xatolarni log qilish
    application.add_error_handler(error)

    # Botni ishga tushirish
    application.run_polling()
