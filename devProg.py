#!/usr/bin/env python3
import json
import requests
import sys


SANDBOX_TOKEN = "<TOKEN_HERE>"  # Replace with your actual sandbox token
SANDBOX_ACCOUNT = <SANDBOX_ACCOUNT>  # Replace with your actual sandbox account number"

def get_quotes(symbols):
    response = requests.post('https://sandbox.tradier.com/v1/markets/quotes',
    data={'symbols': {symbols}, 'greeks': 'true'},
    headers={'Authorization': f'Bearer {SANDBOX_TOKEN}', 'Accept': 'application/json'}
)

    try: 
        result = response.json()
    except Exception as e:
        print (e)
        print(response.text)
        sys.exit(1)

    json_formatted_str = json.dumps(result, indent=2)
    print("Get Quotes Status: {}".format(response.status_code))
    return(json_formatted_str)

def get_chain(symbol, expiration):
    response = requests.get('https://sandbox.tradier.com/v1/markets/options/chains',
        params={'symbol': f'{symbol}', 'expiration': f'{expiration}','greeks': 'true'},
        headers={'Authorization': f'Bearer {SANDBOX_TOKEN}', 'Accept': 'application/json'}
    )

    try: 
        json_response = response.json()
    except Exception as e:
        print (e)
        print(response)
        print(response.text)
        sys.exit(1)

    print("Get Chains Status: {}".format(response.status_code))

    try:
        options_dicts = json_response['options']['option']
    except Exception as e:
        print (e)
        print(json_response)
        sys.exit(1)

    return(options_dicts)
    

def placeOrder(payload):
    response = requests.post(f'https://sandbox.tradier.com/v1/accounts/{SANDBOX_ACCOUNT}/orders',
        data = payload,
        headers = {'Authorization': f'Bearer {SANDBOX_TOKEN}', 'Accept': 'application/json'}
    )
    try: 
        result = response.json()
    except Exception as e:
        print ("Error: {}".format(e))
        print(response)
        print(type(response))
        print("Status: {} -- {}".format(response.status_code, response.text))
        sys.exit(1)

    print(result)

    try:
        ORDERNUM = result['order']['id']
    except Exception as e:
        print ("Error: {}".format(e))
        sys.exit(1)

    # Get the actual order status
    response = requests.get(f'https://sandbox.tradier.com/v1/accounts/{SANDBOX_ACCOUNT}/orders/{ORDERNUM}',
        params={'includeTags': 'true'},
        headers={'Authorization': f'Bearer {SANDBOX_TOKEN}', 'Accept': 'application/json'}
    )

    try: 
        json_response = response.json()
        json_formatted_str = json.dumps(json_response, indent=2)
    except Exception as e:
        print (e)
        print(response)
        print(response.text)
        sys.exit(1)

    print(response.status_code)
    print(json_formatted_str)


if __name__ == "__main__":
    # Example usage
    symbols = 'AAPL'
    expiration = '2025-06-20'
    
    # Get quotes for the symbol
    quotes = get_quotes(symbols)
    print(quotes)

    # Get options chain for the symbol
    options_chain = get_chain(symbols, expiration)
    print(options_chain)

    # Place an order
    PAYLOAD = {'class': 'equity', 'symbol': symbols,'side': 'buy', 'quantity': '1', 'type': 'market','duration': 'day', 'preview': 'false'}
    placeOrder(PAYLOAD)