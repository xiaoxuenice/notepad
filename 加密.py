from Crypto.Cipher import DES3
import base64, hashlib

#单向加密
class HashDate:
    def __init__(self):
        self.salt = "**********"

    def hashpd(self, password, jiami):    #判断密码
        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()

        hash2 = md5hex(md5hex(password) + self.salt)
        if str(hash2) == str(jiami):
            return True
        else:
            return False

    def hashsc(self, password):            #加密生成
        def md5hex(ascii_str):
            return hashlib.md5(ascii_str.encode('ascii')).hexdigest()

        hash2 = md5hex(md5hex(password) + self.salt)
        return hash2

#加密解密
class EncryptDate:
    def __init__(self):
        self.key = b"*********"
        self.iv = b'01234567' 
        self.length = DES3.block_size
        self.des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数

        res = self.des3.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        msg = self.des3.decrypt(res).decode("utf8")
        return self.unpad(msg)

if __name__ == '__main__':
    print(HashDate().hashsc('aaaa'))
    print(HashDate().hashpd('aaaa','cd5834e7635270660c75d340b37e8c7a'))
    print(EncryptDate().encrypt('aaaa'))
    print(EncryptDate().decrypt('d71RogmLXmo='))
