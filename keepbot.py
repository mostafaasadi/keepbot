import random
import gkeepapi
from telegram.ext import Updater, MessageHandler, Filters

# Config
telegramtoken = 'AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA'
GAppUser = 'Google username'
GAppPass = 'App password'
admins = [55555555]  # id in telegram


# Telegram API
# access  bot via token
updater = Updater(token=telegramtoken)
dispatcher = updater.dispatcher

keep = gkeepapi.Keep()
try:
    keep.login(GAppUser, GAppPass)
except Exception as e:
    print(e)

colors = ['White', 'Red', 'Orange', 'Yellow', 'Green', 'Teal', 'Blue', 'DarkBlue', 'Purple', 'Pink', 'Brown', 'Gray']


def text(bot, update):
    if update.message.from_user.id in admins:
        try:
            note = keep.createNote()
            c = random.choice(colors)
            note.text = update.message.text
            label = keep.findLabel('Telegram')
            note.labels.add(label)
            note.color = gkeepapi.node.ColorValue[c]
            keep.sync()
            status = True
        except Exception as e:
            print(e)
            status = False
        if status:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                text='✅'
            )
        else:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                text='⚠️ ' + e
            )
    else:
        try:
            author = update.message.from_user.first_name + " " \
                + update.message.from_user.last_name
            un = str(update.message.from_user.username)
        except Exception as e:
            print(e)
            author = 'Unname'
            un = 'Anonymous user'
        finally:
            bot.sendMessage(
                chat_id=update.message.chat_id,
                reply_to_message_id=update.message.message_id,
                text='⚠️ 😡 شما حق پیام دادن به من را ندارید \n من پیام شما را به اربابم نشان می‌دهم'
            )

            res = '⚠️ غریبه‌ای به من پیام داده \n👤 ' + author + '  ' + un \
                + '\n    ' + update.message.text
            bot.sendMessage(
                chat_id=admins[0],
                text=res
            )


def main():
    # handle dispatcher
    dispatcher.add_handler(MessageHandler(Filters.text, text))

    # run
    updater.start_polling()
    updater.idle()


if __name__ == '__main__':
    main()
