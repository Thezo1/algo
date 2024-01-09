# This sample is provided for demonstration purposes only.
# It is not intended for production use.
# This example does not constitute trading advice.

# For a more verbose version of this example see swapping1_less_convenience.py

from tinyman.v1.pools import Pool
from tinyman.assets import Asset
from tinyman.utils import wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from tinyman.v1.client import TinymanTestnetClient
from algosdk import algod
import algosdk
# Hardcoding account keys is not a great practice. This is for demonstration purposes only.
# See the README & Docs for alternative signing methods.
seed ="mean real crush whale off bamboo winter spray bleak obscure south piano travel attend source predict pretty exhaust explain guide heavy day raw abandon cloth"
private_key = algosdk.mnemonic.to_private_key(seed)
print(private_key)

account = {
    'address': 'W56X7W2ANMOJANBIYKQ3G3EHNO7XPFULYWJDMA355R4THPPFYQUSC5LFSU',
    'private_key': private_key # Use algosdk.mnemonic.to_private_key(mnemonic) if necessary
}

client = TinymanTestnetClient(user_address=account['address'])
# By default all subsequent operations are on behalf of user_address

# Check if the account is opted into Tinyman and optin if necessary
if(not client.is_opted_in()):
    print('Account not opted into app, opting in now..')
    transaction_group = client.prepare_app_optin_transactions()
    transaction_group.sign_with_private_key('W56X7W2ANMOJANBIYKQ3G3EHNO7XPFULYWJDMA355R4THPPFYQUSC5LFSU', account['private_key'])
    result = client.submit(transaction_group, wait=True)
else :
    print('account opted in')

# Fetch our two assets of interest
USDC = client.fetch_asset(10458941)
ALGO = client.fetch_asset(0)

# Fetch the pool we will work with
pool = client.fetch_pool(USDC, ALGO)
print(pool)

# Get a quote for a swap of 1 ALGO to TINYUSDC with 1% slippage tolerance
quote = pool.fetch_fixed_input_swap_quote(ALGO(5), slippage=0.1)
print(quote)
print(f'USDC per ALGO: {quote.price}')
print(f'TINYUSDC per ALGO (worst case): {quote.price_with_slippage}')

qoute = pool.fetch_fixed_input_swap_quote(ALGO(5), slippage=0.1)
transaction_group = pool.prepare_swap_transactions_from_quote(qoute)
for i, txn in enumerate (transaction_group.transactions):
    if txn.sender == account['address']:
        transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
txid = .send_transactions(transaction_group.signed_transactions)
wait_for_confirmation(algod, txid)
# We only want to sell if ALGO is > 180 TINYUSDC (It's testnet!)

    # Check if any excess remaining after the swap
