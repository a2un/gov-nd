#import emailc.py
#import emailvalidator

import os,pandas as pd,pyzmail as pmail

import smtplib

#import imapclient

import getpass

# vars
smtpstr = 'smtp.gmail.com'
imapstr = 'imap.gmail.com'

corr_email = 'arun.balajiee.baci@gmail.com'

email_crawler = 'emailc.py'		#crawler script path and args
email_validator = 'emailvalidator.py' 	#validator script path and args

#emails_csv = 'email.csv'		#Actual file path
emails_csv  = 'testemails.csv'		#Test file path



MAIL_CONTENTS_FILE = 'mailcontents.csv'

def emailbot():
#	run_emailcrawler()

#	df = run_emailvalidator()

	usesmtpobj(smtpstr,"send",corr_email)

#	useimapobj(imapstr,"read")

def usesmtpobj(smtpConnstr, type,corr_email):

	smtpObj = connectsmtp(smtpConnstr)

	print smtpObj.ehlo()

	print smtpObj.starttls()

	print smtpObj.login(corr_email,getpass.getpass())

	if type == "send":

		mails_to = loadEmailIds()

	        mail_from = corr_email

		mail_contents = loadmailcontents()

		result = merge(mails_to,mail_contents,'inner')

# 		read from config file for this.
		for mail_to in result['email']:
			idx = [result.email == mail_to]
			smtpsendmail(smtpObj,mail_from,mail_to, result[idx].mail_content)

	killconnect(smtpObj)


def useimapobj(imapstr):
	pass

def smtpsendmail(smtpObj,mail_from,mail_to,mail_content):
	if smtpObj is not None:
		print 'sending email to ' + mail_to
		smtpObj.sendmail(mail_from, [mail_to],mail_content)

def smtpreadmail(imapObj):
	pass

def loadEmailIds():
	return pd.read_csv(emails_csv)

def loadmailcontents():
	return pd.read_csv(MAIL_CONTENTS_FILE)

def merge(mails_to,mail_contents,how):
	return pd.merge(mails_to,mail_contents,how=how)

def connectsmtp(str):
	obj = smtplib.SMTP(str,587)
	return obj

def killconnect(obj):
	if obj is not None:
		obj.quit()

def run_emailcrawler():
	print 'crawling the web...'
	os.system('python ' + email_crawler)
	print 'emails received'

def run_emailvalidator():
	print 'validating emails .. '
	print 'running validator script..'
	os.system('python ' + email_validator)
	print 'reading csv ..'
	df = pd.read_csv(emails_csv)
	return df

if __name__ == "__main__":
	emailbot()
