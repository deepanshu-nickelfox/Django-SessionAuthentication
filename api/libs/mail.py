# python imports
import logging
import datetime

# django level imports
from django.core.mail import EmailMessage,send_mail

# project imports
from api.settings import EMAIL_HOST_USER


logger = logging.getLogger(__name__)

def sendmail(message,subject,tolist):
	try:
		send_mail(subject, message, EMAIL_HOST_USER, tolist)
		logger.info("Mail Sent ")
		return 1
	except:
		logger.error("Sending mail is failed", exc_info=True)
		return 0

