# OpenAIQ - телеграмм бот с бесплатным доступом к ChatGPT 3.5 / 4 / 4o / 4.1
Данный бот позволяет пользоваться ChatGPT через телеграмм бота.

### Технологии используемые в проекте:
- aiohttp
- aiogram
- openai


### Инструкция по запуску
1) Получить API-ключ для ChatGPT

Проходим по ссылке (https://api.chatanywhere.org/v1/oauth/free/render) и регистрируем свой API-ключ

2) Получить API-ключ телеграмм-бота

У https://t.me/BotFather получаем API-ключ к боту

3) Склонировать репозиторий:
```
https://github.com/QualityRU/openaiq-tg.git
```
4) Переименовать ```.env.example``` в ```.env``` и заполнить его полученными ранее ключами

6) Установить вирутальное окружение, активировать его и установить зависимости
```
python3 -m venv venv
```
```
. venv/bin/activate
```
```
pip install -r requirements.txt
```

6) Запустить бота
```
python main.py
```