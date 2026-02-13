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
| `Формы быстрой оплаты (Quickpay)`_ | Создание платёжной формы для встраивания на сайт или блог. |
+-------------------------------------+-----------------------------------------------------------+

Установка
=========

**Из PyPI** (рекомендуется):

.. code-block:: shell

   pip install yoomoney --upgrade

Или с помощью `uv <https://docs.astral.sh/uv/>`_:

.. code-block:: shell

   uv add yoomoney

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
3. Задайте параметры приложения. Сохраните **CLIENT_ID** и **REDIRECT_URI** —
   они понадобятся далее.
4. Нажмите **Подтвердить**.
5. Вставьте свои реальные данные вместо заглушек в коде ниже, выберите нужные
   права (scopes) и запустите скрипт.
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

Замените ``YOUR_TOKEN`` на свой токен и запустите:

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   user = client.account_info()

   print("Номер счёта:", user.account)
   print("Баланс:", user.balance)
   print("Валюта (ISO 4217):", user.currency)
   print("Статус аккаунта:", user.account_status)
   print("Тип аккаунта:", user.account_type)

   print("Расширенная информация о балансе:")
   for key, value in vars(user.balance_details).items():
       print(f"  {key}: {value}")

   print("Привязанные банковские карты:")
   if user.cards_linked:
       for card in user.cards_linked:
           print(f"  {card.pan_fragment} — {card.type}")
   else:
       print("  Нет привязанных карт")

.. code-block:: text

   Номер счёта: 410019014512803
   Баланс: 999999999999.99
   Валюта (ISO 4217): 643
   Статус аккаунта: identified
   Тип аккаунта: personal
   Расширенная информация о балансе:
     total: 999999999999.99
     available: 999999999999.99
     deposition_pending: None
     blocked: None
     debt: None
     hold: None
   Привязанные банковские карты:
     Нет привязанных карт

История операций
----------------

Замените ``YOUR_TOKEN`` и запустите:

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   history = client.operation_history()

   print("Список операций:")
   print("Следующая страница начинается с:", history.next_record)

   for op in history.operations:
       print()
       print(f"Операция: {op.operation_id}")
       print(f"  Статус     : {op.status}")
       print(f"  Дата       : {op.datetime}")
       print(f"  Название   : {op.title}")
       print(f"  Pattern id : {op.pattern_id}")
       print(f"  Направление: {op.direction}")
       print(f"  Сумма      : {op.amount}")
       print(f"  Метка      : {op.label}")
       print(f"  Тип        : {op.type}")

.. code-block:: text

   Список операций:
   Следующая страница начинается с: None

   Операция: 670278348725002105
     Статус     : success
     Дата       : 2021-10-10 10:10:10
     Название   : Пополнение с карты ****4487
     Pattern id : None
     Направление: in
     Сумма      : 100500.0
     Метка      : 3784030974
     Тип        : deposition

   Операция: 670244335488002313
     Статус     : success
     Дата       : 2021-10-10 10:10:10
     Название   : Перевод от 410019014512803
     Pattern id : p2p
     Направление: in
     Сумма      : 100500.0
     Метка      : 7920963969
     Тип        : incoming-transfer

Детали операции
---------------

Замените ``YOUR_TOKEN`` и ``OPERATION_ID`` (например ``670244335488002312``) и запустите:

.. code-block:: python

   from yoomoney import Client

   client = Client("YOUR_TOKEN")
   details = client.operation_details(operation_id="OPERATION_ID")

   for key, value in vars(details).items():
       if not key.startswith("_"):
           print(f"{key:20s} : {str(value).replace(chr(10), ' ')}")

.. code-block:: text

   operation_id         : 670244335488002312
   status               : success
   pattern_id           : p2p
   direction            : in
   amount               : 100500.0
   amount_due           : None
   fee                  : None
   datetime             : 2021-10-10 10:10:10
   title                : Перевод от 410019014512803
   sender               : 410019014512803
   recipient            : None
   recipient_type       : None
   message              : Justtext
   comment              : None
   codepro              : False
   protection_code      : None
   expires              : None
   answer_datetime      : None
   label                : 7920963969
   details              : Justtext
   type                 : incoming-transfer
   digital_goods        : None

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
   print(quickpay.redirected_url)

.. code-block:: text

   https://yoomoney.ru/quickpay/confirm.xml?receiver=410019014512803&quickpay-form=shop&targets=Sponsor%20this%20project&paymentType=SB&sum=150
   https://yoomoney.ru/transfer/quickpay?requestId=343532353937313933395f66326561316639656131626539326632616434376662373665613831373636393537613336383639

Асинхронный клиент
==================

Асинхронный клиент (``AsyncClient``) предоставляет тот же API, что и синхронный
``Client``, но каждый метод является корутиной. Используйте ``async with`` для
корректного закрытия пула соединений.

Асинхронная информация об аккаунте
----------------------------------

.. code-block:: python

   import asyncio
   from yoomoney import AsyncClient

   async def main():
       async with AsyncClient("YOUR_TOKEN") as client:
           user = await client.account_info()

           print("Номер счёта:", user.account)
           print("Баланс:", user.balance)
           print("Валюта (ISO 4217):", user.currency)
           print("Статус аккаунта:", user.account_status)
           print("Тип аккаунта:", user.account_type)

           print("Расширенная информация о балансе:")
           for key, value in vars(user.balance_details).items():
               print(f"  {key}: {value}")

           print("Привязанные банковские карты:")
           if user.cards_linked:
               for card in user.cards_linked:
                   print(f"  {card.pan_fragment} — {card.type}")
           else:
               print("  Нет привязанных карт")

   asyncio.run(main())

Асинхронная история операций
----------------------------

.. code-block:: python

   import asyncio
   from yoomoney import AsyncClient

   async def main():
       async with AsyncClient("YOUR_TOKEN") as client:
           history = await client.operation_history()

           print("Список операций:")
           print("Следующая страница начинается с:", history.next_record)

           for op in history.operations:
               print()
               print(f"Операция: {op.operation_id}")
               print(f"  Статус     : {op.status}")
               print(f"  Дата       : {op.datetime}")
               print(f"  Название   : {op.title}")
               print(f"  Pattern id : {op.pattern_id}")
               print(f"  Направление: {op.direction}")
               print(f"  Сумма      : {op.amount}")
               print(f"  Метка      : {op.label}")
               print(f"  Тип        : {op.type}")

   asyncio.run(main())

Асинхронные детали операции
---------------------------

.. code-block:: python

   import asyncio
   from yoomoney import AsyncClient

   async def main():
       async with AsyncClient("YOUR_TOKEN") as client:
           details = await client.operation_details(operation_id="OPERATION_ID")

           for key, value in vars(details).items():
               if not key.startswith("_"):
                   print(f"{key:20s} : {str(value).replace(chr(10), ' ')}")

   asyncio.run(main())

----

Лицензия
========

Проект распространяется под лицензией
`GPL-3.0 <https://github.com/AlekseyKorshuk/yoomoney-api/blob/master/LICENSE>`_.
