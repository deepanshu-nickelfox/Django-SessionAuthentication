
'''
These functions can be used for to send the message to client.
'''


def text_message(name, password):
	message_= """
Dear {name},

	 Welcome, We thank you for your registration at G-store.

	Your password is: {password} 

	""".format(name=name, password=password)

	return message_

def txt_otp_message(otp):
	message_ = """
	Hi,
	  {otp} is your G-store password reset code.
	""".format(otp=otp)

	return message_