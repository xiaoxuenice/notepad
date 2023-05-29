###pip install pycryptodome 
###vim models.py
from Crypto.Cipher import DES3
import base64
class jxs(models.Model):
        jxs = models.CharField(max_length=500,unique=True,verbose_name="CDN&解析商同账户")
        cs = models.CharField(max_length=500,unique=False,blank=True,verbose_name="厂商")
        zh = models.CharField(max_length=500,unique=False,blank=True,verbose_name="账号")
        gy = models.CharField(max_length=500,unique=False,blank=True,verbose_name="公钥")
        sy = models.CharField(max_length=500,unique=False,blank=True,verbose_name="私钥")
        class Meta:
                    verbose_name = '域名解析商'
                    verbose_name_plural = '域名解析商'
        def __str__(self):
                          return self.jxs
        def save(self,*args,**kwargs):
            if self.pk == None or jxs.objects.get(id=self.id).gy != self.gy or jxs.objects.get(id=self.id).sy != self.sy:
			    eg = EncryptDate("####****")  # 这里密钥的长度必须是16的倍数
                self.gy = eg.encrypt(self.gy)          #加密
                eg = EncryptDate("####****")  
                self.sy = eg.encrypt(self.sy)

            super(jxs,self).save(*args,**kwargs)
        def get_gy(self):                             #解密
            eg = EncryptDate("####****")      # 这里密钥的长度必须是16的倍数
            return str(eg.decrypt(jxs.objects.get(id=self.id).gy))
        def get_sy(self):							   
            eg = EncryptDate("####****")       
            return str(eg.decrypt(jxs.objects.get(id=self.id).sy))


class EncryptDate:
    def __init__(self, key):
        self.key = key  # 初始化密钥
        self.iv = b'01234567' # 偏移量
        self.length = DES3.block_size  # 初始化数据块大小
        self.des3 = DES3.new(self.key, DES3.MODE_CBC, self.iv)  # 初始化AES,CBC模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    def encrypt(self, encrData):  # 加密函数

        res = self.des3.encrypt(self.pad(encrData).encode("utf8"))
        msg = str(base64.b64encode(res), encoding="utf8")
        # msg =  res.hex()
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.decodebytes(decrData.encode("utf8"))
        # res = bytes.fromhex(decrData)
        msg = self.des3.decrypt(res).decode("utf8")
        return self.unpad(msg)

