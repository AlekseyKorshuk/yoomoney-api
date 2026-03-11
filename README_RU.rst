YooMoney API
============

*Неофициальная Python-библиотека для YooMoney API*

|pypi| |python| |license|

.. |pypi| image:: https://img.shields.io/pypi/v/yoomoney?color=blue&label=PyPI
   :target: https://pypi.org/project/yoomoney/
.. |python| image:: https://img.shields.io/pypi/pyversions/yoomoney
   :target: https://pypi.org/project/yoomoney/
.. |license| image:: https://img.shields.io/github/license/AlekseyKorshuk/yoomoney-api
   :target: https://github.com/AlekseyKorshuk/yoomoney-api/blob/master/LICENSE

`🇬🇧 English version <README.rst>`_

----

.. contents:: Содержание
   :depth: 2
   :local:
   :backlinks: none

----

Введение
========

Библиотека предоставляет удобную Python-обёртку над
`API кошелька YooMoney <https://yoomoney.ru/docs/wallet>`__.
В комплекте идут **синхронный** (``Client``) и **асинхронный** (``AsyncClient``)
клиенты.

Возможности
===========

+-------------------------------------+-----------------------------------------------------------+
| Метод                               | Описание                                                  |
+=====================================+===========================================================+
| `Получение токена`_                 | Получение OAuth-токена доступа.                           |
+-------------------------------------+-----------------------------------------------------------+
| `Информация об аккаунте`_           | Получение информации о состоянии счёта пользователя.      |
+-------------------------------------+-----------------------------------------------------------+
| `История операций`_                 | Просмотр полной или частичной истории операций             |
|                                     | (постраничная, в обратном хронологическом порядке).        |
+-------------------------------------+-----------------------------------------------------------+
| `Детали операции`_                  | Подробная информация об отдельной операции.                |
+-------------------------------------+-----------------------------------------------------------+
| `Формы быстрой оплаты (Quickpay)`_ | Создание платёжной формы для встраивания на сайт или бота. |
+-------------------------------------+-----------------------------------------------------------+
| `Проверка платежей`_                | Polling входящих платежей по label (sync и async).         |
+-------------------------------------+-----------------------------------------------------------+
| `Webhook-уведомления`_              | Приём уведомлений о платежах через FastAPI.                |
+-------------------------------------+-----------------------------------------------------------+

Установка
=========

**Из PyPI** (рекомендуется):

.. code-block:: shell

   pip install yoomoney --upgrade

Или с помощью `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: shell

   uv add yoomoney

**С поддержкой webhook:**

.. code-block:: shell

   pip install yoomoney fastapi

**Из исходников**:

.. code-block:: shell

   git clone https://github.com/AlekseyKorshuk/yoomoney-api --recursive
   cd yoomoney-api
   uv sync

Быстрый старт
==============

Получение токена
----------------

Для начала работы необходимо получить токен доступа.

.. image:: docs/assets/token.gif
   :alt: Получение токена доступа

1. Войдите в свой кошелёк YooMoney. Если у вас его нет —
   `создайте <https://yoomoney.ru/reg>`_.
2. Перейдите на страницу `регистрации приложения <https://yoomoney.ru/myservices/new>`_.
3. Задайте параметры приложения. Сохраните **CLIENT_ID** и **REDIRECT_URI**.
4. Нажмите **Подтвердить**.
5. Вставьте свои реальные данные в код ниже и запустите скрипт.
6. Следуйте инструкциям на экране.

.. code-block:: python

   from yoomoney import Authorize

   Authorize(
       client_id="YOUR_CLIENT_ID",
       redirect_uri="YOUR_REDIRECT_URI",
       client_secret="YOUR_CLIENT_SECRET",
       scope=[
           "account-info",
           "operation-history",
           "operation-details",
           "incoming-transfers",
           "payment-p2p",
           "payment-shop",
       ],
   )

Самая сложная часть позади!

Информация об аккаунте
----------------------

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   user = client.account_info()

   print("Номер счёта:", user.account)
   print("Баланс:", user.balance, user.currency)
   print("Статус:", user.account_status)
   print("Тип:", user.account_type)

История операций
----------------

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   history = client.operation_history(records=10)

   for op in history.operations:
       print(f"{op.datetime}  {op.direction:>4}  {op.amount} ₽  {op.label or '—'}")

Детали операции
---------------

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   details = client.operation_details(operation_id="OPERATION_ID")

   for key, value in vars(details).items():
       if not key.startswith("_"):
           print(f"{key:20s} : {str(value).replace(chr(10), ' ')}")

Формы быстрой оплаты (Quickpay)
--------------------------------

.. code-block:: python

   from yoomoney import Quickpay

   quickpay = Quickpay(
       receiver="410019014512803",
       quickpay_form="shop",
       targets="Sponsor this project",
       paymentType="SB",
       sum=150,
   )
   print(quickpay.base_url)

Проверка платежей
-----------------

``PaymentChecker`` опрашивает историю операций и вызывает колбэк сразу после
поступления входящего платежа с нужным label (и опционально суммой).

.. code-block:: python

   from yoomoney import Quickpay, PaymentChecker
   from yoomoney.operation.operation import Operation

   TOKEN    = "YOUR_TOKEN"
   RECEIVER = "YOUR_WALLET"

   label = PaymentChecker.make_label("order")

   quickpay = Quickpay(
       receiver=RECEIVER,
       quickpay_form="shop",
       targets="Оплата заказа",
       paymentType="AC",
       sum=299.0,
       label=label,
   )
   print("Ссылка на оплату:", quickpay.base_url)

   def on_paid(op: Operation) -> None:
       print(f"  Получено {op.amount} ₽  label={op.label}")

   checker = PaymentChecker(token=TOKEN, interval=5)
   paid = checker.watch(label=label, callback=on_paid, amount=299.0, timeout=600)

Асинхронная версия:

.. code-block:: python

   import asyncio
   from yoomoney import PaymentChecker
   from yoomoney.operation.operation import Operation

   async def main() -> None:
       checker = PaymentChecker(token="YOUR_TOKEN", interval=5)

       async def on_paid(op: Operation) -> None:
           print(f"  Получено {op.amount} ₽")

       await checker.watch_async(label="order_123", callback=on_paid, timeout=300)

   asyncio.run(main())

Webhook-уведомления
-------------------

YooMoney умеет отправлять POST-уведомление на ваш сервер при поступлении платежа.
Библиотека предоставляет готовый обработчик для FastAPI со встроенной проверкой
SHA-1 подписи.

**Шаг 1 — Установка**

.. code-block:: shell

   pip install yoomoney fastapi

**Шаг 2 — Получите секрет в YooMoney**

1. Перейдите на `yoomoney.ru/transfer/myservices/http-notification <https://yoomoney.ru/transfer/myservices/http-notification>`_.
2. Скопируйте значение из **«Секрет для проверки подлинности»** — это ваш ``SECRET``.
3. В поле **«Куда отправлять (URL сайта)»** укажите URL вашего сервера.
4. Поставьте галочку **«Отправлять HTTP-уведомления»** и сохраните.

**Шаг 3 — Создайте сервер**

.. code-block:: python

   import os
   from fastapi import FastAPI, Request
   from yoomoney.webhook import Notification, fastapi_webhook

   SECRET = os.environ.get("YOOMONEY_SECRET", "ВАШ_СЕКРЕТ")

   app = FastAPI()

   def on_payment(notification: Notification) -> None:
       print(f"  Платёж получен!")
       print(f"  сумма        : {notification.amount} ₽")
       print(f"  operation_id : {notification.operation_id}")
       print(f"  label        : {notification.label}")
       print(f"  отправитель  : {notification.sender}")

   @app.post("/yoomoney/notify")
   async def notify(request: Request):
       return await fastapi_webhook(
           request=request,
           secret=SECRET,
           on_payment=on_payment,
       )

**Шаг 4 — Запустите сервер**

.. code-block:: shell

   uvicorn myapp:app --host 0.0.0.0 --port 8000

Для продакшна с несколькими воркерами:

.. code-block:: shell

   uvicorn myapp:app --host 0.0.0.0 --port 8000 --workers 4

**Тестирование локально через ngrok**

YooMoney требует публичный HTTPS-адрес для отправки уведомлений.
При локальной разработке его можно получить бесплатно через
`ngrok <https://ngrok.com>`_.

1. Зарегистрируйтесь на `ngrok.com <https://ngrok.com>`_ и скачайте утилиту.

2. Авторизуйтесь (одноразово):

.. code-block:: shell

   ngrok config add-authtoken ВАШ_ТОКЕН_С_САЙТА_NGROK

3. В первом терминале запустите ваш сервер:

.. code-block:: shell

   uvicorn myapp:app --host 0.0.0.0 --port 8000

4. Во втором терминале запустите ngrok:

.. code-block:: shell

   ngrok http 8000

5. В выводе ngrok найдите строку ``Forwarding`` — это ваш публичный URL:

.. code-block:: text

   Forwarding  https://abc123.ngrok-free.app -> http://localhost:8000

6. Скопируйте этот URL (``https://abc123.ngrok-free.app``) и вставьте его
   в поле **«Куда отправлять (URL сайта)»** в настройках YooMoney,
   добавив путь: ``https://abc123.ngrok-free.app/yoomoney/notify``

7. Нажмите **«Протестировать»** — в терминале с сервером появится уведомление:

.. code-block:: text

     Платёж получен!
     сумма        : 200.39 ₽
     operation_id : test-notification
     label        :
     отправитель  : 41001000040

Чтобы отключить проверку подписи во время локальной разработки, передайте ``verify=False``:

.. code-block:: python

   return await fastapi_webhook(request=request, secret=SECRET,
                                on_payment=on_payment, verify=False)

Асинхронный клиент
==================

.. code-block:: python

   import asyncio
   from yoomoney import AsyncClient

   async def main():
       async with AsyncClient("YOUR_TOKEN") as client:
           user    = await client.account_info()
           history = await client.operation_history(records=5)

           print("Баланс:", user.balance)
           for op in history.operations:
               print(f"  {op.datetime}  {op.amount} ₽")

   asyncio.run(main())

----

Лицензия
========

Проект распространяется под лицензией
`GPL-3.0 <https://github.com/AlekseyKorshuk/yoomoney-api/blob/master/LICENSE>`_.
