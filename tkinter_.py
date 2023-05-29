# -*- mode=python coding:utf-8 -*-
import traceback
from tkinter import *
from socket import gethostbyname
import time, requests, threading, random, json,    ssl, socket, whois, re, websockets
import dns.resolver
import asyncio
import idna
from socket import socket as ssocket
from OpenSSL import SSL
from numpy import *
LOG_LINE_NUM = 0


class MY_GUI_SET():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.ipdz = '____________'
        self.ceshi = []
        self.ceshi1 = []
        self.ceshi2 = []
        self.ceshi3 = []
        self.zhenghe = []
        self.uaList = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.104",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 ",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100",
        ]


    def set_init_window(self):
        self.init_window_name.title("运维工具 @Author weidong    @Version 3.5")
        self.init_window_name.geometry("1170x660+430+30")
        #self.init_window_name.resizable(0, 0)
        self.init_window_name.attributes("-alpha", 1)  # 虚化 值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="输入框")
        self.init_data_label.grid(row=0, column=0)
        self.name_data_label = Label(self.init_window_name, text="输出框")
        self.name_data_label.grid(row=0, column=14)
        #  滚动条
        self.scroll1 = Scrollbar()
        self.scroll2 = Scrollbar()
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=30, height=39, font=2)  # 原始数据录入框
        self.scroll2.config(command=self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand=self.scroll2.set)
        self.init_data_Text.grid(row=1, column=0, rowspan=20, columnspan=10)
        self.scroll2.grid(row=1, column=11, rowspan=20, columnspan=1, sticky='nsw')

        self.name_data_Text = Text(self.init_window_name, width=80, height=39, font=2)  # 处name果展示
        self.scroll1.config(command=self.name_data_Text.yview)
        self.name_data_Text.config(yscrollcommand=self.scroll1.set)
        self.name_data_Text.grid(row=1, column=14, rowspan=20, columnspan=10)
        self.scroll1.grid(row=1, column=25, rowspan=20, columnspan=1, sticky='nsw')

        self.name_data_Text.tag_config("tag2", foreground="green", font=2)
        self.name_data_Text.tag_config("tag1", foreground="red", font=2)
        self.name_data_Text.tag_config("tag3", foreground="blue", font=2)
        self.name_data_Text.tag_config("tag4", foreground="orange", font=2)
        self.name_data_Text.tag_config("tag5", foreground="black", font=("华文行楷", 30))
        self.name_data_Text.tag_config("tag6", foreground="black", font=("宋体", 15))


        self.str_trans_to_md5_button = Button(self.init_window_name, text="快速去重", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.qc))
        self.str_trans_to_md5_button.grid(row=2, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="Replace", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.splace))
        self.str_trans_to_md5_button.grid(row=3, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="状态码/TEXT", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.zhuangtaima))
        self.str_trans_to_md5_button.grid(row=4, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="wss 检测", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.wss))
        self.str_trans_to_md5_button.grid(row=5, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="NS查询", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.ns))
        self.str_trans_to_md5_button.grid(row=6, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="DNS/TXT", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.DNS))
        self.str_trans_to_md5_button.grid(row=7, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="域名到期", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.ymdq))
        self.str_trans_to_md5_button.grid(row=8, column=12)

        self.str_trans_to_md5_button = Button(self.init_window_name, text="证书到期", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.zsdq))
        self.str_trans_to_md5_button.grid(row=9, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text=" 清 屏", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.qp))
        self.str_trans_to_md5_button.grid(row=10, column=12)

        self.str_trans_to_md5_button = Button(self.init_window_name, text="密码生成", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.mmsc))
        self.str_trans_to_md5_button.grid(row=11, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="Telnet", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.telnet))
        self.str_trans_to_md5_button.grid(row=12, column=12)
        
        self.str_trans_to_md5_button = Button(self.init_window_name, text="IP归属", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.ipgs))
        self.str_trans_to_md5_button.grid(row=13, column=12)




        menubar = Menu(self.init_window_name, tearoff=False)
        def cut(editor, event=None):
            editor.event_generate("<<Cut>>")

        def copy(editor, event=None):
            editor.event_generate("<<Copy>>")

        def paste(editor, event=None):
            editor.event_generate('<<Paste>>')

        def rightKey(event, editor):
            menubar.delete(0, END)
            menubar.add_command(label='剪切', command=lambda: cut(editor))
            menubar.add_command(label='复制', command=lambda: copy(editor))
            menubar.add_command(label='粘贴', command=lambda: paste(editor))
            menubar.post(event.x_root, event.y_root)

        self.init_data_Text.bind("<Button-3>", lambda x: rightKey(x, self.init_data_Text))
        self.name_data_Text.bind("<Button-3>", lambda x: rightKey(x, self.name_data_Text))

    def onPaste(self):
            self.text  = self.init_window_name.clipboard_get()
            show = StringVar()
            show.set(str(self.text))

    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func)
        t.start()

    def telnet(self):
        ip_port  = self.init_data_Text.get(1.0, END).strip()
        for i in ip_port.split('\n'):
            try:
                if len(i.split()) == 2:
                    sk = socket.socket()
                    sk.settimeout(5)
                    sk.connect((i.split()[0], int(i.split()[1])))
                    sk.send(b'111')
                    sk.close()
                    self.name_data_Text.insert(END, self.duiqi(i,"  open\n",18), 'tag2')

            except Exception as err:
                print(err)
                self.name_data_Text.insert(END, self.duiqi(i, f"  close {str(err)}\n",18), 'tag1')

    def mmsc(self):
        self.name_data_Text.delete(1.0, END)

        def code(xx):
            a = '1234567890abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            b = ''
            for i in range(xx):
                c = random.randint(0, 61)
                b += a[c]
            self.name_data_Text.insert(END, f'字母数字{xx}位:\t\t {b}\n')
            return b

        def get_code(xx):
            a = '!@#$%^&*()./1234567890abcdefghijklmnopqr!@#$%^&*()./stuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
            b = ''
            for i in range(xx):
                c = random.randint(0, 85)
                b += a[c]
            self.name_data_Text.insert(END, f'字母数字符号{xx}位:\t\t {b}\n')
            return b

        code(18)
        code(20)
        code(25)
        code(30)
        get_code(18)
        get_code(20)
        get_code(25)
        get_code(30)

    def qp(self):
        self.name_data_Text.delete(1.0, END)

    def duiqi(self, name, par, strlen):
        return '{name:<{len}}'.format(name=name, len=int(strlen) - len(name.encode('UTF-8')) + len(name)) + "\t"+par

    def splace(self):
        self.name_data_Text.delete(1.0, END)
        a = self.init_data_Text.get(1.0, END)
        if not a.strip():
            self.name_data_Text.insert(END, '分隔符 ###', 'tag1')
            return 0
        b = a.split('###')
        c = b[0]
        d = b[1]
        e = b[2]
        e = e.replace('\n','',1)
        f = c.replace(d,e)
        self.name_data_Text.insert(END, f'{f}\n', 'tag1')
        
    def qc(self):
        self.name_data_Text.delete(1.0, END)
        self.name_data_Text.insert(END, '如果两组数据用空行分开\n\n', 'tag1')
        a = self.init_data_Text.get(1.0, END).strip()
        b = a.split('\n\n')
        if len(b) == 1:
            cc = b[0].strip().split('\n')
            ccc = []
            for i in cc:
                ccc.append(i.strip())
            self.name_data_Text.insert(END, f'输入数据 {len(ccc)} 个\n', 'tag1')
            dd = set(ccc)
            self.name_data_Text.insert(END, f'去重后 {len(dd)} 个\n', 'tag1')
            for i in dd:
                self.name_data_Text.insert(END, i + "\n")
        else:
            c = b[0]
            d = b[1]
            ca = c.split('\n')
            caca = []
            for i in ca:
                caca.append(i.strip())
            cb = d.split('\n')
            cbcb = []
            for i in cb:
                cbcb.append(i.strip())
            e = set(caca)
            f = set(cbcb)
            self.name_data_Text.insert(END, f'第一组一共有 {len(e)} 个\n', 'tag3')
            self.name_data_Text.insert(END, f'第二组一共有 {len(f)} 个\n', 'tag3')
            g = e | f
            h = e & f
            self.name_data_Text.insert(END, f'\n两组全部域名是 {len(g)} 个\n', 'tag1')
            for i in g:
                self.name_data_Text.insert(END, i + "\n")
            self.name_data_Text.insert(END, f'\n两组共有域名是 {len(h)} 个\n', 'tag1')
            for i in h:
                self.name_data_Text.insert(END, i + "\n")
            self.name_data_Text.insert(END, f'\n第一组不在第二组的\n', 'tag1')
            n = 0
            for i in e:
                if i not in f:
                    n += 1
                    self.name_data_Text.insert(END, i + '\n')
            self.name_data_Text.insert(END, f'合计{str(n)}\n', 'tag2')
            self.name_data_Text.insert(END, f'\n第二组不在第一组的\n', 'tag1')
            n = 0
            for i in f:
                if i not in e:
                    n += 1
                    self.name_data_Text.insert(END, i + '\n')
            self.name_data_Text.insert(END, f'合计{str(n)}\n', 'tag2')

    def zhuangtaima(self):
        self.name_data_Text.delete(1.0, END)
        self.name_data_Text.insert(END, "\n状态码 检测开始\n", "tag2")
        try:
            my_ip = requests.get("https://ipv4.icanhazip.com").content
            strra = '检测的公网ip       ' + my_ip.decode() + "\n"
            self.name_data_Text.insert(END, strra, "tag3")
        except Exception as f:

            self.name_data_Text.insert(END, "检测公网ip获取失败，结束检测\n", "tag3")
            return 0
        a = self.init_data_Text.get(1.0, END).strip()
        if not a:
            self.name_data_Text.insert(END, "末行加入TEXT检测添加TEXT", "tag4")
        a = a.split("\n")
        self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}
        if  a[-1].strip()  == "TEXT":
            is_text = False
        else:
            is_text = True
        for i in a:
            if not i.strip()  or i.strip() == 'TEXT' :
                continue
            i = i.strip()
            i = i.split()[0]
            self.ipdz = '____________'
            self.ll = ''
            i = i.strip()
            try:
                nohttp = i.replace('https://', '').replace('http://', '')
                noport = nohttp.split(':')[0]
                noport = noport.split('/')[0]
                self.ipdz = gethostbyname(noport)
                l = 20 - len(self.ipdz)

                for aecw in range(l):
                    self.ll += ' '
                self.ll += '\t'
                if is_text:
                    if 'https://' in i or 'http://' in i:
                        ztm = requests.get(str(i),   stream=True, timeout=10).status_code
                    else:


                        ztm = requests.get("https://" + str(i), timeout=10).status_code

                    strr = str(self.ipdz) + self.ll + str(ztm) + "     \t" + i + "\n"
                    self.name_data_Text.insert(END, strr, "tag2")
                else:
                    if 'https://' in i or 'http://' in i:

                        aaaa = requests.get(str(i),   stream=True, timeout=10)
                        zzz = aaaa.status_code
                        ztm = aaaa.content.decode()
                        print(ztm)
                        strr = str(self.ipdz) + self.ll + str(zzz) + "     \t" + i +  "\n"
                        self.name_data_Text.insert(END, strr, "tag2")
                        self.name_data_Text.insert(END,str(ztm) +"\n" ,
                                                   "tag4")
                        self.name_data_Text.insert(END,
                                                   "-----------------------------------------------------------------------------------------------------------------------------------------------\n",
                                                   "tag3")
                    else:
                        aaaa = requests.get("https://" + str(i), stream=True, timeout=10)
                        zzz = aaaa.status_code
                        ztm = aaaa.content.decode()
                        strr = str(self.ipdz) + self.ll + str(zzz) + "     \t"+ i +  "\n"
                        self.name_data_Text.insert(END, strr, "tag2")
                        self.name_data_Text.insert(END, str(ztm) + "\n" ,
                                                   "tag4")
                        self.name_data_Text.insert(END,
                                                   "------------------------------------------------------------------------------------------------------------------------------------------------\n","tag3")
            except Exception as f:
                traceback.print_exc()
                print(f)
                if "timed out" in str(f):

                    ztm = "超时"
                    strr = str(self.ipdz) + self.ll + str(ztm) + "\t     " + i + "\n"

                    self.name_data_Text.insert(END, strr, "tag1")
                elif "ConnectionResetError" in str(f) or "10054" in str(f):

                    ztm = "屏蔽"
                    strr = str(self.ipdz) + self.ll + str(ztm) + "\t     " + i + "\n"

                    self.name_data_Text.insert(END, strr, "tag1")

                elif "Name or service" in str(f) or "getaddrinfo" in str(f):

                    ztm = "未解"
                    strr = str(self.ipdz) + '\t\t\t\t' + self.ll + str(ztm) + "\t     " + i + "\n"

                    self.name_data_Text.insert(END, strr, "tag1")
                elif "Connection refused" in str(f):

                    ztm = "拒绝"
                    strr = str(self.ipdz) + " \t    \t" + str(ztm) + "\t     " + i

                    self.name_data_Text.insert(END, strr, "tag1")
                elif "SSLError" in str(f):

                    ztm = "掉证"
                    strr = str(self.ipdz) + self.ll + str(ztm) + "\t     " + i + "\n"

                    self.name_data_Text.insert(END, strr, "tag1")
                else:

                    ztm = "错误"
                    strr = str(self.ipdz) + self.ll + str(ztm) + "\t     " + i + "\n"
                    self.name_data_Text.insert(END, strr, "tag1")
        self.name_data_Text.insert(END, "\n状态码 检测结束\n", "tag2")

    def ns(self):
        self.name_data_Text.insert(END, "\nNS 检测开始\n", "tag2")
        a = self.init_data_Text.get(1.0, END).strip()
        aec = a.split("\n")
        for i in aec:
            if i.strip():
                i = i.strip()
                i = i.split()[0]
                i = i.replace('https://', '').replace('http://', '').replace('/', '')
                i = i.split(':')[0]
                i = "{}.{}".format(i.split(".")[-2], i.split(".")[-1])
            else:
                continue
            try:
                l = 20 - len(i)
                self.ll = ''
                for aecw in range(l):
                    self.ll += ' '
                self.ll += '\t'
                dd = ''
                a = dns.resolver.query(i, 'NS')


                for ia in a.response.answer:
                    for ii in ia.items:
                        dd += '  '
                        dd += ii.to_text()

                strr = self.ll + dd + "\n"

                self.name_data_Text.insert(END, i.strip(), 'tag3')
                self.name_data_Text.insert(END, strr)
            except Exception as ff:
                print(ff)
                try:
                    self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                                    "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}
                    dd = re.findall("Name Server:(.*?)<", requests.get(
                        f"https://whois.reg.cn/Whois/QueryWhois?domain={i}&key=23dfw43459835vbffg").text)[0].lower()
                    strr = self.ll + dd + "\n"

                    self.name_data_Text.insert(END, i.strip(), 'tag3')
                    self.name_data_Text.insert(END, strr)
                except Exception as ff:
                    strr = i.strip() + str(ff) + "\n"
                    self.name_data_Text.insert(END, strr, 'tag1')

        self.name_data_Text.insert(END, "\nNS 检测结束\n", "tag2")

    def wss(self):
        self.name_data_Text.insert(END, "wss 开始检测\n", "tag1")
        a = self.init_data_Text.get(1.0, END).strip()
        aec = a.split("\n")
        mess = '带kefu的检测为：ws.connect(f"wss://{domain}/ws_visitor")\ngateway检测为：ws.connect(f"wss://{domain}/gate/ws")\n带wss:// or ws:// 按照url请求\n'
        self.name_data_Text.insert(END, mess, "tag4")
        for domain in aec:
            if not domain.strip():
                continue
            try:
                ws = websockets
                if "ws://" in domain or "wss://" in domain:
                    domain = domain.split()[0]

                    async def hello():
                        async with ws.connect(domain) as wsss:
                            await wsss.send("Hello world!")

                    asyncio.run(hello())
                elif 'kefu' in domain:
                    domain = domain.split()[0]
                    async def hello():
                        async with  ws.connect(f"wss://{domain}/ws_visitor") as wsss:
                            await wsss.send("Hello world!")

                    asyncio.run(hello())
                else:
                    domain = domain.split()[0]
                    async def hello():
                        async with  ws.connect(f"wss://{domain}/gate/ws") as wsss:
                            await wsss.send("Hello world!")

                    asyncio.run(hello())
                if ws.connect:
                    self.name_data_Text.insert(END, domain.strip() + '         ' + 'OK' + '\n', "tag2")
            except Exception as err:
                self.name_data_Text.insert(END, domain.strip() + '         ' + str(err) + '\n', "tag1")
        self.name_data_Text.insert(END, "\nwss检测结束\n", "tag2")


    def DNS(self):
        self.name_data_Text.insert(END, "DNS检测开始\n", "tag1")
        self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}
        try:
            my_ip = requests.get("https://ipv4.icanhazip.com").content
            strra = '检测的公网ip       ' + my_ip.decode() + "\n"
            self.name_data_Text.insert(END, strra, "tag3")
        except Exception as f:

            self.name_data_Text.insert(END, "检测公网ip获取失败，结束检测", "tag3")
            return 0
        a = self.init_data_Text.get(1.0, END).strip()
        if not a:
            self.name_data_Text.insert(END, "末行加入TXT检测为TXT", "tag4")
        aec = a.split("\n")
        if  aec[-1].strip()  == "TXT":
            for i in aec:
                if not i.strip() or i.strip() == 'TXT':
                    continue
                try:

                    self.name_data_Text.insert(END, "\n{}\n".format(i), "tag2")
                    wb = ''
                    i = i.split()[0]
                    i = i.replace('https://', '').replace('http://', '').replace('/', '')
                    i = i.split(':')[0]
                    for ix in dns.resolver.query(i.strip(),'TXT'):
                        wb += ix.to_text() + "\n"
                    self.name_data_Text.insert(END, wb)
                except Exception as err:
                    self.name_data_Text.insert(END, i + str(err), "tag1")
        else:
            for i in aec:
                if not i.strip() or i.strip() == 'TXT':
                    continue
                try:

                    self.name_data_Text.insert(END, "\n{}\n".format(i), "tag2")
                    wb = ''
                    i = i.split()[0]
                    i = i.replace('https://', '').replace('http://', '').replace('/', '')
                    i = i.split(':')[0]
                    for ix in dns.resolver.query(i.strip()).response.answer:
                        wb += ix.to_text() + "\n"
                    self.name_data_Text.insert(END, wb)
                except Exception as err:
                    self.name_data_Text.insert(END, i + str(err), "tag1")
        self.name_data_Text.insert(END, "\nDNS检测结束\n", "tag2")

    def ipgs(self):
        self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}
        a = self.init_data_Text.get(1.0, END).strip()
        aec = a.split("\n")
        for i in aec:
            try:

                time.sleep(0.5)
                c = requests.get(
                    f'http://opendata.baidu.com/api.php?query={i.strip()}&co=&resource_id=6006&oe=utf8' ).content.decode()
                d = json.loads(c)
                wb = i.strip() + '   ' + d['data'][0]['location'] + "\n"
                self.name_data_Text.insert(END, wb)
            except Exception as err:
                self.name_data_Text.insert(END, i + str(err) + '\n', "tag1")
        self.name_data_Text.insert(END, "\nIP归属检测结束\n", "tag2")

    def ymdq(self):
        self.name_data_Text.insert(END, "域名到期检测开始\n", "tag1")
        a = self.init_data_Text.get(1.0, END).strip()
        aec = a.split("\n")
        self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}
        allym = []
        errym = []
        for i in aec:
            if not i.strip():
                continue
            l = 20 - len(i)
            self.ll = ''
            for aecw in range(l):
                self.ll += ' '
            self.ll += '\t'
            i = i.strip()
            i = i.split()[0]
            i = i.replace('https://', '').replace('http://', '').replace('/', '')
            i = i.split(':')[0]
            try:

                if i != '\n':
                    pass
                else:
                    continue
                i = i.strip()
                i = "{}.{}".format(i.split(".")[-2], i.split(".")[-1])
                bb = whois.whois(i)
                cc = bb.expiration_date
                print(cc)
                if type(cc) is list:
                    dd = cc[0]
                    a = str(dd.strftime("%Y-%m-%d %H:%M:%S"))
                else:
                    a = str(cc.strftime("%Y-%m-%d %H:%M:%S"))
                allym.append(a + '   ' + i)
                strr = i + self.ll + a + "\n"
                self.name_data_Text.insert(END, strr, "tag2")
            except Exception as f:
                try:
                    a = re.findall("Registry Expiry Date:(.*?)T", requests.get(
                        f"https://whois.reg.cn/Whois/QueryWhois?domain={i.lower().strip()}&key=23dfw43459835vbffg",
                        timeout=3).text)[0]
                    allym.append(a + '   ' + i)
                    strr = i.strip() + self.ll + a + "\n"
                    self.name_data_Text.insert(END, strr, "tag2")
                except Exception as ff:
                    errym.append(i + '   ' + str(ff))
                    strr = i.strip() + self.ll + str(ff) + "\n"
                    self.name_data_Text.insert(END, strr, "tag1")
        aaaa = sorted(allym)

        self.name_data_Text.insert(END, "\n=================  域名到期排序   =================\n", "tag3")
        for i in aaaa:
            self.name_data_Text.insert(END, i + "\n", "tag2")
        self.name_data_Text.insert(END, "=================  没有检测出来的   =================\n", "tag3")
        for i in errym:
            self.name_data_Text.insert(END, i + "\n", "tag1")

        self.name_data_Text.insert(END, "域名到期检测结束\n", "tag1")

    def zsdq(self):

        self.headers = {"User-Agent": random.choice(self.uaList), "accept": "text/plain, */*; q=0.01",
                        "accept-language": "zh-CN,zh;q=0.9,en;q=0.8,und;q=0.7", "Connection": "close"}

        today = time.strftime('%Y%m%d', time.localtime(time.time()))
        aerr = {}
        will = {}
        all = {}
        a = self.init_data_Text.get(1.0, END).strip()
        if not a:
            self.name_data_Text.insert(END, f"域名+空行+IP 为绑定IP去检测证书\n", "tag3")
        ta = a.split("\n\n")
        bindip = False
        if len(ta) == 2:
            bindip = True
            aec = ta[0].split("\n")
            _ipip = ta[1].strip()
            self.name_data_Text.insert(END, f"检测为绑定IP模式 \n\n", "tag3")
        else:
            aec = a.split("\n")

        def get_certificate(_cdn, _domain, port):
            hostname_idna = idna.encode(_domain)
            sock = ssocket()
            print(f'1{_cdn}-{_domain}-{port}2')
            sock.connect((_cdn, port), )
            ctx = SSL.Context(SSL.SSLv23_METHOD)
            ctx.check_hostname = False
            ctx.verify_mode = SSL.VERIFY_NONE
            sock_ssl = SSL.Connection(ctx, sock)
            sock_ssl.set_connect_state()
            sock_ssl.set_tlsext_host_name(hostname_idna)  # 关键: 对应不同域名的证书
            sock_ssl.do_handshake()
            cert = sock_ssl.get_peer_certificate()
            sock_ssl.close()
            sock.close()
            return cert

        for i in aec:
            if not i.strip():
                continue


            domain = i.strip()
            i = i.split()[0]
            i = i.replace('https://', '').replace('http://', '').replace('/', '')
            ii = i
            pSSl = 443
            if len(i.split(':')) == 2:
                pSSl = int(i.split(':')[1])
            i = i.split(':')[0]
            try:
                requests.get('https://{}'.format(ii), timeout=10).close()
            except Exception as err:
                aerr[domain] = "检测有误\t\t"
                continue
            if  bindip:
                try:
                    print('xxxxxxxx 1 ')
                    cert = get_certificate(_ipip, i, pSSl)
                    _start = time.strftime("%Y-%m-%d",
                                           time.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ"))
                    _end = time.strftime("%Y-%m-%d", time.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ"))
                    days = int(
                        (time.mktime(
                            time.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")) - time.time()) / (
                                60 * 60 * 24))
                    self.name_data_Text.insert(END, f"{i}\n", "tag1")
                    self.name_data_Text.insert(END, f"申请时间:  {_start}  \t到期时间:{_end}  \t到期天数:{int(days)}\n\n", "tag2")
                except Exception as err:
                    print('xxxxxxxx 2 ')
                    print(err)
                    try:
                        cert = get_certificate(_ipip, i, pSSl)
                        _start = time.strftime("%Y-%m-%d",
                                               time.strptime(cert.get_notBefore().decode(), "%Y%m%d%H%M%SZ"))
                        _end = time.strftime("%Y-%m-%d", time.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ"))
                        days = int(
                            (time.mktime(
                                time.strptime(cert.get_notAfter().decode(), "%Y%m%d%H%M%SZ")) - time.time()) / (
                                        60 * 60 * 24))
                        self.name_data_Text.insert(END, i + f"\t     申请时间:{_start}  到期时间:{_end}  剩余天数:{int(days)}\n",
                                                   "tag2")
                    except Exception as err:
                        aerr[i] = str(err)
                        self.name_data_Text.insert(END, i + "\t        {}\n".format(str(err)), "tag1")
                continue

            else:

                c = ssl.create_default_context()
                s = c.wrap_socket(socket.socket(), server_hostname=i)
                try:
                    s.connect((i, pSSl))
                except Exception as err:
                        print('mlgp')
                        aerr[i] = str(err)
                        self.name_data_Text.insert(END, i + "\t        {}\n".format(str(err)), "tag1")
                        s.close()
                        continue
                print('nidaye')
                cert = s.getpeercert()

                print(cert['notBefore'])
                print(type(cert['notBefore']))
                sqsj = time.strftime("%Y-%m-%d", time.strptime(cert['notBefore'], "%b %d %H:%M:%S %Y %Z"))
                dqsja = time.strftime("%Y%m%d", time.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z"))
                dqsj = time.strftime("%Y-%m-%d",time.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z"))
                print(type(time.mktime(time.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z"))))
                asdf = time.mktime(time.strptime(cert['notAfter'], "%b %d %H:%M:%S %Y %Z"))
                sysj = (asdf - time.time()) / (60 * 60 * 24)
                if int(dqsja) - int(today) < 5:
                    will[i] = dqsj
                all[i] = dqsj
                self.name_data_Text.insert(END, i + f"\t     申请时间:{sqsj}  到期时间:{dqsj}  剩余天数:{int(sysj)}\n", "tag2")
                zsgym = cert.get('subject')[0][0][1]
                self.name_data_Text.insert(END, "证书公有名:               {}\n".format(zsgym), "tag4")
                self.name_data_Text.insert(END, "证书绑定域名:\n", "tag4")
                for i in cert.get('subjectAltName'):
                    self.name_data_Text.insert(END, f"\t\t{i[1]}\n", "tag4")
                self.name_data_Text.insert(END,
                                           "---------------------------------------------------------------------------------------\n\n",
                                           "tag2")
        if not bindip:
            time.sleep(0.5)
            alll = []
            for i in all:
                alll.append('{} \t     {}'.format(all[i], i))
            allll = sorted(alll)
            self.name_data_Text.insert(END, "\n=====  证书到期时间   ====\n", "tag3")
            for i in allll:
                self.name_data_Text.insert(END, i + "\n", "tag2")
            self.name_data_Text.insert(END, "=====  没检查出来的 =====\n", "tag3")
            for i in aerr.keys():
                self.name_data_Text.insert(END, aerr[i] + "\t\t" + i + "\n", "tag1")
            self.name_data_Text.insert(END, "=====  证书快到期的  =====\n", "tag3")
            for i in will.keys():
                self.name_data_Text.insert(END, will[i] + "\t\t" + i + "\n", "tag1")
            self.name_data_Text.insert(END, "证书检测结束\n", "tag1")



if __name__ == "__main__":
    init_window = Tk()
    MY_GUI_SET(init_window).set_init_window()
    init_window.mainloop()

