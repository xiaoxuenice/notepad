# -*- mode=python coding:utf-8 -*-
from tkinter import *
import threading,CloudFlare,time,easygui
LOG_LINE_NUM = 0
class MY_GUI_SET():
    def __init__(self, init_window_name):
        self.init_window_name = init_window_name
        self.cf=''
    def set_init_window(self):
        self.init_window_name.title("cloudflare批量添加域名工具")
        self.init_window_name.geometry("860x660+430+30")

        self.init_window_name.resizable(0, 0)
        self.init_window_name.attributes("-alpha", 1)  # 虚化 值越小虚化程度越高
        # 标签
        self.init_data_label = Label(self.init_window_name, text="输入域名")
        self.init_data_label.grid(row=0, column=0)
        self.name_data_label = Label(self.init_window_name, text="邮箱")
        self.name_data_label.grid(row=0, column=14, sticky='nsw')
        self.name_data_label = Label(self.init_window_name, text="token")
        self.name_data_label.grid(row=2, column=14, sticky='nsw')
        self.name_data_label = Label(self.init_window_name, text="CNAME写域名         A记录写ip地址         TXT写TXT值     ")
        self.name_data_label.grid(row=4, column=14, sticky='nsw')
        self.name_data_label = Label(self.init_window_name, text="日志")
        self.name_data_label.grid(row=6, column=14, sticky='nsw')
        #  滚动条
        self.scroll1 = Scrollbar()
        self.scroll2 = Scrollbar()
        # 文本框
        self.init_data_Text = Text(self.init_window_name, width=20, height=39,font=2)  # 原始数据录入框
        self.scroll2.config(command=self.init_data_Text.yview)
        self.init_data_Text.config(yscrollcommand=self.scroll2.set)
        self.init_data_Text.grid(row=1, column=0, rowspan=20, columnspan=10)
        self.scroll2.grid(row=1, column=11,rowspan=20, columnspan=1, sticky='nsw')
        self.mail=Text(self.init_window_name, width=70,height=1,font=2)
        self.mail.grid(row=1,column=14)
        self.key=Text(self.init_window_name, width=70,height=1,font=2)
        self.key.grid(row=3,column=14)
        self.jiexizhi=Text(self.init_window_name, width=70,height=1,font=2)
        self.jiexizhi.grid(row=5,column=14)


        self.name_data_Text = Text(self.init_window_name, width=70, height=30,font=2)  # 处name果展示
        self.scroll1.config(command=self.name_data_Text.yview)
        self.name_data_Text.config(yscrollcommand=self.scroll1.set)
        self.name_data_Text.grid(row=7, column=14, rowspan=20, columnspan=10)
        self.scroll1.grid(row=7, column=25, rowspan=20, columnspan=1, sticky='nsw')

        self.name_data_Text.tag_config("tag2", foreground="green",font=2)
        self.name_data_Text.tag_config("tag1", foreground="red", font=2)
        self.name_data_Text.tag_config("tag3", foreground="blue", font=2)

        self.str_trans_to_md5_button = Button(self.init_window_name, text="CNAME", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.cname))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=9, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="CNAME代理", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.cnamedl))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=7, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="A 记录 ", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.aaaa))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=10, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="A   代理", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.bbbb))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=8, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="TXT", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.txt))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=11, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="清空所有记录", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.clean))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=12, column=12)
        self.str_trans_to_md5_button = Button(self.init_window_name, text="NS查询", bg="lightblue", width=10,
                                              command=lambda: self.thread_it(self.nscx))  # 调用内部方法  加()为直接调用
        self.str_trans_to_md5_button.grid(row=13, column=12)
##############################################################################################################
    # 添加txt记录传入url，记录，值
    def add_txt_recode(self,url, srccontext, descontext):
        zone_id = self.get_zoneid(url)
        recode = {'name': srccontext, 'type': 'TXT', 'content': descontext}
        try:
            self.cf.zones.dns_records.post(zone_id, data=recode)
            self.name_data_Text.insert(END, url+' txt                添加完成' +"\n","tag2")
        except Exception as err:
            self.name_data_Text.insert(END, url + '     '+ str(err) + "\n", "tag1")

    # 添加A记录,传递域名，二级域名，和对应A记录
    def add_a_recode(self,url, zone, ip):
        try:
            zone_id = self.get_zoneid(url)
            recode = {'name': zone, 'type': 'A', 'content': ip, 'proxied': False}
            self.name_data_Text.insert(END, f'{url}    {zone}   {ip}         添加完成' + "\n", "tag2")
        except Exception  as err:
            self.name_data_Text.insert(END, url + '     '+ str(err) + "\n", "tag1")
    def add_a_recodedl(self,url, zone, ip):
        try:
            zone_id = self.get_zoneid(url)
            recode = {'name': zone, 'type': 'A', 'content': ip, 'proxied': True}
            self.cf.zones.dns_records.post(zone_id, data=recode)
            self.name_data_Text.insert(END, f'{url}    {zone}   {ip}         添加完成' + "\n", "tag2")
        except Exception  as err:
            self.name_data_Text.insert(END, url + '     '+  str(err) + "\n", "tag1")
    # 添加CNAME记录，传递要操作的域名，二级域名，和对应cname值，如果二级域名传递的是域名本身，代表添加根记录
    def add_cname_recode(self,url, zone, cnameurl):
        try:
            zone_id = self.get_zoneid(url)
            recode = {'name': zone, 'type': 'CNAME', 'content': cnameurl, 'proxied': False}
            self.cf.zones.dns_records.post(zone_id, data=recode)
            self.name_data_Text.insert(END,  f'{url}    {zone}   {cnameurl}         添加完成' + "\n", "tag2")
        except Exception  as err:
            self.name_data_Text.insert(END, url + '     '+  str(err) + "\n", "tag1")
    def add_cname_recodedl(self,url, zone, cnameurl):
        try:
            zone_id = self.get_zoneid(url)
            recode = {'name': zone, 'type': 'CNAME', 'content': cnameurl, 'proxied': True}
            self.cf.zones.dns_records.post(zone_id, data=recode)
            self.name_data_Text.insert(END,  f'{url}    {zone}   {cnameurl}         添加完成' + "\n", "tag2")
        except Exception  as err:
            self.name_data_Text.insert(END, url + '     '+  str(err) + "\n", "tag1")
    def cxns(self,url):
        try:
            zone_infos = self.cf.zones.get(params={'name': url})
            print(zone_infos)
            mess=url+'     '+'   '.join(zone_infos[0]['name_servers'])
            self.name_data_Text.insert(END, f"{mess}\n", "tag2")
        except Exception as err:
            mess = url + ' 没找到 '
            self.name_data_Text.insert(END, f"{mess}\n", "tag1")
    # 判断是否添加该域名，如果有添加返回1，未添加返回0
    def if_add(self,url):
        zone_infos = self.cf.zones.get(params={'name': url})
        if len(zone_infos) == 0:
            return 0
        return 1

    # 获取zoneid，如果域名没有加则加域名后再获取
    def get_zoneid(self,url):
        # 如果没有添加域名
        if self.if_add(url) == 0:
            zone_info = self.cf.zones.post(data={'name': url})
            return zone_info['id']
        # 如果有添加域名后，再获取id
        else:
            zone_infos = self.cf.zones.get(params={'name': url})
            return zone_infos[0]['id']

    # 清除某个域名的所有记录
    def clean_recode(self,url):
        try:
            zone_id = self.get_zoneid(url)
            dns_records = self.cf.zones.dns_records.get(zone_id)
            for dns_record in dns_records:
                dns_record_id = dns_record['id']
                self.cf.zones.dns_records.delete(zone_id, dns_record_id)
            self.name_data_Text.insert(END, url + "                        已清空所有记录" + "\n", "tag2")
        except Exception as err:
            self.name_data_Text.insert(END, url + str(err) + "\n", "tag1")
    # 删除某个域名的某条记录，第一个参数为域名，第二个参数为二级域名，传入@代表删除根记录
    def delete_record(self,url, dns_name):
        zone_id = self.get_zoneid(url)
        try:
            if dns_name == '@':
                dns_records =self.cf.zones.dns_records.get(zone_id, params={'name': url})
                for dns_record in dns_records:
                    dns_record_id = dns_record['id']
                    self.cf.zones.dns_records.delete(zone_id, dns_record_id)
            else:
                dns_records = self.cf.zones.dns_records.get(zone_id, params={'name': dns_name + '.' + url})
                for dns_record in dns_records:
                    dns_record_id = dns_record['id']
                    self.cf.zones.dns_records.delete(zone_id, dns_record_id)
        except Exception as err:
            self.name_data_Text.insert(END, url + str(err) + "\n", "tag1")

    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func)
        t.setDaemon(True)  # 守护--就算主界面关闭，线程也会留守后台运行（不对!）
        t.start()
    def qp(self):
        self.name_data_Text.delete(1.0,END)
    def clean(self):
            em=self.mail.get(1.0,END).strip()
            key=self.key.get(1.0,END).strip()
            self.cf = CloudFlare.CloudFlare(email=em,token=key)
            all = self.init_data_Text.get(1.0, END).strip()
            b=all.split('\n')
            for i in b:
                try:
                    time.sleep(0.2)
                    if i:
                        pass
                    else:
                        continue
                    i=i.strip()
                    self.clean_recode(i)
                except Exception as err:
                    self.name_data_Text.insert(END, "========================================\n", "tag1")
                    self.name_data_Text.insert(END,f"{i}   {err}\n", "tag1")
                    self.name_data_Text.insert(END, "========================================\n", "tag1")
    def cname(self):

        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for  i in b:
            try:
                time.sleep(0.2)
                if i:
                    pass
                else:
                    continue
                i=i.strip()
                self.delete_record(i, '@')
                self.delete_record(i, 'www')
                self.add_cname_recode(i, '@', content)
                self.add_cname_recode(i, 'www', content)
            except Exception as err:
                self.name_data_Text.insert(END, "========================================\n", "tag1")
                self.name_data_Text.insert(END, f"{i}   {err}\n", "tag1")
                self.name_data_Text.insert(END, "========================================\n", "tag1")
    def cnamedl(self):

        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for i in b:
            try:
                time.sleep(0.2)
                if i:
                    pass
                else:
                    continue
                i=i.strip()
                self.delete_record(i, '@')
                self.delete_record(i, 'www')
                self.add_cname_recodedl(i, '@', content)
                self.add_cname_recodedl(i, 'www', content)
            except Exception as err:
                self.name_data_Text.insert(END, "========================================\n", "tag1")
                self.name_data_Text.insert(END, f"{i}   {err}\n", "tag1")
                self.name_data_Text.insert(END, "========================================\n", "tag1")
    def nscx(self):
        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for i in b:
            self.cxns(i)
    def aaaa(self):

        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for i in b:
            try:
                time.sleep(0.2)
                if i:
                    pass
                else:
                    continue
                i=i.strip()
                self.delete_record(i, '@')
                self.delete_record(i, 'www')
                self.add_a_recode(i, '@', content)
                self.add_a_recode(i, 'www', content)
            except Exception as err:
                self.name_data_Text.insert(END, "========================================\n", "tag1")
                self.name_data_Text.insert(END, f"{i}   {err}\n", "tag1")
                self.name_data_Text.insert(END, "========================================\n", "tag1")
    def bbbb(self):

        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for i in b:
            try:
                time.sleep(0.2)
                if i:
                    pass
                else:
                    continue
                i=i.strip()
                self.delete_record(i, '@')
                self.delete_record(i, 'www')
                self.add_a_recodedl(i, '@', content)
                self.add_a_recodedl(i, 'www', content)
            except Exception as err:
                self.name_data_Text.insert(END, "========================================\n", "tag1")
                self.name_data_Text.insert(END, f"{i}   {err}\n", "tag1")
                self.name_data_Text.insert(END, "========================================\n", "tag1")
    def txt(self):

        em=self.mail.get(1.0,END).strip()
        key=self.key.get(1.0,END).strip()
        self.cf = CloudFlare.CloudFlare(email=em,token=key)
        all = self.init_data_Text.get(1.0, END).strip()
        content=self.jiexizhi.get(1.0,END).strip()
        b=all.split('\n')
        for i in b:
            try:
                time.sleep(0.2)
                if i:
                    pass
                else:
                    continue
                i=i.strip()
                self.delete_record(i, '_dnsauth')
                self.add_txt_recode(i,'_dnsauth', content)
            except Exception as err:
                self.name_data_Text.insert(END, "========================================\n", "tag1")
                self.name_data_Text.insert(END, f"{i}   {err}\n", "tag1")
                self.name_data_Text.insert(END, "========================================\n", "tag1")
if __name__=="__main__":
    init_window = Tk()
    MY_GUI_SET(init_window).set_init_window()
    init_window.mainloop()
