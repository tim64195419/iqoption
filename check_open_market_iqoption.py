from iqoptionapi.stable_api import IQ_Option
import time
from datetime import datetime



error_password="""{"code":"invalid_credentials","message":"You entered the wrong credentials. Please check that the login/password is correct."}"""
Iq = IQ_Option("USER","PASSWORD")
check,reason=Iq.connect()


def calRate(rate):
    rate = 2/rate
    return round(rate,2)

ACTIVES = []
print(check)
if check:
    print("Start your robot")

    ALL_Asset=Iq.get_all_open_time()
    for i in ALL_Asset["turbo"]:
        if i in ["USDSGD-OTC","USDHKD-OTC","USDINR-OTC","NZDCAD","EURCAD","NZDJPY","USDNOK","CADCHF","USDCHF","AUDCAD"]:
            continue
        if ALL_Asset["turbo"][i]["open"]:
            ACTIVES.append(i)
print(ACTIVES)

f = open("open_market_check.txt","w")
for i in ACTIVES:
    f.write(i)
    f.write("\n")
f.close()
