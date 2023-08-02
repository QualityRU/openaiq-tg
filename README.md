# OpenAIQ - телеграмм бот с бесплатным доступом к ChatGPT 3.5 / 4
Данный бот позволяет пользоваться ChatGPT через телеграмм бота без VPN и регистрации аккаунта посредством реверс-инжиниринга.

### Технологии используемые в проекте:
- aiohttp
- aiogram
- openai


### Инструкция по запуску
1) Получить API-ключ для ChimeraGPT

Вступаем в Discord проекта (https://discord.gg/chimeragpt), проходим верификацию (https://discord.com/channels/1109383423061147680/1110612696874885141), идем в канал #bot и отправляем команду /key get

2) Получить API-ключ телеграмм-бота

У https://t.me/BotFather получаем API-ключ к боту

3) Склонировать репозиторий:
```
https://github.com/QualityRU/openaiq-tg.git
```
4) Переименовать ```.env.example``` в ```.env``` и заполнить его полученными ранее ключами

5) Установить вирутальное окружение, активировать его и установить зависимости
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

### Автор
2023 Quality mr.quality@ya.ru