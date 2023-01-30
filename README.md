# SybilSentry

This code is a Flask-based REST API that checks if a given Ethereum address is a "Sybil" address. A "Sybil" address is defined as an address that is used only for voting purposes, i.e., all transactions from the address are for voting operations.

The code takes a JSON input with a single key, wallet id, whose value is a list of Ethereum addresses. For each address, the code performs the following steps:

Calculates the start and end block numbers of a lookback window, which is defined as the number of days in the past to check for transactions. The lookback window size and the current time are defined in the code, and the current time is obtained using datetime.now().

Calls the vote_only function, which obtains the transactions of each address and determines if the address is used only for voting. The function calls the feature_store function to obtain the transactions of each address.

The vote_only function calculates the ratio of the number of voting transactions to the total number of transactions for each address. If this ratio is equal to a threshold defined in the code, then the address is considered to be used only for voting purposes.

The pipe function returns a JSON response indicating if the address is a Sybil address or not. If all transactions from an address are for voting operations, the response will be {"Sybil":"True"}, otherwise, it will be {"Sybil":"False"}.

The code uses the Etherscan API to obtain Ethereum transactions, and the requests library to make HTTP requests to the API. The Etherscan API requires an API key, which is stored in a config.json file. The pandas library is used to store and manipulate the transaction data.

--------------

the configuration for app

All values are present in config.json

"lookback_days": (int.) The no.of days from today we need to look back for past transaction of a given wallet (by default 30)

"api_key": The api key obtained from etherscan.io

"threshold": (int.) The percentage limit at which a given wallet is considered sybil (by deafult 100) don't keep it less than 75

Note in this the start time is considered the current time so if your are looking for transactions that happended way back in the past like more than 2 weeks you might not find them in the eth block
