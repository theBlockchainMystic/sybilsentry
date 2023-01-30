# SybilSentry
the configuration for app
All values are present in config.json
"lookback_days": (int.) The no.of days from today we need to look back for past transaction of a given wallet (by deafult 30)
"api_key": The api key obtained from etherscan.io
"threshold": (int.) The percentage limit at which a given wallet is considered sybil (by deafult 100) don't keep it less than 75
Note in this the start time is considered the current time so if your are looking for transactions that happended way back in past like more than 2 weeks
you might not find them in the eth block
