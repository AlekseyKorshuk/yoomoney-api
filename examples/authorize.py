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
