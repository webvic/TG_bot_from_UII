from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

from dotenv import load_dotenv
import os
from PIL import Image


# возьмем переменные окружения из .env
load_dotenv()

# загружаем токен бота
TOKEN = os.environ.get("TOKEN")


# функция команды /start
async def start(update, context):
    await update.message.reply_text('Первая задача выполнена!')

# функция команды /warcraft
async def warcraft(update, context):
    # создаем список Inline кнопок
    keyboard = [[InlineKeyboardButton("Альянс", callback_data="Альянс"),
                InlineKeyboardButton("Орда", callback_data="Орда")]]
    
    # создаем Inline клавиатуру
    reply_markup = InlineKeyboardMarkup(keyboard)

    # прикрепляем клавиатуру к сообщению
    await update.message.reply_text('Warcraft. Choose mode:', reply_markup=reply_markup)

# функция обработки нажатия на кнопки Inline клавиатуры
async def button(update, context):

    # параметры входящего запроса при нажатии на кнопку
    query = update.callback_query

    # отправка всплывающего уведомления
    await query.answer('Начинаем игру!')
    
    # редактирование сообщения
    await query.edit_message_text(text=f"Вы вошли в режим: {query.data}")

async def make_dir(dir='Image'):
    # Получаем текущую рабочую директорию
    current_dir = os.getcwd()

    # Проверяем наличие папки "Images" в текущей директории
    images_dir = os.path.join(current_dir, "Images")
    if not os.path.exists(images_dir):
        # Если папки "Images" нет, создаем ее
        os.makedirs(images_dir)
    return images_dir

async def convert_to_jpg(file_path, output_path):
    # Открываем изображение
    image = Image.open(file_path)
    
    # Конвертируем в JPEG
    image.save(output_path, "JPEG")

async def download_and_convert(file, output_path,img_id):
    # Скачиваем файл
    file_path = await file.download_to_drive()
     
    # Конвертируем в JPG
    await convert_to_jpg(file_path, os.path.join(output_path, f"{img_id}.{'jpg'}"))

# функция для изображений
async def image(update, context):
    await update.message.reply_text('Эй! Мы получили от тебя фотографию!')
    
    # Получаем кортеж фотографий
    photo = update.message.photo[-1]

    # Получаем ID файла последней (самой большой) фотографии
    img_id = photo.file_id

    # достаем файл изображения из сообщения
    file = await photo.get_file()
    
    # Определяем папку для сохранения файлов
    output_path = "Image"
    if not os.path.exists(output_path):
        os.makedirs(output_path)
    
    # Конвертируем и сохраняем файл
    jpg_file_path = await download_and_convert(file, output_path, img_id)

# функция для текстовых сообщений
async def text(update, context):
    
    # использование update
    # print(update)
    # print()
    # print(update.message.text)
    # print(update.message.message_id)
    # print(update.message.date)
    # print(update.message.from_user.first_name)
    # print(update.message.from_user.id)
    # print()

    my_message = await update.message.reply_text(f'Число слов в вашем сообщении: {len(update.message.text.split())}')

    # использованеи context
    # time.sleep(5)
    # удаление сообщений
    # await context.bot.deleteMessage(chat_id=update.message.chat_id, message_id=my_message.message_id)

    # закрепление сообщений
    # await context.bot.pin_chat_message(chat_id=update.message.chat_id, message_id=update.message.message_id)

    # изменение описания бота
    # await context.bot.set_my_short_description("Этот бот очень умный, добрый и красивый")

# функция для голосовых сообщений
async def voice(update, context):
    voice_message = update.message.voice
    voice_message_id = voice_message.file_id
    await update.message.reply_text(f'Голосовое сообщение получено! Его ID: {voice_message_id}')


def main():

    # точка входа в приложение
    application = Application.builder().token(TOKEN).build()
    print('Бот запущен...')

    # добавляем обработчик команды /start
    application.add_handler(CommandHandler("start", start))

    # добавляем обработчик команды /warcraft
    application.add_handler(CommandHandler("warcraft", warcraft))

    # добавляем обработчик нажатия Inline кнопок
    application.add_handler(CallbackQueryHandler(button))

    # добавляем обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT, text))

    # добавляем обработчик голосовых сообщений
    application.add_handler(MessageHandler(filters.VOICE, voice))

    # добавляем обработчик сообщений с изображением
    application.add_handler(MessageHandler(filters.PHOTO, image))

    # запуск приложения (для остановки нужно нажать Ctrl-C)
    application.run_polling()


if __name__ == "__main__":
    main()