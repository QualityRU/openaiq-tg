from decouple import config

TELEGRAM_BOT_TOKEN: str = config('TELEGRAM_BOT_TOKEN')
OPENAI_API_KEY: str = config('OPENAI_API_KEY')
GPT_ENGINE: str = config('GPT_ENGINE')
ADMIN_IDS: set = set(
    int(user_id)
    for user_id in config('ADMIN_IDS', '').split(',')
    if user_id.strip()
)
