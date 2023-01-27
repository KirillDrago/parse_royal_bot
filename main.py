import pandas as pd

from telethon import TelegramClient, events, functions
from telethon.errors import ChatAdminRequiredError
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty


API_ID = 21618626
API_HASH = "7372ff2bf3d7bd288213dd3df4465019"
PHONE = "PHONE"

BOT_TOKEN = "5804671397:AAHbQ3IkVe3O-tR8x4AG6GEnBc893ZkNo_U"
bot = TelegramClient(PHONE, API_ID, API_HASH).start()

bot.start(bot_token=BOT_TOKEN)


chats = []
last_date = None
size_chats = 1000
groups = []


@bot.on(events.NewMessage(pattern="/start"))
async def help_bot(event):
    await bot.send_message(
        event.chat_id, "Для поиска просто введите ключевое слово (например: Linux)\n"
                       "(Внимание: Бот не может считать участников с закрытого чата или если список участников скрыт)"
    )


@bot.on(events.NewMessage(pattern="/file"))
async def get_file(event):
    try:
        await bot.send_file(event.chat_id, "table.html")
    except ValueError:
        await bot.send_message(event.chat_id, "Файл еще не создан, что бы создать файл введите /start")


# @bot.on(events.NewMessage(pattern="/me")) # функция для парсинга чатов пользователя
# async def parse(event):
#     global groups
#
#     result = await bot(GetDialogsRequest(
#         offset_date=last_date,
#         offset_id=0,
#         offset_peer=InputPeerEmpty(),
#         limit=size_chats,
#         hash=0
#     ))
#
#     chats.extend(result.chats)
#
#     for chat in chats:
#         try:
#             groups.append(chat)
#         except:
#             continue
#
#     i = 0
#     res = ""
#     for group in groups:
#         text = f"{i} - {group.title} id: {group.id}"
#         i += 1
#         res += text + "\n"
#     await bot.send_message(event.chat_id, f"{res}")
#     await bot.send_message(event.chat_id, "Введите номер чата, который нужно считать")


@bot.on(events.NewMessage)
async def peoples(event):

    message = event.message
    text = message.text
    if len(text) <= 3:
        target_group = groups[int(text)]

        print('Узнаём пользователей...')
        try:
            all_participants = bot.get_participants(target_group)
        except ChatAdminRequiredError:
            await bot.send_message(event.chat_id, "Нет доступа к списку учаcтников")
        except ValueError:
            print("Wait please...")
        except RuntimeError:
            print("Wait please...")
        else:
            print('Сохраняем данные в файл...')

            usernames = []
            names = []
            target_groups = []
            await bot.send_message(event.chat_id, "Узнаём пользователей...")
            try:
                for user in await all_participants:
                    if user.username:
                        username = user.username
                    else:
                        username = ""
                    if user.first_name:
                        first_name = user.first_name
                    else:
                        first_name = ""
                    if user.last_name:
                        last_name = user.last_name
                    else:
                        last_name = ""
                    name = (first_name + ' ' + last_name).strip()
                    usernames.append(username)
                    names.append(name)
                    target_groups.append(target_group.title)

                    data = {'username': usernames,
                            'name': names,
                            'target_group': target_groups}
                    df = pd.DataFrame(data)

                    html_table = df.to_html()

                    with open('table.html', 'w', encoding='UTF-8') as f:
                        f.write(html_table)
                print('Парсинг участников группы успешно выполнен.')
                await event.respond("Файл создан, что бы его получить - введите /file")
            except ValueError:
                await bot.send_message(event.chat_id, "Нет доступа к списку учаcтников, попробуйте другой чат(val)")
            except ChatAdminRequiredError:
                await bot.send_message(event.chat_id, "Нет доступа к списку учаcтников, попробуйте другой чат")


@bot.on(events.NewMessage)
async def search(event):
    message = event.message
    text = message.text
    global chats
    chats = []
    if "/" not in text and not text.isdigit():
        result = await bot(functions.contacts.SearchRequest(
            q=text,
            limit=1000
        ))

        chats.extend(result.chats)
        global groups
        groups = []
        for chat in chats:
            try:
                groups.append(chat)
            except:
                continue

        i = 0
        res = ""
        for group in groups:
            text = f"{i} - {group.title} id: {group.id}"
            i += 1
            res += text + "\n"
        await bot.send_message(event.chat_id, f"{res}")
        await bot.send_message(event.chat_id, "Введите номер чата, который нужно считать")


def main():
    bot.run_until_disconnected()


if __name__ == '__main__':
    main()
