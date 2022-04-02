import os
import requests

from bs4 import BeautifulSoup
from ftplib import FTP


tags_url = "https://qrcodes.360tv.ru/tags/"

tags_source = requests.get(tags_url, auth=("", "")).text

soup = BeautifulSoup(tags_source, features="html.parser")

tags = soup.find_all("a")

qr_quantity = int(input("Сколько нужно qr-кодов для стрима?(максимум 9)\n"))


def get_link(tags, qr_name, qr_num):

    while True:

        qr_link = False

        for tag in tags:
            if qr_name in str(tag):

                qr_link = "https://qrcodes.360tv.ru/tags/"+str(tag).split(r'"')[1]

                qr_dict[qr_name] = qr_link

        if qr_link:
            return qr_link
        else:
            print("QR-код " + qr_name + " отсутствует на сайте")
            qr_name = input("Напишите qr-код N" + str(qr_num) + "(писать с #)\n")


qr_dict = {}


def cycle_get_names(qr_quantity, iter=1):

    for qr_num in range(iter, qr_quantity+1):

        qr = input("Напишите qr-код N"+str(qr_num)+"(писать с #)\n")

        get_link(tags, qr_name=qr, qr_num=qr_num)


cycle_get_names(qr_quantity)


new_qr_dict = {}

qr_names = ["2221", "2222", "2223", "2224", "2225", "2226", "2227", "2228", "2229"]


for i in range(len(qr_dict)):
    new_qr_dict[qr_names[i]] = qr_dict.get(list(qr_dict.keys())[i])

ftp_karrera = FTP('')
ftp_karrera.login()
ftp_karrera.cwd("SUITE1/qr/")

for qr_name, qr_link in new_qr_dict.items():
    img_data = requests.get(qr_link,  auth=("", "")).content

    with open(qr_name, 'wb') as handler:
        handler.write(img_data)

        ftpCommand = "STOR "+qr_name+".png"
        fpFile = open(qr_name, "rb")
        ftp_karrera.storbinary(cmd=ftpCommand, fp=fpFile)  # send the file
        fpFile.close()
        handler.close()  # close file and FTP
    os.remove(qr_name)
ftp_karrera.quit()
