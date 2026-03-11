"""FastAPI webhook server for YooMoney payment notifications.

Installation
------------
    pip install yoomoney[fastapi]

    or manually:

    pip install fastapi uvicorn python-multipart

Setup
-----
1. Get your notification secret from YooMoney:
   https://yoomoney.ru/transfer/myservices/http-notification

2. Set your notification URL in YooMoney settings:
   https://your-domain.com/yoomoney/notify

3. Set environment variable:
   export YOOMONEY_SECRET=your_secret_here

Running
-------
    uvicorn examples.webhook_server:app --host 0.0.0.0 --port 8000

For production with multiple workers:
    uvicorn examples.webhook_server:app --host 0.0.0.0 --port 8000 --workers 4
"""

import os

from fastapi import FastAPI, Request

from yoomoney.webhook import Notification, fastapi_webhook

SECRET = os.environ.get("YOOMONEY_SECRET", "YOUR_NOTIFICATION_SECRET")

app = FastAPI()


def handle_payment(notification: Notification) -> None:
    print("Payment received!")
    print(f"  operation_id : {notification.operation_id}")
    print(f"  amount       : {notification.amount}")
    print(f"  label        : {notification.label}")
    print(f"  sender       : {notification.sender}")


@app.post("/yoomoney/notify")
async def notify(request: Request):
    return await fastapi_webhook(
        request=request,
        secret=SECRET,
        on_payment=handle_payment,
    )
