from iqoptionapi.stable_api import IQ_Option
import logging
from time import sleep
from datetime import datetime
from multiprocessing import Pool


logging.basicConfig(level=logging.CRITICAL,format='%(asctime)s %(message)s')

choice = {'USDCHF-OTC': 0.8, 'USDCAD': 0.78, 'GBPCHF': 0.8, 'CADCHF': 0.8, 'GBPNZD': 0.8,
          'USDJPY': 0.8, 'GBPUSD-OTC': 0.8, 'GBPAUD': 0.8, 'CHFJPY': 0.8, 'EURAUD': 0.8,
          'EURNZD': 0.8, 'EURCAD': 0.8, 'NZDUSD-OTC': 0.8, 'GBPUSD': 0.8, 'EURUSD': 0.8,
          'GBPJPY': 0.8, 'USDCHF': 0.8, 'EURUSD-OTC': 0.8, 'EURGBP-OTC': 0.8, 'AUDJPY': 0.8,
          'CADJPY': 0.8, 'EURCHF': 0.8, 'EURGBP': 0.8, 'AUDCAD': 0.8, 'NZDUSD': 0.8,
          'AUDCAD-OTC': 0.8, 'GBPCAD': 0.8, 'EURJPY': 0.8, 'AUDUSD': 0.77}

MAXBET_results = 0
Max_bet_amount_limit_results = 0
win_count_results = 0
loose_count_results = 0


print('Login info')
ID = input('Account: ')
PW = input('Password: ')

timess = input('Run times: ')
Max_bet_amount_limit_set = input('Max bet limits: ')

print('login..')

I_want_money = IQ_Option(ID + "@gmail.com", PW)
#connect to iqoption
I_want_money.connect()
start_time_results = datetime.fromtimestamp(I_want_money.get_server_timestamp() + 3600 * 8)


I_want_money.change_balance('REAL')

start_balance_results = I_want_money.get_balance()
print(start_balance_results)
# get_all_open_time for choice array
ALL_Asset = dict
d = dict





def run(choice_market):
    I_want_money = IQ_Option(ID + "@gmail.com", PW)
    I_want_money.connect()
    # I_want_money.change_balance('PRACTICE')
    I_want_money.change_balance('REAL')
    start_balance = I_want_money.get_balance()

    print('Account: %s , balance: %s' % (ID, start_balance))
    start_time = datetime.fromtimestamp(I_want_money.get_server_timestamp() + 3600 * 8)
    print(start_time)

    final = False
    loose_count = 0
    win_count = 0
    loose_times = 0
    running = True
    count = 0
    Money = 1
    MAXBET = 0
    ACTION = "put"
    ACTIVES=''
    value = ''
    count_put = 0
    count_call = 0
    # bet times
    global timess, Max_bet_amount_limit_set
    times = int(timess)
    Max_bet_amount_limit = int(Max_bet_amount_limit_set)


    # 計算當前profits的倍率
    max_open_market = {}
    open_market = []

    def append_market_to_choice():
        global ALL_Asset
        global d
        ALL_Asset = I_want_money.get_all_open_time()
        d = I_want_money.get_all_profit()
        # store open market in d=[]
        for market, value in d.items():
            for type, profit in value.items():
                if type == 'turbo':
                    choice[market] = profit
                    pass
        # print(choice)
        for market_key in list(choice):
            if ALL_Asset["turbo"][market_key]["open"] != True:
                del choice[market_key]
        # print(choice)
        for _ in range(3):
            max_market = max(choice, key=choice.get)
            max_open_market.update({max_market: choice[max_market]})
            del choice[max_market]
        for x in max_open_market.keys():
            open_market.append(x)

        print(max_open_market)
        # print(open_market)

    append_market_to_choice()

    # 每隔一個時段檢查現在市場的profits是否正確。
    def check_market_status(number):
        global ALL_Asset
        global d
        ALL_Asset = I_want_money.get_all_open_time()
        d = I_want_money.get_all_profit()
        # store open market in d=[]
        for market, value in d.items():
            for type, profit in value.items():
                if type == 'turbo':
                    choice[market] = profit
                    pass
        # print(choice)
        for market_key in list(choice):
            if ALL_Asset["turbo"][market_key]["open"] != True:
                del choice[market_key]

        number = number - 1
        a = open_market[number]
        # print(a)
        for key, value in max_open_market.items():
            # print(key)
            if key == a:
                if choice.get(a) == value:
                    return True
                else:
                    return False

    # high profits
    def cal_profits_multiple(profits):
        if profits <= 0.7:
            x = 1 / profits
            x = x + 1
        else:
            x = 2 / profits

        return round(x, 3)


    def find_max_profit_market(number):
        number = number - 1
        a = open_market[number]
        # print(a)
        for key, value in max_open_market.items():
            # print(key)
            if key == a:
                b = value
                return a, b

    # check order ID win or loose
    def check_order_info():
        check_id = True
        # c_count 檢查是否有市場重複下單，若有則重新尋找新的市場
        c_count = 1
        while check_id:
            results = I_want_money.get_optioninfo(5)
            results = results.get('msg')
            results = results.get('result')
            results = results.get('closed_options')
            # results[number] is 查找最近第幾筆歷史交易紀錄
            results0 = results[0]
            results1 = results[1]
            results2 = results[2]

            if [id_list_1[1]][0] in results0.get('id'):
                check_id = False
                results = results0
            elif [id_list_1[1]][0] in results1.get('id'):
                check_id = False
                results = results1
            elif [id_list_1[1]][0] in results2.get('id'):
                check_id = False
                results = results2

        print('=====' * 20)


        if results['amount'] == results['win_amount']:
            print('results : equal')
            print('done..')
            print('=====' * 20)
            return 'equal'
        else:
            print('results : %s' % results['win'])
            print('done..')
            print('=====' * 20)
            return results['win']


    def check_order_results(value, loose_count, loose_times, Money, multiple, Max_bet_amount_limit, times, ACTION,
                            win_count, running, count_call, count_put, profit):

        if value == 'loose':
            # count loose 次數
            loose_count = loose_count + 1
            loose_times = loose_times + 1

            if ACTION == 'put':
                count_call = count_call+1
            else:
                count_put = count_put+1
            Money = format(Money * multiple, '.3f')
            # 限制 Max_bet_amount_limit 最大下注金額,超過MAXBET金額則離開
            if float(Money) >= Max_bet_amount_limit:
                # running = False
                print('Now betAmount:', Money, '$ is too large, please STOP!!!!')
                Money = 1


            # 測試最後一次是否win?,若是loose且 < MAXBET,則for loop繼續直到獲勝結束
            if x == times - 1:
                times = 2
                # if loose_times == 5 or loose_times == 8:
                #     sleep(57)
                if ACTION == "put":
                    ACTION = "call"
                else:
                    ACTION = "put"

            else:
                if ACTION == "put":
                    ACTION = "call"
                else:
                    ACTION = "put"

        elif value == 'win':
            loose_times = 0
            win_count = win_count + 1

            if ACTION == 'call':
                count_call = count_call+1
            else:
                count_put = count_put+1

            # if x == times -1 --> 如果最後一次win 則離開迴圈完成running
            if x == times - 1:
                running = False
            else:
                Money = 1
        # if equals
        else:
            if x == times - 1:
                times = 2
        # 每兩分鐘下單一次，無論輸贏

        print('win: %s , loose: %s' % (win_count, loose_count))
        return loose_count, loose_times, Money, multiple, Max_bet_amount_limit, times, ACTION, win_count, running, count_call, count_put

    # 自動下單，每次整點下單
    try:
        while True:
            times = times + 1
            print('=====' * 20)
            print('Start....')
            ACTIVES, profit = find_max_profit_market(choice_market)
            multiple = float(format(cal_profits_multiple(profit), '.2f'))
            print('Now Trading market:[%s], Profit: %s , Multiple: %s' % (ACTIVES, profit, multiple))
            firstBet = True
            while running:
                from multiprocessing import Lock
                lock = Lock()
                for x in range(1, times):
                    count = count + 1
                    print('\n')
                    print('Start...')
                    print('ROUND : %s' % count)
                    timestamp = I_want_money.get_server_timestamp()
                    dt_object = datetime.fromtimestamp(timestamp)
                    dt_object = dt_object.second
                    print('=====' * 20)
                    wait = 60
                    wait = wait - dt_object
                    if float(Money) <= Max_bet_amount_limit:
                        if firstBet:
                            print('ready... BetAmount : ', Money)
                            print('wait %d sec to order' % wait)
                            if dt_object >= 55:
                                sleep(57)
                                pass
                            else:
                                sleep(wait - 2)
                                pass
                            firstBet = False
                        else:
                            print('ID matching...')

                            print('ready...   BetAmount : %s $' % Money)
                            print('\n')
                    else:
                        return win_count, loose_count, MAXBET, Max_bet_amount_limit

                    print('order..   direction:', ACTION)
                    # expirations_mode :0 為turbo
                    expirations_mode = 0
                    Money = float(Money)

                    # 下單
                    lock.acquire()
                    id_list_1 = I_want_money.buy(Money, ACTIVES, ACTION, expirations_mode)
                    lock.release()
                    print(id_list_1)

                    # 紀錄MAXBET
                    if Money > MAXBET:
                        MAXBET = Money

                    if id_list_1[1]:
                        print("check result only  id : %s" % id_list_1[1])
                    else:
                        pass

                    # check trading market & profits info
                    if x % 5 == 0:
                        if check_market_status(choice_market):
                            print('good market to be continue...')
                            pass
                        else:
                            append_market_to_choice()
                            ACTIVES, profit = find_max_profit_market(choice_market)
                            multiple = float(format(cal_profits_multiple(profit), '.2f'))
                            print('\n')
                            print('Time to check marketing info ')
                            print('Now Trading market:[%s], Profit: %s , Multiple: %s' % (ACTIVES, profit, multiple))

                    # get value = win or loose

                    while True:
                        I_want_money.connect()
                        if id_list_1[0] == True:
                            value = check_order_info()
                        # value = 'win'
                        elif id_list_1[0] == False:
                            while True:
                                lock.acquire()
                                id_list_1 = I_want_money.buy(Money, ACTIVES, ACTION, expirations_mode)
                                lock.release()
                                if id_list_1[0] == True:
                                    print("afresh check result only  id : %s" % id_list_1[1])
                                    value = check_order_info()
                                    if value == 'win' or value == 'loose' or value == 'equal':
                                        break

                        if value == 'win' or value == 'loose' or value == 'equal':
                            break


                    print('check order results...')
                    lock.acquire()
                    loose_count, loose_times, Money, multiple, Max_bet_amount_limit, times, ACTION, win_count, running, count_call, count_put = check_order_results(
                        value, loose_count, loose_times, Money, multiple, Max_bet_amount_limit, times, ACTION, win_count, running, count_call, count_put, profit)
                    lock.release()
                    if running == False:
                        break
            final = True
            break
    finally:
        if final:
            print('finish..')
        else:
            print('This processing has something wrong then terminal, now trading market is ', ACTIVES)

        # results info with running time , profits
        end_time = datetime.fromtimestamp(I_want_money.get_server_timestamp() + 3600 * 8)

        print('Start time %s' % start_time)
        print('Finish time %s' % end_time)
        print('Max Bet Amount:', MAXBET, '$')

        total_running_time = end_time - start_time
        print('Total Running Time:%s' % total_running_time)
        rate = win_count / (win_count + loose_count)
        rate = format(float(rate) * 100, '.2f')
        print('Rate: %s ' % rate)
        # time need change type to string data
        start_time = str(start_time)
        end_time = str(end_time)
        total_running_time = str(total_running_time)
        rate = float(rate)
        p_row = [start_time, end_time, total_running_time, MAXBET,
               Max_bet_amount_limit, win_count, loose_count, rate]
        print(p_row)

        return win_count, loose_count, MAXBET, Max_bet_amount_limit


get_return_value = []
try:
    if __name__ == '__main__':
        with Pool(5) as p:
            get_return_value.append(p.map(run, [1, 2, 3]))
            print(get_return_value)
            # 分解 get_return_value data to counting win or loose count ..
            for x in get_return_value:
                for y in x:
                    for z, r in enumerate(y):
                        if r:
                            if z == 0:
                                win_count_results = win_count_results + r
                            elif z == 1:
                                loose_count_results = loose_count_results + r
                            elif z == 2:
                                if MAXBET_results <= r:
                                    MAXBET_results = r
                            elif z == 3:
                                Max_bet_amount_limit_results = r

finally:

    I_want_money = IQ_Option(ID + "@gmail.com", PW)
    I_want_money.connect()
    end_time_results = datetime.fromtimestamp(I_want_money.get_server_timestamp() + 3600 * 8)

    total_running_time_results = end_time_results - start_time_results
    total_running_time_results = str(total_running_time_results)
    sleep(5)
    end_balance = I_want_money.get_balance()

    total_profit_results = format(float(end_balance) - float(start_balance_results), '.2f')
    total_profit_results = float(total_profit_results)
    rate_results = win_count_results / (win_count_results + loose_count_results)
    rate_results = format(float(rate_results) * 100, '.2f')


    start_time_results = str(start_time_results)
    end_time_results = str(end_time_results)
    row = [start_time_results, end_time_results, start_balance_results, end_balance, total_running_time_results,
           total_profit_results, MAXBET_results, Max_bet_amount_limit_results, win_count_results, loose_count_results,
           rate_results]
    print('------' * 5)
    print('final...')
    print(row)

