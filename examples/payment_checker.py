"""Example: wait for a payment with a specific label (synchronous polling)."""

from yoomoney import PaymentChecker, Quickpay
from yoomoney.operation.operation import Operation

TOKEN = "YOUR_TOKEN"
RECEIVER = "YOUR_WALLET_NUMBER"


def on_payment_received(op: Operation) -> None:
    print("  Payment confirmed!")
    print(f"  Amount       : {op.amount} ₽")
    print(f"  Label        : {op.label}")
    print(f"  Operation ID : {op.operation_id}")
    print(f"  Date/Time    : {op.datetime}")


checker = PaymentChecker(token=TOKEN, interval=5)
label = PaymentChecker.make_label(prefix="order")
print(f"Generated label: {label}")

payment = Quickpay(
    receiver=RECEIVER,
    quickpay_form="shop",
    targets="Order payment",
    paymentType="AC",
    sum=2,
    label=label,
    successURL="https://example.com/thanks",
)
print(f"Payment URL: {payment.base_url}")

paid = checker.watch(
    label=label,
    callback=on_payment_received,
    amount=299.0,
    timeout=600,
)

if not paid:
    print("Payment not received within the timeout.")
