from yoomoney import Client

token = "YOUR_TOKEN"

client = Client(token)

response = client.request_payment(
    to='410019014512803',
    amount=150,
    comment="Sponsor this project"
)

print(response.result)
