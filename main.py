import googletrans
from aiogram import Bot, Dispatcher, executor, types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from config import TOKEN, DIR_PATH, LOG_FILE_PATH
from datetime import datetime
from langs import LANGS
import os
import googletrans
bot = Bot(token=TOKEN)
dp = Dispatcher(bot=bot, storage=MemoryStorage())
t = googletrans.Translator()


def _(text, langcode):
    return t.translate(text, langcode, 'en').text


def translate(text, langcode):
    if langcode in LANGS:
        return LANGS[langcode]
    else:
        return LANGS['en']


def logging(log: str):
    with open(LOG_FILE_PATH, 'a+', encoding='utf-8') as file:
        file.write(log)


@dp.message_handler()
async def main_func(message: types.Message):
    lang = message.from_user.language_code
    if message.text.startswith('add: '):
        text = message.text.replace('add: ', '')
        path = DIR_PATH + str(message.from_user.id) + '.txt'
        if not os.path.isfile(path):
            with open(path, 'w', encoding='utf-8') as file:
                pass
        with open(path, 'a+', encoding='utf-8') as file:
            file.write(text + ',')
        logging(
            f'TASK_ADDED={text}, TIME: {datetime.now()}, USER: {message.from_user.first_name} {message.from_user.last_name}, USER_ID: {message.from_user.id}  \n')
        await message.answer(_('Adding sucessful', lang))

    elif message.text.startswith('delete: '):
        text = message.text.replace('delete: ', '')
        context = ''
        path = DIR_PATH + str(message.from_user.id) + '.txt'
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                context = file.read().split(',')
            if text in context:
                context.remove(text)
                finish_context = ''
                for i in context:
                    if i != '':
                        finish_context += f'{i},'
                    else:
                        continue
                with open(path, 'w', encoding='utf-8') as file:
                    file.write(finish_context)
                logging(
                    f'TASK_DELETED={message.text}, TIME: {datetime.now()}, USER: {message.from_user.first_name} {message.from_user.last_name}, USER_ID: {message.from_user.id}  \n')
                await message.answer(_('Deleting successful', lang))
            else:
                logging(
                    f'ERROR: NO_TASK={text}, TIME: {datetime.now()}, USER: {message.from_user.first_name} {message.from_user.last_name}, USER_ID: {message.from_user.id}  \n')
                await message.answer(_('You don`t have this task\n'
                                       'You can use command /all to see all tasks',
                                       lang))
        else:
            logging(
                f'ERROR: ANY_TASK, TIME: {datetime.now()}, USER: {message.from_user.first_name} {message.from_user.last_name}, USER_ID: {message.from_user.id}  \n')
            await message.answer('You don`t have any task')
    elif message.text == '/start':
        answer = translate(text="Choose what do you want to do:\n"
                                "1. Add task - add: <task>\n"
                                "2. Delete task - delete: <task>\n"
                                "3. See all - /all\n",
                           langcode=lang)
        await message.answer(answer)
    elif message.text == '/all':
        path = DIR_PATH + str(message.from_user.id) + '.txt'
        context = ''
        finish_context = ''
        if os.path.isfile(path):
            with open(path, 'r', encoding='utf-8') as file:
                context = file.read().split(',')
                if context:
                    for i in context:
                        finish_context += f'{i}\n'
                    if finish_context != '\n':
                        ansver = _('Your tasks:\n', lang)
                        await message.answer(f'{ansver}\n'
                                             f'{finish_context}')
                    else:
                        await message.answer(_('You don`t have any task', lang))
                else:
                    await message.answer(_('You don`t have any task', lang))
        else:
            await message.answer(_('You don`t have any task', lang))
    else:
        logging(
            f'ERROR: UNKNOUN_COMMAND={message.text}, TIME: {datetime.now()}, USER: {message.from_user.first_name} {message.from_user.last_name}, USER_ID: {message.from_user.id}  \n')
        await message.answer(_('Unknoun command.\n'
                               'Try again',
                               lang))


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
