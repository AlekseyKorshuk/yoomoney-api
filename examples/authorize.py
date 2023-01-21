from yoomoney import Authorize

Authorize(client_id='YOUR_CLIENT_ID', 
          client_secret='YOUR_CLIENT_SECRET',
          redirect_uri='YOUR_REDIRECT_URI',
          scope=["account-info",
                 "operation-history",
                 "operation-details",
                 "incoming-transfers",
                 "payment-p2p",
                 "payment-shop",
          ]
)
