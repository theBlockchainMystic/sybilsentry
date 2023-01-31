from flask import Flask, request, jsonify
import requests
from datetime import datetime, timedelta
import time
import pandas as pd
import json
import numpy as np
from eth_abi import abi

app = Flask(__name__)

with open('config.json') as f:
    data = json.load(f)

apikey = data["api_key"]# Keep your api key in config.json

## threshold
try:
    threshold =  int(data["threshold"])
except:
    threshold = 100

## lookback_days
try:
    lookback_days = int(data["lookback_days"])
except:
    lookback_days = 30


## get_block num
def get_block(timestamp):
    r = requests.post(f"https://api.etherscan.io/api?module=block&action=getblocknobytime&timestamp={timestamp}&closest=before&apikey={apikey}")
    results=r.json()
    return results['result']


## Normal Transactions By Address
def feature_store(start_block_num,end_block_num,wallet_address):
    normal_trans = f"https://api.etherscan.io/api?module=account&action=txlist&address={wallet_address}&startblock={start_block_num}&endblock={end_block_num}&page=1&offset=10&sort=asc&apikey={apikey}"
    r = requests.post(normal_trans)
    print(wallet_address,r)
    results=r.json()
    #print(results['result'])
    if len(results['result'])>0:
        try:
            l=pd.DataFrame(results['result'])
        except:
            l=None
    else:
        l=None
    
    return l

## checks if wallets is used only for voting
def vote_only(start_block_num,end_block_num,source_wallets):
    results=[]
    print("###### Obtaining Wallet meta-data ######")
    for i in source_wallets:
        r=feature_store(start_block_num,end_block_num,i)
        if r is None:
            pass
        else:
            results.append(r)
    if len(results)>0:
        #print(results)
        temp_df=pd.concat(results)
        #print(temp_df)
        vl=list(temp_df[temp_df['functionName'].str.contains('vote')]['functionName'].dropna().unique())
        temp_df['classes'] = 1
        temp_df['classes']=temp_df['classes'].where(temp_df['functionName'].isin(vl),0)
        s1=pd.concat([temp_df.groupby(['from'])['classes'].count(),temp_df.groupby(['from'])['classes'].sum()],axis=1)
        s1=s1.reset_index()
        s1.columns = ['from','total','vote']
        s1['percent_vote'] = s1['vote']*100/s1['total']
        return list(s1[s1['percent_vote']==threshold]['from'].unique())
    else:
        return []

@app.route('/sybilsentry',methods=['POST'])
def pipe():
    inp_json = request.json
    if isinstance(inp_json['wallet id'], list):
        source_wallets = inp_json['wallet id']
    elif isinstance(inp_json['wallet id'], str):
        source_wallets = [inp_json['wallet id']]
    ## Wallet check
    present = datetime.now()
    window = timedelta(days=lookback_days) # Add how many days to lookback
    lookback = present - window
    start_epoch = int(present.timestamp())
    end_epoch = int(lookback.timestamp())
    start_block_num = get_block(start_epoch)
    end_block_num = get_block(end_epoch)
    votes_only = vote_only(start_block_num,end_block_num,source_wallets)
    result = {'result':[]}
    if len(source_wallets)==1:
        if source_wallets in votes_only:
            return jsonify({"Sybil":"True"})
        else:
            return jsonify({"Sybil":"False"})
    
    elif len(source_wallets)>1:
        for j in source_wallets:
            result['result'].append({'wallet id':str(j),'Sybil':'True' if j in votes_only else 'False'})
        return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)