import requests
try:
    from commands import Time, File, Str, Int
except ImportError:
    from bootstrapping_module import *
    from commands import Time, File, Str, Int
try:
    import telebot
except ImportError:
    from commands.pip9 import Pip
    Pip.install("pytelegrambotapi")
    import telebot


def safe_start_bot(bot_func, skipped_exceptions=(requests.exceptions.ReadTimeout,
                                                 requests.exceptions.ConnectionError,
                                                 requests.exceptions.ChunkedEncodingError)):
    ended = False
    while not ended:
        try:
            bot_func()
            ended = True
        except skipped_exceptions as e:
            print(f"{e} {e.args} {e.with_traceback(e.__traceback__)}... {Time.dotted()}")
            Time.sleep(5)


def very_safe_start_bot(bot_func):
    safe_start_bot(bot_func=bot_func, skipped_exceptions=(requests.exceptions.ReadTimeout,
                                                          requests.exceptions.ConnectionError,
                                                          requests.exceptions.ChunkedEncodingError,
                                                          telebot.apihelper.ApiException,
                                                          telebot.apihelper.ApiTelegramException))


def download_file(telegram_api, telegram_token, file_id, output_path):
    import requests
    import shutil
    file_info = telegram_api.get_file(file_id)
    address = f'https://api.telegram.org/file/bot{telegram_token}/{file_info.file_path}'
    r = requests.get(address, stream=True)
    if r.status_code == 200:
        with open(output_path, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        raise requests.HTTPError(f"Status: '{r.status_code}', address: '{address}'")


def send_photo(telegram_api, image_path, chat_id):
    if not File.exist(image_path):
        raise FileNotFoundError(f"File not exist: '{image_path}'")
    photo = open(image_path, 'rb')
    telegram_api.send_photo(chat_id, photo)


def send_video(telegram_api, video_path, chat_id):
    if not File.exist(video_path):
        raise FileNotFoundError(f"File not exist: '{video_path}'")
    video = open(video_path, 'rb')
    telegram_api.send_video(chat_id, video)


def send_message(telegram_api_object, chat_id, text,
                 disable_web_page_preview=None, reply_to_message_id=None, reply_markup=None,
                 parse_mode=None, disable_notification=None):
    if len(text) in Int.from_to(1, 4095):
        texts = [text]
    elif len(text) > 4096:
        texts = Str.split_every(text, 4096)
    else:
        texts = ["<empty message>"]
    output = []
    for text in texts:
        for i in range(10):
            try:
                output.append(telegram_api_object.send_message(chat_id=chat_id, text=text,
                                                               disable_web_page_preview=disable_web_page_preview,
                                                               reply_to_message_id=reply_to_message_id,
                                                               reply_markup=reply_markup, parse_mode=parse_mode,
                                                               disable_notification=disable_notification,
                                                               timeout=300))
                break
            except requests.exceptions.ReadTimeout:
                pass
    if len(output) == 0:
        return []
    elif len(output) == 1:
        return output
    else:
        return output


def delete_message(telegram_api: telebot.TeleBot, chat_id, message_id):
    return telegram_api.delete_message(chat_id, message_id)
