import os
import csv
import datetime
import glob


def createFolder(directory):
    try:
        if not os.path.exists(directory):
            os.makedirs(directory)
    except OSError:
        print('Error: Creating directory. ' + directory)





def addData(filename,fieldnames,data):  # 데이터 생성 짜응 # len(data)==7
    with open(filename, 'a') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        info = {
            "TIME": data[0],  # 원래는 time 근데 학회 준비를 위해서
            "X": data[1],'Y': data[2],'Z': data[3]}
        csv_writer.writerow(info)
        csv_file.close()

def writeData(path,addr,fieldnames):
    date = datetime.datetime.now()

    path = os.path.abspath(path + '/Cam%s_%s-%s-%s' % (addr, date.year, date.month, date.day))
    createFolder(path)
    list_of_dir = glob.glob(path + "/*")

    path = os.path.abspath(path + '/session%s' % (len(list_of_dir)))
    createFolder(path)
    # 클라이언트가 접속을 끊을 때 까지 반복합니다.
    filename = os.path.join(path, 'Buffer_%s시%s분%s초.csv' % (
        date.hour, date.minute, date.second))
    with open(filename, 'w') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        csv_writer.writeheader()
    return filename