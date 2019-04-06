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
#########################
import smtplib
import requests
import re
import time

def send_email(sum1):
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
	num_str = a[0]+'.'+a[1]
	num = float(num_str)
	print("Num: " + num_str)
	return num

one_more_two_flag = False
while (True):
    t=datetime.datetime.now()
    if(datetime.time(10, 0, 0) < datetime.time(t.hour, t.minute, t.second) < datetime.time(18, 40, 0)): # work day
	    current = get_price()
	    sum1 = float(sum(a[:4]+current))/5
	    sum2 = float(sum(a[:9]+current))/10
	    if(sum1 < sum2 and one_more_two_flag or sum1 > sum2 and not one_more_two_flag):
	    	send_email(sum1)
	    	one_more_two_flag = sum1 > sum2
	    time.sleep(REQUEST_RATE)
	

	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	
	