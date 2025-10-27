import telebot
import os

# 🔑 Токен зберігається у середовищі (Render його зчитує автоматично)
TOKEN = os.environ.get("8446399579:AAHFrcm5miiclLxH7BTfU_qbaGGAn2Vp_B4")

bot = telebot.TeleBot(TOKEN)

# 🖐️ Обробка входу нових учасників у групу
@bot.message_handler(content_types=['new_chat_members'])
def greet_new_member(message):
    for new_member in message.new_chat_members:
        mention = f"@{new_member.username}" if new_member.username else new_member.first_name
        text = (
            f"👋 Ласкаво просимо, {mention}!\n\n"
            f"Щоб було зручно, у нас усе поділено по гілках.\n"
            f"Ознайомся з інформацією 😉"
        )
        bot.send_message(message.chat.id, text)

print("✅ Бот запущений і працює 24/7...")
bot.polling(none_stop=True)
