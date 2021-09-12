from iqoptionapi.stable_api import IQ_Option
import time
from datetime import datetime


error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
Iq = IQ_Option("USER","PASSWORD")
check,reason=Iq.connect()


def calRate(rate):
    rate = 2/rate
    return round(rate,2)


def check_win_result(id):
    while check:
        for i in Iq.get_optioninfo(20)['msg']['result']['closed_options']:
            if id == i["id"][0]:
                return i['win']

looseMoneyTotal = 1
Money=1
ACTIVES=""
ACTION="call"#or "put"
expirations_mode=1
result = ""
count = 0
maxOrder = 2000
orderCount = 0
print(check)
if check:
    print("Start your robot")
    d=Iq.get_all_profit()

    omc = open("open_market_check.txt","r")
    lines = omc.readlines()
    omc.close()

    ACTIVES = lines[0].split("\n")[0]
    del lines[0]
    nomc = open("open_market_check.txt","w+")
    for line in lines:
        nomc.write(line)
    nomc.close()

    crf = open("current_running_market.txt","r")
    lines = crf.readlines()
    crf.close()

    for line in lines:
        if line.strip("\n") == ACTIVES:
            print(ACTIVES," this market already exist!!! choise another market")
            ACTIVES = ""

    if ACTIVES != "":
        crf = open("current_running_market.txt","a")
        crf.write(ACTIVES+"\n")
        crf.close()

    orderMarketProfit = d[ACTIVES]["turbo"] 

    #if see this you can close network for test
    while looseMoneyTotal<=maxOrder and ACTIVES !="" and orderCount <=5:
        if Iq.check_connect()==False: ##detect the websocket is close
            print("try reconnect")
            check,reason=Iq.connect()
            if check:
                print("Reconnect successfully")
            else:
                if reason==error_password:
                    print("Error Password")
                else:
                    print("No Network")
        ### logic in here
        # if balance < 10000 can reset practice balance
        # iqoption.reset_practice_balance()
        # balance_type="PRACTICE" ## PRACTICE,REAL
        # Iq.change_balance(balance_type)
        # print(iqoption.get_balance())
 
        if count>20:
            diffSec = Iq.get_remaning(expirations_mode)
            if diffSec-0.5 > 0:
                time.sleep(diffSec-0.5)
            else:
                time.sleep(diffSec)
                print("diffsec: ",diffSec)
        if orderMarketProfit <= 0.64:
            print("Profit too low, only "+str(orderMarketProfit)+" ,wait higher profit")
            continue
        check,id=Iq.buy(round(Money,2),ACTIVES,ACTION,expirations_mode)
        d=Iq.get_all_profit()
        orderMarketProfit = d[ACTIVES]["turbo"]
        rate = 1

        if check:
            print("!buy!")
            rate = calRate(orderMarketProfit)
            result = check_win_result(id)
            print(result,rate,Money)
            orderCount = 0
        else:
            print("buy fail")
            result = "equal"
            orderCount = orderCount +1

        if result == "loose":
            count = count +1
            Money = Money*rate
            looseMoneyTotal = looseMoneyTotal+Money
            if ACTION == "call":
                ACTION = "put"
            else:
                ACTION = "call"
        elif result == "equal":
            pass
        elif result =="win":
            looseMoneyTotal = 1
            Money = 1
            count = 0
    ### Order money is too big order too big need record ,then restart
    if ACTIVES != "":
        if orderCount <=5:
            print("Order money is too big: ",Money)
            f = open("lose_market_order_too_big/"+ACTIVES,"a")

            f.write(str(datetime.now())+",")
            f.write(str(ACTIVES)+",")
            f.write(str(looseMoneyTotal-Money)+",")
            f.write(str(Money))
            f.write("\n")
            f.close()

        crf = open("current_running_market.txt","r")
        lines = crf.readlines()
        crf.close()

        nomc = open("current_running_market.txt","w")
        for line in lines:
            if line.strip("\n") != ACTIVES:
                nomc.write(line)
        nomc.close()
else:

    if reason=="[Errno -2] Name or service not known":
        print("No Network")
    elif reason==error_password:
        print("Error Password")


