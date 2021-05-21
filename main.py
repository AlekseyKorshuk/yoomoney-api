from yoomoney import Quickpay
import requests, random, time
token = "YOUR_TOKEN"
token = "410019014512803.FFC25705851AEE05EA36A435025663B57D53EE065BB427E5B808C397DBDB67A7F9A07C82DC3F05368E2B2C30D60D31751654605C66918D978B0C016DCE9FBC01A5DBFE51BC436F9AC1DEE2C2287C93371CD024EF033425C44F6E094DEA921497804AD63FDE288BF9FF4D1314D82A97878FB91492F0E639BD7782CEC9A621A737"

quickpay = Quickpay(
            receiver="410019014512803",
            quickpay_form="shop",
            targets="Sponsor this project",
            paymentType="SB",
            sum=150,
            )

print(quickpay.base_url)
print(quickpay.redirected_url)