import telebot
import os

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# Словник для збереження вже відомих учасників {chat_id: set(user_id)}
known_members = {}

def update_known_members(chat_id):
    """Оновлює список учасників у групі"""
    try:
        members = bot.get_chat_administrators(chat_id)  # беремо адміністраторів
        # І додаємо всіх інших учасників через get_chat_member_count та get_chat_member
        count = bot.get_chat(chat_id).get('members_count', 0)
        # Для простоти – зберігаємо лише адміністративний список, інші учасники додаються при події
        known_members[chat_id] = set(admin.user.id for admin in members)
    except Exception as e:
        print(f"Помилка оновлення учасників: {e}")

# 🖐️ Привітання нових учасників
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    chat_id = message.chat.id
    if chat_id not in known_members:
        known_members[chat_id] = set()

    for new_member in message.new_chat_members:
        if new_member.id not in known_members[chat_id]:
            mention = f"@{new_member.username}" if new_member.username else new_member.first_name
            text = (
                f"👋 Ласкаво просимо, {mention}!\n\n"
                f"Щоб було зручно, у нас усе поділено по гілках.\n"
                f"Ознайомся з інформацією 😉"
            )
            bot.send_message(chat_id, text)
            known_members[chat_id].add(new_member.id)

# 🔄 Запуск бота
print("✅ Бот запущений і працює 24/7...")
bot.polling(none_stop=True)
