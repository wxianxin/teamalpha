import gdax
public_client = gdax.PublicClient()


key = '65abde3cb4a08123ba7fd866f3b7e3d4'
b64secret = 'xeSbL2s/I3VyDQhUJfAGZEcDOTZl6FNkKkhKVTDEWuE8uBPe3xLhbeCh/jPXXIkJReX0oJGHz4ylscBNj//JsQ=='
passphrase = '634ch407i4'

auth_client = gdax.AuthenticatedClient(key, b64secret, passphrase,api_url="https://api-public.sandbox.gdax.com")
accounts = auth_client.get_accounts()

def get_account(currency):
    for account in accounts:
        if account['currency'].lower() == currency.lower():
            return account
    return None
btc_account = get_account('BTC')
usd_account = get_account('USD')

auth_client.buy(price='100.00', size='0.01', product_id='BTC-USD', post_only=True, type = 'limit')
print(auth_client.get_orders()[0][0])

