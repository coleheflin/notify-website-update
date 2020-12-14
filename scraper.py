from selenium import webdriver
from datetime import date
import logging
import smtplib


# TODO:
# set up env vars for gmail accounts, password, client secret/token
# Create email templates for when bot fails/succeeds to find the size
# add comments
# Automate using lambda functions


def send_email(sender_email,sender_pass, receiver_email, email_text):
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(sender_email, sender_pass)
	  
	# sending the mail 
	s.sendmail(sender_email, receiver_email, email_text) 
	  
	# terminating the session 
	s.quit()

	return None




# sender_email = "reginald.botlington@gmail.com"
# sender_pass = ''
# receiver_email = "sosinclair10@gmail.com"
# subject = 'Botlington at your service'
# body = 'Hello! I will be sending you emails regarding updates to the vineyard vines leggings.'
# email_text = """\
# From: %s
# To: %s
# Subject: %s

# %s
# """ % (sender_email, receiver_email, subject, body)

# send_email(sender_email, sender_pass, receiver_email, email_text)


found_size = False
today = date.today()
PATH = "C:\Program Files (x86)\chromedriver.exe"
URL = "https://www.vineyardvines.com/womens-pants/americana-flag-print-leggings/2P001084.html?dwvar_2P001084_color=3879#q=leggings&start=8&cgid=&format=ajax&dgrqt=true&dwvar_2P001084_color=3879"
driver = webdriver.Chrome(PATH)

logging.info(f'Connecting to {URL}')
driver.get(URL)

logging.info(f'Finding all elements with class name "available"')
list_of_sizes = driver.find_elements_by_class_name('available')

logging.info(f'Looping through all available sizes')
for size in list_of_sizes:
	print(size)
	if size == 'S':
		found_size = True
		print('Found your size! Sending email to notify.')
		logging.info(f'Found correct size! Sending email to notify.')

logging.info(f'Closing out of web browser')
driver.quit()

if found_size == False:
	print(f'Did not find your size on {today}. Will try again in an hour')
	logging.info(f'Did not find your size on {today}. Will try again in an hour')
