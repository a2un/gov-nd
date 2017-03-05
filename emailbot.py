#import emailc.py
#import emailvalidator

import os,sys,pandas as pd,pyzmail as pmail

import smtplib

import imapclient

import getpass

STANDARD_EMAIL_ID  = 'arun.balajiee.baci@gmail.com'
TEST_EMAILS_FILE   = 'testemails.csv'
MAIL_CONTENTS_FILE = 'mailcontents.csv'
NUMBER_OF_ARGS     = 5
MIN_NUMBER_OF_ARGS = 2

# vars
smtpstr = 'smtp.gmail.com'
imapstr = 'imap.gmail.com'

corr_email = STANDARD_EMAIL_ID if(sys.argv is None or len(sys.argv)<NUMBER_OF_ARGS) else sys.argv[2]

email_crawler = 'emailc.py'											#crawler script path and args
email_validator = 'emailvalidator.py' 										#validator script path and args

#emails_csv = 'email.csv'											#Actual file path
emails_csv  = TEST_EMAILS_FILE if(sys.argv is None or len(sys.argv)<NUMBER_OF_ARGS) else sys.argv[3]		#Test file path

MAIL_CONTENTS_FILE = MAIL_CONTENTS_FILE if(sys.argv is None or len(sys.argv)<NUMBER_OF_ARGS) else sys.argv[4]  #MAIL_CONTENTS



def emailbot():
#	run_emailcrawler()

#	df = run_emailvalidator()
	print sys.argv
	if sys.argv is not None and len(sys.argv)>=MIN_NUMBER_OF_ARGS and sys.argv[1] == "send":
		usesmtpobj(smtpstr,"send",corr_email)
	if sys.argv is not None and len(sys.argv)>=MIN_NUMBER_OF_ARGS and sys.argv[1] == "read":
		useimapobj(imapstr,"read",corr_email)

def usesmtpobj(smtpConnstr, type,corr_email):
	try:
		smtpObj = connectsmtp(smtpConnstr)

		print smtpObj.ehlo()

		print smtpObj.starttls()

		print smtpObj.login(corr_email,getpass.getpass("Email Password:"))

		if type == "send":

			mails_to = loadEmailIds()
	
		        mail_from = corr_email
	
			mail_contents = loadmailcontents()
	
			result = pd.merge(mails_to,mail_contents)

# 			read from config file for this.
			for idx in range(0,len(result)):
				try:
#					print 'mail\'s content: ' + result.mail_content[idx]
					smtpsendmail(smtpObj,mail_from,mails_to.email[idx], result.mail_content[idx])
				except ValueError,error:
					print 'Value Error occured %s' ,error
#					killconnect(smtpObj)

		killconnect(smtpObj)
	except smtplib.SMTPAuthenticationError,error:
		print str(error) + 'occured'

def useimapobj(imapstr,type,corr_email):
	imapObj = imapclient.IMAPClient(imapstr,use_uid=True, ssl=True)
	imapObj.login(corr_email,getpass.getpass("Email Password:"))

	inbox_details = imapObj.select_folder('INBOX',readonly=True)
	print('%d messages in INBOX' % inbox_details['EXISTS'])

	UIDS = imapObj.search(['FROM','arun.balajiee.baci@gmail.com'])

	print("%d messages that aren't deleted" % len(UIDS))
	
#	print UIDS
	
	rawMessages = imapObj.fetch(UIDS,['BODY[]','FLAGS'])

	for items in rawMessages:
#		print items
		message = pmail.PyzMessage.factory(rawMessages[items]['BODY[]'])

		print	'subject' + message.get_subject()
		for mails_from in message.get_addresses('from'):
			if mails_from is not None:
				print 	'from %s'% (mails_from,)
		for mails_to   in message.get_addresses('to'):
			if mails_to is not None:
				print 	'to %s'%(mails_to,)

		if message.text_part.charset is not None:
			print message.text_part.get_payload().decode(message.text_part.charset)
	#kill connect
	imapObj.logout()
#	pass

def smtpsendmail(smtpObj,mail_from,mail_to,mail_content):
	if smtpObj is not None:
		print 'sending email to ' + mail_to
		print 'mail\'s content' + mail_content
		smtpObj.sendmail(mail_from, [mail_to],'{0}'.format(mail_content))

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
