from selenium import webdriver
from datetime import date
from dotenv import load_dotenv
from pathlib import Path
import logging
import smtplib
import os


# TODO:
# add comments
# Automate using lambda functions


def send_email(SENDER_EMAIL,sender_pass, receiver_email, email_text):
	# creates SMTP session 
	s = smtplib.SMTP('smtp.gmail.com', 587) 
	  
	# start TLS for security 
	s.starttls() 
	  
	# Authentication 
	s.login(SENDER_EMAIL, sender_pass)
	  
	# sending the mail 
	s.sendmail(SENDER_EMAIL, receiver_email, email_text) 
	  
	# terminating the session 
	s.quit()

	return None

# loading in environment vars
env_path = Path('.') / '.env'
load_dotenv(dotenv_path=env_path)



def main():
	# Constants
	URL = "https://www.vineyardvines.com/womens-pants/americana-flag-print-leggings/2P001084.html?dwvar_2P001084_color=3879#q=leggings&start=8&cgid=&format=ajax&dgrqt=true&dwvar_2P001084_color=3879"
	SENDER_EMAIL = os.environ['SENDER_EMAIL']
	sender_pass = os.environ['SENDER_PASSWORD']
	SUCCESS_RECEIVER_EMAIL = os.environ['RECEIVER_EMAIL']
	FAIL_RECEIVER_EMAIL = os.environ['SENDER_EMAIL']
	SUBJECT = 'Update on your Vineyard Vines leggings'
	SUCCESS_BODY = f'I have found your vineyard vines leggings in size Small! Please visit {URL}'
	FAIL_BODY = 'I was unable to find the vineyard vines leggings :( I will try again soon.'
	PATH = "C:\Program Files (x86)\chromedriver.exe"
	# Variables
	found_size = False
	today = date.today()
	fail_email_text = """\
	From: %s
	To: %s
	SUBJECT: %s

	%s
	""" % (SENDER_EMAIL, FAIL_RECEIVER_EMAIL, SUBJECT, FAIL_BODY)
	success_email_text = """\
	From: %s
	To: %s
	SUBJECT: %s

	%s
	""" % (SENDER_EMAIL, SUCCESS_RECEIVER_EMAIL, SUBJECT, SUCCESS_BODY)
	# Speciyfing to use the chrome driver
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
			send_email(SENDER_EMAIL, sender_pass, SUCCESS_RECEIVER_EMAIL, success_email_text)

	logging.info(f'Closing out of web browser')
	driver.quit()

	if found_size == False:
		print(f'Did not find your size on {today}. Will try again in an hour')
		logging.info(f'Did not find your size on {today}. Will try again in an hour')
		send_email(SENDER_EMAIL, sender_pass, FAIL_RECEIVER_EMAIL, fail_email_text)

if __name__ == '__main__':
	main()



