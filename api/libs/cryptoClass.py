from Crypto.Cipher import AES
import base64

class Crypto():
    def __init__(self):
        self.BLOCK_SIZE=32
        self.password = b'ksjvdbihsjvbijvijbvjdsvnjnvdbsbjnns'
        self.salt = b'bvijhvnsdjikvndsjnjdnjn'

    # @classmethod
    def encrypt(self,message):
        '''
        encrypt the give data
        '''
        obj = AES.new(self.password.ljust(32)[:32], AES.MODE_CFB,self.salt.ljust(16)[:16])
        return base64.b64encode(obj.encrypt(message))

    # @classmethod
    def decrypt(self,encrypted):
        ''' 
        decrypt the given data
        '''
        obj = AES.new(self.password.ljust(32)[:32], AES.MODE_CFB, self.salt.ljust(16)[:16])
        return obj.decrypt(base64.b64decode(encrypted)).decode('utf-8')