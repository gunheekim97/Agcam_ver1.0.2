"""
나중에 로스를 통해서 데이터를 전송 받고 csv에 저장함.
"""

from modules.app_Tools import *

import datetime

import random
def genSample_Data():

    PATH = 'TEST'
    createFolder(PATH)
    fieldnames = ['TIME', 'X', 'Y', 'Z']
    addr = ['123']
    filename = writeData(PATH, addr[0], fieldnames)
    startTime = datetime.datetime.now()
    print(startTime)
    print(startTime.second + 10)
    while True:
        time = datetime.datetime.now()

        x = random.uniform(-5, 5)
        y = random.uniform(-5, 5)
        z = random.uniform(-5, 5)
        data = [time,x,y,z]
        print(data)
        addData(filename, fieldnames, data)
        if startTime.second+10 == time.second:
            print('end')
            break


    return
# genSample_Data()