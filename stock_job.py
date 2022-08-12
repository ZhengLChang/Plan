import mail
import time
import datetime
from  stock_base import Stock_Base


def IsNow(hour, minute):
    now = datetime.datetime.now()
    if now.hour == int(hour) and now.minute == int(minute):
        return True
    return False

isFirst = True
try:
    #if not isFirst and not IsNow(20, 55):
    #    print("Not now, will retry")
    #    time.sleep(20); 
    #    continue
    isFirst = False
    t1 = time.time()
    obj = Stock_Base()
    convertible_list = obj.get_all_convertible()
    t2 = time.time()
    dump_arr = []
    dump_arr.append(f"Running exe spend time: {t2 - t1}\n")
    dump_arr.append(f"Count: {len(convertible_list)}\n")
    for stock_name, notice in convertible_list:
        dump_arr.append(f"{stock_name}: {notice}\n")
    mail.sentemail('mail subject', dump_arr)
except Exception as err:
    print(f"[Exception] [get_stocks_number] {traceback.format_exc()}")
    mail.sentemail('mail subject', [f"[Exception] [get_stocks_number] {traceback.format_exc()}"])
    time.sleep(3600);

