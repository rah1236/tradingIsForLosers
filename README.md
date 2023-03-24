# tradingIsForLosers
A Coinbase Pro based trading algorithm that is completely (psuedo) random

#THIS MACHINE TURNS MONEY INTO DUST, ONLY INVEST WHAT YOU'RE WILLING TO LOSE

Dependencies:

 ```
pip install coinbasepro
 ```

coinbasepro is the most up to date version of a python wrapper for the coinbase api I could find. It's working so far.

You need to make your own 'scrt.py' file that contains the following variables:

* api_key
* api_secret
* passphrase 
* acct_id_ETH    
* acct_id_USD 

the first three are given to you by coinbase pro,
the latter 2 I scraped myself using the  ```auth_client.get_accounts() ``` method. 

All are strings.
