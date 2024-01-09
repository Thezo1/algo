from tinyman.v1.pools import Pool
from tinyman.assets import Asset
from tinyman.utils import wait_for_confirmation
from algosdk.v2client.algod import AlgodClient
from tinyman.v1.client import TinymanMainnetClient
from algosdk import algod
import algosdk

#put seed phrase without the comma sign
#paste address at address
seed =""

private_key = algosdk.mnemonic.to_private_key(seed)
address = ''
print(private_key)
print(address)
account = {
    'address': address,
    'private_key': private_key}
#api is testnet, change to TinymanMainnet if want to run on mainnet
client = TinymanTestnetClient(user_address=account['address'])

#paste token ID you want to swap, also change the tickers below from nurd to the token ticker
NURD= client.fetch_asset(330168845)
ALGO = client.fetch_asset(0)

pool = client.fetch_pool(ALGO, NURD)
print(pool)

#adjust slippage
quote = pool.fetch_fixed_input_swap_quote(ALGO(10_000_000), slippage=90)
print(quote)
print(f'NURD per ALGO: {quote.price}')
print(f'NURD per ALGO (worst case): {quote.price_with_slippage}')

if quote.price > 0:
    print(f'Swapping {quote.amount_in} to {quote.amount_out}')
    # Prepare a transaction group
    transaction_group = pool.prepare_swap_transactions(
        amount_in=quote.amount_in,
        amount_out=quote.amount_out,
        swap_type='fixed-input',
        swapper_address=account['address'],
    )
    for i, txn in enumerate(transaction_group.transactions):
        if txn.sender == account['address']:
            transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
    result = client.submit(transaction_group, wait=False)

    excess = pool.fetch_excess_amounts(account['address'])
    if NURD.id in excess:
        amount = excess[NURD.id]
        print(f'Excess: {amount}')
        if amount > 0:
            transaction_group = pool.prepare_redeem_transactions(amount, account['address'])
            # Sign the group with our key
            for i, txn in enumerate(transaction_group.transactions):
                if txn.sender == account['address']:
                    transaction_group.signed_transactions[i] = txn.sign(account['private_key'])
            result = client.submit(transaction_group, wait=False)
