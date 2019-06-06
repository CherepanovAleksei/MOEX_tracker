########settings#########
my_yandex_mail = 'your@yandex.mail'
yandex_pass = 'password'
send_to_email = my_yandex_mail
# https://www.finanz.ru/aktsii/*** - page for watching
kurs_url = 'https://www.finanz.ru/aktsii/Rostelecom_1'
# name of kurs (up to table)
kurs_name = r'Ростелеком - Курс акции - RUB - MOEX'
REQUEST_RATE = 60 #sec
# you can add old data
closed_days = []
print("Closed days: " + str(closed_days))
#########################
import smtplib
import requests
import re
import datetime

def send_email(sum1):
    print("Try to send email")
    title = "Intersection of charts!"
    msg = "In "+kurs_name+" charts have intersected with average amount:"+str(sum1)+".\n\nWatch site: "+kurs_url+"\n"
    server = smtplib.SMTP_SSL('smtp.yandex.ru', 465)
    server.ehlo()
    server.login(yandex_mail,yandex_pass)
    message = 'Subject: {}\n\n{}'.format(title,msg)
    server.sendmail(yandex_mail,send_to_email,message)
    server.quit()
    print('E-mails successfully sent!')

def get_price(kurs_url, kurs_name):
    request = requests.get(kurs_url)
    text = request.text
    pattern = re.compile('<th >\d+,\d*\s<span>RUB</span></th>')
    result = pattern.findall(text)
    num_list = result[0].split('>')[1].split(' ')[0].split(',')
    num_str = num_list[0]+'.'+num_list[1]
    num = float(num_str)
    print("Current price: " + num_str)
    return num

one_more_two_flag = False
day_open = False
current = 0;
while (True):
    t=datetime.datetime.now()
    if(datetime.time(10, 0, 0) < datetime.time(t.hour, t.minute, t.second) < datetime.time(18, 40, 0)): # work day
        current = get_price(kurs_url, kurs_name)
        sum1 = float(sum(closed_days[:4])+current)/5
        sum2 = float(sum(closed_days[:9])+current)/10
        print("sum(/5): " + str(sum1) + ". sum(/10): " + str(sum2))
        if(sum1 < sum2 and one_more_two_flag or sum1 > sum2 and not one_more_two_flag):
            send_email(sum1)
            one_more_two_flag = sum1 > sum2
        day_open = True
        time.sleep(REQUEST_RATE)
    else:
        if(day_open):
            print("Close day: " + str(current))
            closed_days = [current]+closed_days
            closed_days.pop()
            day_open = False
