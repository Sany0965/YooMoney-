import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from yoomoney import Quickpay, Client

# Токены и идентификаторы
TOKEN = ""  # Токен бота
YOOMONEY_TOKEN = ""  # Токен Yoomoney
RECEIVER = ""  # Ваш кошелек Yoomoney

bot = telebot.TeleBot(TOKEN)
payment_labels = {}  # Хранение платежных меток пользователей

@bot.message_handler(commands=["start"])
def start(message):
    keyboard = InlineKeyboardMarkup()
    pay_button = InlineKeyboardButton("💳 Оплатить", callback_data="pay")
    keyboard.add(pay_button)
    bot.send_message(message.chat.id, "Привет! Нажмите 'Оплатить', чтобы перейти к оплате.", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "pay")
def process_payment(call):
    user_id = call.message.chat.id
    label = f"user_{user_id}"  # Уникальный label для пользователя
    payment_labels[user_id] = label  # Запоминаем label

    quickpay = Quickpay(
        receiver=RECEIVER,
        quickpay_form="shop",
        targets="Оплата доступа",
        paymentType="SB",
        sum=150,  # Сумма платежа
        label=label
    )

    keyboard = InlineKeyboardMarkup()
    pay_url_button = InlineKeyboardButton("🔗 Перейти к оплате", url=quickpay.base_url)
    check_payment_button = InlineKeyboardButton("🔄 Проверить оплату", callback_data="check_payment")
    keyboard.add(pay_url_button, check_payment_button)

    bot.send_message(call.message.chat.id, "Перейдите по ссылке для оплаты:", reply_markup=keyboard)

@bot.callback_query_handler(func=lambda call: call.data == "check_payment")
def check_payment(call):
    user_id = call.message.chat.id
    label = payment_labels.get(user_id)

    if not label:
        bot.answer_callback_query(call.id, "❌ Оплата не найдена.", show_alert=True)
        return

    client = Client(YOOMONEY_TOKEN)
    history = client.operation_history(label=label)

    for operation in history.operations:
        if operation.status == "success":
            bot.send_message(call.message.chat.id, "✅ Спасибо за оплату!")
            bot.delete_message(call.message.chat.id, call.message.message_id)  # Удаляем сообщение
            del payment_labels[user_id]  # Удаляем запись после успешной оплаты
            return

    bot.answer_callback_query(call.id, "❌ Оплата не найдена. Попробуйте позже.", show_alert=True)

if __name__ == "__main__":
    bot.polling(none_stop=True)