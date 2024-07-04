API Yoomoney - unofficial python library
==================================================

This is an unofficial `YooMoney <https://yoomoney.ru>`_ API python library.

==========
Summary
==========

- `Introduction`_

- `Features`_

- `Installation`_

- `Quick start`_

  #. `Access token`_

  #. `Account information`_

  #. `Operation history`_

  #. `Operation details`_

  #. `Quickpay forms`_

============
Introduction
============

This repository is based on the official documentation of `YooMoney <https://yoomoney.ru/docs/wallet>`__.

========
Features
========

Implemented methods:

- `Access token`_ - Getting an access token
- `Account information`_ - Getting information about the status of the user account.
- `Operation history`_ - This method allows viewing the full or partial history of operations in page mode. History records are displayed in reverse chronological order (from most recent to oldest).
- `Operation details`_ - Provides detailed information about a particular operation from the history.
- `Quickpay forms`_ - The YooMoney form is a set of fields with information about a transfer. You can embed payment form into your interface (for instance, a website or blog). When the sender pushes the button, the details from the form are sent to YooMoney and an order for a transfer to your wallet is initiated.

============
Installation
============

You can install with:

.. code:: shell

        pip install yoomoney --upgrade


You can install from source with:

.. code:: shell

    git clone https://github.com/AlekseyKorshuk/yoomoney-api --recursive
    cd yoomoney-api
    python setup.py install

===========
Quick start
===========

Access token
************

First of all we need to receive an access token.

.. image:: token.gif

1. Log in to your YooMoney wallet with your username. If you do not have a wallet, `create it <https://yoomoney.ru/reg>`_.
2. Go to the `App registration <https://yoomoney.ru/myservices/new>`_ page.
3. Set the application parameters. Save CLIENT_ID and YOUR_REDIRECT_URI for net steps
4. Click the Confirm button.
5. Paste CLIENT_ID, REDIRECT_URI and CLIENT_SECRET insted of YOUR_CLIENT_ID, YOUR_REDIRECT_URI and YOUR_CLIENT_SECRET. Choose scopes and run code.
6. Follow all steps from the program.

.. code:: python

    from yoomoney import Authorize

    Authorize(
          client_id="YOUR_CLIENT_ID",
          redirect_uri="YOUR_REDIRECT_URI",
          client_secret="YOUR_CLIENT_SECRET",
          scope=["account-info",
                 "operation-history",
                 "operation-details",
                 "incoming-transfers",
                 "payment-p2p",
                 "payment-shop",
                 ]
          )

You are done with the most difficult part!

Account information
*******************

Paste YOUR_TOKEN and run this code:

.. code:: python

      from yoomoney import Client

      token = "YOUR_TOKEN"

      client = Client(token)

      user = client.account_info()

      print("Account number:", user.account)
      print("Account balance:", user.balance)
      print("Account currency code in ISO 4217 format:", user.currency)
      print("Account status:", user.account_status)
      print("Account type:", user.account_type)

      print("Extended balance information:")
      for pair in vars(user.balance_details):
          print("\t-->", pair, ":", vars(user.balance_details).get(pair))

      print("Information about linked bank cards:")
      cards = user.cards_linked

      if len(cards) != 0:
          for card in cards:
              print(card.pan_fragment, " - ", card.type)
      else:
          print("No card is linked to the account")

Output:
*******
.. code:: python

      Account number: 410019014512803
      Account balance: 999999999999.99
      Account currency code in ISO 4217 format: 643
      Account status: identified
      Account type: personal
      Extended balance information:
         --> total : 999999999999.99
         --> available : 999999999999.99
         --> deposition_pending : None
         --> blocked : None
         --> debt : None
         --> hold : None
      Information about linked bank cards:
      No card is linked to the account


Operation history
*****************

Paste YOUR_TOKEN and run this code:

.. code:: python

      from yoomoney import Client

      token = "YOUR_TOKEN"

      client = Client(token)

      history = client.operation_history()

      print("List of operations:")
      print("Next page starts with: ", history.next_record)

      for operation in history.operations:
          print()
          print("Operation:",operation.operation_id)
          print("\tStatus     -->", operation.status)
          print("\tDatetime   -->", operation.datetime)
          print("\tTitle      -->", operation.title)
          print("\tPattern id -->", operation.pattern_id)
          print("\tDirection  -->", operation.direction)
          print("\tAmount     -->", operation.amount)
          print("\tLabel      -->", operation.label)
          print("\tType       -->", operation.type)

Output:
*******
.. code:: python

      List of operations:
      Next page starts with:  None

      Operation: 670278348725002105
        Status     --> success
        Datetime   --> 2021-10-10 10:10:10
        Title      --> Пополнение с карты ****4487
        Pattern id --> None
        Direction  --> in
        Amount     --> 100500.0
        Label      --> 3784030974
        Type       --> deposition

      Operation: 670244335488002313
        Status     --> success
        Datetime   --> 2021-10-10 10:10:10
        Title      --> Перевод от 410019014512803
        Pattern id --> p2p
        Direction  --> in
        Amount     --> 100500.0
        Label      --> 7920963969
        Type       --> incoming-transfer


Operation details
*****************

Paste YOUR_TOKEN with an OPERATION_ID (example: 670244335488002312) from previous example output and run this code:

.. code:: python

      from yoomoney import Client

      token = "YOUR_TOKEN"

      client = Client(token)

      details = client.operation_details(operation_id="OPERATION_ID")

      properties = [i for i in details.__dict__.keys() if i[:1] != '_']

      max_size = len(max(properties, key=len))

      for prop in properties:
          print(prop, " " * (max_size - len(prop)), "-->", str(details.__getattribute__(prop)).replace('\n', ' '))

Output:
*******
.. code:: python

      operation_id     --> 670244335488002312
      status           --> success
      pattern_id       --> p2p
      direction        --> in
      amount           --> 100500.0
      amount_due       --> None
      fee              --> None
      datetime         --> 2021-10-10 10:10:10
      title            --> Перевод от 410019014512803
      sender           --> 410019014512803
      recipient        --> None
      recipient_type   --> None
      message          --> Justtext
      comment          --> None
      codepro          --> False
      protection_code  --> None
      expires          --> None
      answer_datetime  --> None
      label            --> 7920963969
      details          --> Justtext
      type             --> incoming-transfer
      digital_goods    --> None


Quickpay forms
**************

Run this code:

.. code:: python

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

Output:
*******
.. code:: python

      https://yoomoney.ru/quickpay/confirm.xml?receiver=410019014512803&quickpay-form=shop&targets=Sponsor%20this%20project&paymentType=SB&sum=150
      https://yoomoney.ru/transfer/quickpay?requestId=343532353937313933395f66326561316639656131626539326632616434376662373665613831373636393537613336383639
