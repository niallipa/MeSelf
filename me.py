"""
    Version 0.01
"""

from pyrogram import Client, filters, idle
from pyrogram.errors import FloodWait
from time import sleep
import time
import subprocess
import psutil
import datetime
import requests

timerStart = time.time()

RASPBERRY = True

accounts = [
    {"session_name": "account1", "api_id": 3791635, "api_hash": "cb2263b73c0d8e8c192730ed2d0a5036"},
    # {"session_name": "account2", "api_id": 25274244, "api_hash": "51a21a254d86e117d6f272fd1a4b5e7b"},
    # Добавьте больше аккаунтов здесь
]

clients = []
for account in accounts:
    session_name = account['session_name']
    api_id = account['api_id']
    api_hash = account['api_hash']
    client = Client(session_name, api_id=api_id, api_hash=api_hash)
    clients.append(client)
    print(f"Client {session_name} has started.")
    client.start()


# Получить время работы сервера
def get_uptime():
    boot_time = psutil.boot_time()
    current_time = datetime.datetime.now().timestamp()
    uptime = current_time - boot_time
    uptime_timedelta = datetime.timedelta(seconds=uptime)

    # Получение количества дней, часов, минут и секунд
    days = uptime_timedelta.days
    hours = uptime_timedelta.seconds // 3600
    minutes = (uptime_timedelta.seconds // 60) % 60
    seconds = uptime_timedelta.seconds % 60

    return f"Сервер включен: {days} д. {hours} ч. {minutes} м. {seconds:.2f} с."


# Статус сетевых интерфейсов
def get_network_info():
    network_info = psutil.net_if_stats()
    network_io = psutil.net_io_counters(pernic=True)

    # Получение информации о сетевых интерфейсах
    interfaces = list(network_info.keys())

    # Сбор информации о пропускной способности и текущей загрузке сетевых интерфейсов в одну строку
    network_info_str = ""
    for interface in interfaces:
        stats = network_info[interface]
        if stats.isup:
            bandwidth = round(stats.speed / (8 * 1024 * 1024), 2)  # округление до 2 знаков после запятой и перевод в МБ
            if interface in network_io:
                io = network_io[interface]
                bytes_sent = round(io.bytes_sent / (1024 * 1024), 2)  # округление до 2 знаков после запятой и перевод в МБ
                bytes_recv = round(io.bytes_recv / (1024 * 1024), 2)  # округление до 2 знаков после запятой и перевод в МБ
                network_info_str += f"Интерфейс: {interface}, Полоса: {bandwidth} МБ, Отправлено: {bytes_sent} МБ, Получено: {bytes_recv} МБ\n"
            else:
                network_info_str += f"Интерфейс: {interface}, Полоса: {bandwidth} МБ, Отправлено: Нет данных, Получено: Нет данных\n"

    return network_info_str

# Статус дискового пространства
def get_disk_usage():
    disk_usage = psutil.disk_usage('/')
    total_space = disk_usage.total / (1024 ** 2)  # перевод в мегабайты
    used_space = disk_usage.used / (1024 ** 2)  # перевод в мегабайты
    percent_used = disk_usage.percent
    return f'Диск: {used_space}/{total_space} МБ, {percent_used}%'

# Работа диска
def get_disk_io():
    disk_io = psutil.disk_io_counters()
    read_bytes = disk_io.read_bytes / (1024 ** 2)  # перевод в мегабайты
    write_bytes = disk_io.write_bytes / (1024 ** 2)  # перевод в мегабайты
    return f'чтение {read_bytes:.0f}, запись{write_bytes:.0f} МБ',

# Работа процессора
def get_cpu_usage():
    cpu_percent = psutil.cpu_percent()
    cpu_count = psutil.cpu_count()
    return f"Процессор: {cpu_percent}%, Ядер: {cpu_count}"

# Получить оперативную память 
def get_memory_usage():
    virtual_memory = psutil.virtual_memory()
    total_memory = virtual_memory.total / (1024 * 1024)
    used_memory = virtual_memory.used / (1024 * 1024)
    percent_memory = virtual_memory.percent
    return f'Оперативная память:{used_memory:.0f}/{total_memory:.0f} МБ, {percent_memory:.2f}%'

# Получить через sensors температуру процессора
def get_cpu_temperature():
    output = subprocess.check_output(['sensors'])
    lines = output.decode().split('\n')
    for line in lines:
        if 'temp1' in line:
            temperature = line.split(':')[1].strip().split(' ')[0]
            return str(temperature)

# Функция формата времени в день, часы, минуты, секунды
def format_time(seconds):
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    return f"{int(days)} д., {int(hours)} ч., {int(minutes)} м., {seconds:.0f} с."

# Функция статуса .status
def status(client, msg):
    elapsedTime = time.time() - timerStart
    client.delete_messages(msg.chat.id, msg.id)
    uptime = format_time(elapsedTime)
    
    if RASPBERRY:
        client.send_message(msg.chat.id, f"Запущено на сервере.\nВремя работы: {uptime}\n{get_memory_usage()}\n{get_cpu_usage()} темп.: {get_cpu_temperature()}\n{get_disk_usage()}, {get_disk_io()}\n{get_network_info()}\n{get_uptime()}")
    else:
        client.send_message(msg.chat.id, f"Запущено локально.\nВремя работы: {uptime}")




# Функция обработчика команды .type
def typee(client, msg):
    # print(msg)
    # print(msg.text)
    orig_text = msg.text.split(".type ", maxsplit=1)[1]
    text = orig_text
    tbp = ""  # to be printed
    typing_symbol = "▒"

    while tbp != orig_text:
        try:
            msg.edit(tbp + typing_symbol)
            sleep(0.05)  # 50 ms

            tbp = tbp + text[0]
            text = text[1:]

            msg.edit(tbp)
            sleep(0.05)

        except FloodWait as e:
            sleep(e.x)

def heart_filling(client, msg):
    heart_stages = [
        "🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤",
        "🖤🖤❤️❤️🖤🖤🖤🖤🖤❤️❤️🖤🖤",
        "🖤❤️❤️❤️❤️🖤🖤🖤❤️❤️❤️❤️🖤",
        "🖤❤️❤️❤️❤️❤️🖤❤️❤️❤️❤️❤️🖤",
        "🖤🖤❤️❤️❤️❤️❤️❤️❤️❤️❤️🖤🖤",
        "🖤🖤🖤❤️❤️❤️❤️❤️❤️❤️🖤🖤🖤",
        "🖤🖤🖤🖤❤️❤️❤️❤️❤️🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤❤️❤️❤️🖤🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤🖤❤️🖤🖤🖤🖤🖤🖤",
        "🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤🖤"
    ]
    chat_id = msg.chat.id
    client.delete_messages(msg.chat.id, msg.id)
    message = client.send_message(chat_id, heart_stages[0])
    text = message.text
    for stage in heart_stages[1:]:
        try:
            text = text + "\n" + stage
            message.edit_text(text)
            sleep(0.3)
        except FloodWait as e:
            sleep(e.x)

def send_reactions(client, msg):
    msg.react(emoji='👍')


def ping_service(client, message):
    endpoints = {
        "8080": "http://185.192.247.60:8080/ping",
        "8090": "http://185.192.247.60:8090/ping",
        "80": "http://185.192.247.60:80/ping",
        "8081": "http://185.192.247.60:8081/ping",
        "8666": "http://185.192.247.60:8666/ping",
        "8900": "http://185.192.247.60:8900/ping"
    }

    responses = {}
    for port, url in endpoints.items():
        try:
            response = requests.get(url)
            responses[port] = f"{port} - code {response.status_code}"
        except requests.exceptions.RequestException as e:
            responses[port] = f"{port} - ERROR"

    response_text = "\n".join(responses.values())
    client.send_message(message.chat.id, response_text)


for client in clients:


    # Фильтр команды .type
    @client.on_message(filters.command("type", prefixes=".") & filters.me)
    def message_handler(client, message):
        typee(client, message)


    # Фильтры команды .heart
    @client.on_message(filters.command("heart", prefixes=".") & filters.me)
    def message_handler(client, message):
        heart_filling(client, message)


    #Фильтр пересылки сообщений из рабочий группы
    # @client.on_message(filters.chat(-604038253)) # forward_messages 920379538
    # def message_handler(client, message):
    #     if client.name == "account1":
    #         client.forward_messages(-1002059083019, from_chat_id=message.chat.id, message_ids=message.id)
    #         # client.send_message(chat_id=920379538, text="Message forwarded to account2")

    #Фильтр команды статус
    @client.on_message(filters.command("status", prefixes=".") & filters.me)
    def message_handler(client, message):
        status(client, message)


    #Фильтр команды ping
    @client.on_message(filters.command("ping", prefixes="."))
    def ping(client, message):
        # Получение аргументов команды
        args = message.command[1:]
        if len(args) == 0:
            message.reply_text("Пожалуйста, укажите IP-адрес, доменное имя или 'server' для пинга.")
            return

        # Проверка аргумента "server"
        if "server" in args:
            targets = ["95.140.159.144", "185.192.247.60"]
        else:
            targets = args

        try:
            for i, target in enumerate(targets):
                # Выполнение команды ping с помощью subprocess
                ping_result = subprocess.run(['ping', '-c', '4', target], capture_output=True, text=True).stdout

                # Редактирование или отправка сообщения с результатом пинга
                if i == 0:
                    message.edit_text(f"{target}:\n{ping_result}")
                else:
                    message.reply_text(f"{target}:\n{ping_result}")
        except Exception as e:
            message.edit_text(f"Ошибка: {str(e)}")


    @client.on_message(filters.command("ping_service", prefixes=".") & filters.me)
    def message_handler(client, message):
        ping_service(client, message)




idle()

# compose() and asyncio()