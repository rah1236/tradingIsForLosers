import coinbasepro
import time
import random
from scrt import *

public_client = coinbasepro.PublicClient()
auth_client =   coinbasepro.AuthenticatedClient(api_key,api_secret,passphrase)



orderCompletePeriod = 10 #number of seconds to wait before checking api if order is complete
loopPeriod = 60         #number of seconds to wait for going thru the whole loop

loopEnable = True        #toggles trading loop


lastBuySize = 0
lastSellSize = 0
buySize = 0
sellSize = 0

lastSellPrice = 0
lastBuyPrice = 0
buyPrice = 0
sellPrice = 0

productID = 'ETH-USD'

def getNewSeed():
    return random.randint(1349,1473891543759432)

def getETHBalance():
    return (auth_client.get_account(acct_id_ETH)['available'])

def getUSDBalance():
    return((auth_client.get_account(acct_id_USD)['available']))

# list = auth_client.get_accounts()

# for thing in list:
#     print(thing)

while loopEnable:
    random.seed(getNewSeed())

    USDBalance = getUSDBalance()
    ETHBalance = getETHBalance()

    print("Current ETH Balance: {}".format(ETHBalance))
    print("Current USD Balance: ${}".format(USDBalance))

    ticker = public_client.get_product_ticker(productID)
    buyPrice = float(ticker['price'])
    sellPrice = float(ticker['price'])


    if (random.choice([True,False]) and USDBalance < 125.0 and USDBalance > 10.0): #buying
        buySize = round(random.uniform(0.003, 0.02),5) #coinbase gets upset if you try to have more accuracy than 1e-8
        while(buySize*buyPrice > USDBalance):
            buySize = round(random.uniform(0.003, 0.02),5)
        print('Buying {} ETH at ${} per Eth. (${})'.format(buySize, buyPrice, float(buyPrice)*float(buySize)))
        buy_order = auth_client.place_limit_order(product_id=productID, side='buy', price=buyPrice, size=buySize)
        if (auth_client.get_order((buy_order['id']))['filled_size'] > 0):#auth_client.get_order((buy_order['id']))['status'] == 'done'): #this is fucking ratchet
             print()
             print('!!BOUGHT {} ETH at ${} per Eth. (${})'.format(buySize, buyPrice, round(float(buyPrice)*float(buySize),2)))
             lastBuyPrice = buyPrice
             lastBuySize = buySize
        else:
            while(auth_client.get_order((buy_order['id']))['filled_size'] <= 0):
                print("waiting for buy order to complete")
                time.sleep(orderCompletePeriod)
            print()
            print('!!Bought {} ETH at ${} per Eth. (${})'.format(buySize, buyPrice, round(float(buyPrice)*float(buySize),2)))
            lastBuyPrice = buyPrice
            lastBuySize = buySize
    else:
        print("Balance is too high/low: it's currently sitting at ${}".format(USDBalance))
    
    if(random.choice([True,False])): #selling
        sellSize = round(random.uniform(0.005, 0.02), 5)
        if (sellSize < getETHBalance()):
            print('Selling {} ETH at ${} per Eth. (${})'.format(sellSize, sellPrice, float(sellPrice)*float(sellSize)))
            sell_order = auth_client.place_limit_order(product_id=productID, side='sell', price=sellPrice, size=sellSize)
            if (auth_client.get_order((sell_order['id']))['filled_size'] > 0): #this is fucking ratchet
                print()
                print('!!SOLD {} ETH at ${} per Eth. (${})'.format(sellSize, sellPrice, round(float(sellPrice)*float(sellSize),2)))
                lastBuyPrice = buyPrice
                lastBuySize = buySize
            else:
                while(auth_client.get_order((sell_order['id']))['filled_size'] <= 0):
                    print("waiting for sell order to complete")
                    time.sleep(orderCompletePeriod) #self rate limitting, dont want to sell my whole account
                print()
                print('!!SOLD {} ETH at ${} per Eth. (${})'.format(sellSize, sellPrice, round(float(sellPrice)*float(sellSize),2)))
                lastSellPrice = sellPrice
                lastBuySize = sellSize
    
    time.sleep(loopPeriod) 
        

