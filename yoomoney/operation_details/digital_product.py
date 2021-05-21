

class DigitalProduct:
    def __init__(self,
                 merchant_article_id: str,
                 serial: str,
                 secret: str
                 ):
        self.merchant_article_id = merchant_article_id
        self.serial = serial
        self.secret = secret
