# -*- mode=python ending:utf-8 -*-
import kivy

kivy.require('1.11.1')
from kivy.app import App
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.widget import Widget
from kivy.uix.button import Button
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import ListProperty
from kivy.graphics import Color, Rectangle
from kivy.config import Config
from kivy.core.window import Window
from kivy.factory import Factory
import MYSQLL, mdpasswd, threading, time


class RootWidget(FloatLayout):
    def __init__(self, **kwargs):
        super(RootWidget, self).__init__(**kwargs)

        Config.set('graphics', 'resizable', 0)
        Window.fullscreen = 0
        #Window.size = (380, 600)

        tc = Button(pos_hint={'x': 0.2, 'y': 0.65}, size_hint=(0.2, 0.05))
        tc.background_color = [2, 2, 3, 1]
        self.add_widget(tc)
        tc = Button(pos_hint={'x': 0.2, 'y': 0.6}, size_hint=(0.2, 0.05))
        tc.background_color = [2, 2, 3, 1]
        self.add_widget(tc)
        tc = Button(pos_hint={'x': 0.2, 'y': 0.5}, size_hint=(0.2, 0.05))
        tc.background_color = [2, 2, 3, 1]
        self.add_widget(tc)
        cb = CustomBtn1(pos_hint={'x': 0.2, 'y': 0.5}, size_hint=(0.2, 0.6))
        cb.bind()
        self.add_widget(cb)

        self.add_widget(Label(text='NAME', font_name='zw.ttf', pos_hint={'x': 0.2, 'y': 0.65}, size_hint=(0.2, 0.05)))
        self.add_widget(Label(text='SEND', font_name='zw.ttf', pos_hint={'x': 0.2, 'y': 0.6}, size_hint=(0.2, 0.05)))
        self.add_widget(Label(text='PASSWD', font_name='zw.ttf', pos_hint={'x': 0.2, 'y': 0.5}, size_hint=(0.2, 0.05)))

        self.userna = TextInput(font_name='zw.ttf', size_hint_y=.2, multiline=False, pos_hint={'x': 0.43, 'y': 0.65},
                                size_hint=(0.4, 0.05))
        self.add_widget(self.userna)
        self.send = TextInput(font_name='zw.ttf', size_hint_y=.2, multiline=False, pos_hint={'x': 0.43, 'y': 0.6},
                              size_hint=(0.4, 0.05))
        self.add_widget(self.send)
        self.userpw = TextInput(password=True, font_name='zw.ttf', size_hint_y=.2, multiline=False,
                                pos_hint={'x': 0.43, 'y': 0.5}, size_hint=(0.4, 0.05))
        self.add_widget(self.userpw)

        login = Button(text="LOGIN", pos_hint={'x': 0.333, 'y': 0.4}, size_hint=(0.333, 0.08))
        login.background_color = [2, 2, 3, 1]
        self.add_widget(login)

        cb = CustomBtn2(pos_hint={'x': 0.333, 'y': 0.4}, size_hint=(0.333, 0.08))
        cb.bind(pressed=self.btn_pressed)
        self.add_widget(cb)

    def btn_pressed(self, instance, pos):
        b = self.userna.text
        b = b.lower().strip()
        c = self.userpw.text
        c = c.lower().strip()
        e = self.send.text
        e = e.lower().strip()

        if MYSQLL.ACTIVE() == "ok":
            tc = Button(pos_hint={'x': 0, 'y': 0.95}, size_hint=(1, 0.05))
            tc.background_color = [2, 2, 3, 1]
            self.add_widget(tc)
            self.add_widget(
                Label(text='loading...', font_name='zw.ttf', pos_hint={'x': 0, 'y': 0.95}, size_hint=(1, 0.05)))



            if MYSQLL.activebr("user") == "ok":
                d = MYSQLL.user()
                yh = []
                for i in d:
                    yh.append(i[0])
                if b in yh:
                    for i in d:
                        if i[0] == b:
                            if mdpasswd.pd(c, i[1]) == "ok":
                                br = [b, e]
                                brr = ''.join(sorted(br))
                                abrr = "a" + brr
                                if MYSQLL.active(brr) == "ok" and MYSQLL.aactive(brr) == "ok":
                                    self.clear_widgets()
                                    cur_wdgt = Factory.RootWidget1(b, e, brr, abrr)
                                    self.add_widget(cur_wdgt)
                                else:
                                    MYSQLL.crebr(brr)
                                    MYSQLL.crear(abrr)
                                    self.clear_widgets()
                                    cur_wdgt = Factory.RootWidget1(b, e, brr, abrr)
                                    self.add_widget(cur_wdgt)
                else:
                    pd = mdpasswd.sc(c)
                    MYSQLL.creuser(b, pd)
            else:
                MYSQLL.creut("user")
        else:
            tc = Button(pos_hint={'x': 0, 'y': 0.95}, size_hint=(1, 0.05))
            tc.background_color = [2, 2, 3, 1]
            self.add_widget(tc)
            self.add_widget(Label(text='糟糕！！！！ 没有Network连接哦~~~~', font_name='zw.ttf', pos_hint={'x': 0, 'y': 0.95},
                                  size_hint=(1, 0.05)))



class RootWidget1(FloatLayout):
    def __init__(self, IP, lt, brr, abrr):
        super(RootWidget1, self).__init__()
        self.brr = brr
        self.abrr = abrr
        self.IP = IP
        self.lt = lt

        Config.set('graphics', 'resizable', 0)
        Window.fullscreen = 0
        #Window.size = (380, 600)

        tc = Button(pos_hint={'x': 0, 'y': .95}, size_hint=(1, 0.05))
        tc.background_color = [2, 2, 3, 1]
        self.add_widget(tc)
        cb = CustomBtn3(pos_hint={'x': 0, 'y': 0.95}, size_hint=(1, 0.05))
        self.add_widget(cb)
        self.add_widget(
            Label(text='欢迎 {}  正在与 {} 聊天ing'.format(self.IP, self.lt), font_name='zw.ttf', pos_hint={'x': 0, 'y': 0.95},
                  size_hint=(1, 0.05)))

        self.echo = TextInput(font_name='zw.ttf', size_hint_y=.2, multiline=False, pos_hint={'x': 0, 'y': 0.6},
                              size_hint=(1, 0.35))
        self.add_widget(self.echo)
        self.send = TextInput(font_name='zw.ttf', size_hint_y=.2, multiline=False, pos_hint={'x': 0, 'y': 0.5},
                              size_hint=(0.73, 0.1))
        self.add_widget(self.send)
        self.his = TextInput(font_name='zw.ttf', size_hint_y=.2, multiline=False, pos_hint={'x': 0, 'y': 0},
                             size_hint=(1, 0.45))
        self.add_widget(self.his)

        login = Button(text="SEND", pos_hint={'x': 0.75, 'y': 0.52}, size_hint=(0.23, 0.06))
        login.background_color = [2, 2, 3, 1]
        self.add_widget(login)
        login = Button(text="CLEAR", pos_hint={'x': 0, 'y': 0.45}, size_hint=(0.4, 0.05))
        login.background_color = [2, 2, 3, 1]
        self.add_widget(login)
        login = Button(text="HISTORY", pos_hint={'x': 0.50, 'y': 0.45}, size_hint=(0.4, 0.05))
        login.background_color = [2, 2, 3, 1]
        self.add_widget(login)

        cb1 = CustomBtn4(pos_hint={'x': 0.75, 'y': 0.52}, size_hint=(0.23, 0.06))
        cb1.bind(pressed=self.btn_pressed1)
        self.add_widget(cb1)
        cb2 = CustomBtn5(pos_hint={'x': 0, 'y': 0.45}, size_hint=(0.4, 0.05))
        cb2.bind(pressed=self.btn_pressed2)
        self.add_widget(cb2)
        cb3 = CustomBtn6(pos_hint={'x': 0.5, 'y': 0.45}, size_hint=(0.4, 0.05))
        cb3.bind(pressed=self.btn_pressed3)
        self.add_widget(cb3)

        self.thread_it(self.read)

    @staticmethod
    def thread_it(func):
        t = threading.Thread(target=func)
        t.setDaemon(True)
        t.start()

    def read(self):
        while True:
            yjbcdtime = MYSQLL.S_already(self.lt, self.abrr)
            print(u"   循环 中。。。。。。")
            ltjl = MYSQLL.retu(self.lt, self.brr)
            for i in ltjl:
                if i[1] not in yjbcdtime:
                    ddxx = "{} {}    \n{}\n".format(i[0], self.TIME(i[1]), i[2])
                    self.echo.insert_text(ddxx)
                    MYSQLL.I_already(i[0], i[1], self.abrr)
            time.sleep(1)

    def TIME(self, bbb):
        return (time.strftime("%H:%M:%S", time.localtime(float(bbb))))

    def btn_pressed1(self, instance, pos):
        t = time.time()
        b = self.send.text
        if not b == "":
            bb = "{} {}      \n{}\n".format(self.IP, self.TIME(t), b)
            self.echo.insert_text(bb)
            MYSQLL.insert(self.IP, t, b, self.brr)

    def btn_pressed2(self, instance, pos):
        MYSQLL.delete(self.brr)
        MYSQLL.D_already(self.abrr)

    def btn_pressed3(self, instance, pos):
        if MYSQLL.active(self.brr) == "ok":
            for i in MYSQLL.select(self.brr)[-1::-1]:
                xx = "{}  {}  \n{} \n".format(i[0], self.TIME(i[1]), i[2])
                self.his.insert_text(xx)


class CustomBtn1(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn1, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 ')


class CustomBtn2(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn2, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 ')


class CustomBtn3(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn3, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 ')


class CustomBtn4(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn4, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 {}'.format(pos))


class CustomBtn5(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn5, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 ')


class CustomBtn6(Widget):
    pressed = ListProperty([0, 0])

    def on_touch_down(self, touch):
        if self.collide_point(*touch.pos):
            self.pressed = touch.pos
            return True
        return super(CustomBtn6, self).on_touch_down(touch)

    def on_pressed(self, instance, pos):
        print(u'你单击我了 ')


class TestApp(App):
    def build(self):
        self.color = color = RootWidget()
        color.bind(size=self._update_rect, pos=self._update_rect)
        with self.color.canvas.before:
            Color(2, 1, 0, 2)
            self.rect = Rectangle(size=self.color.size,
                                  pos=self.color.pos)
        return color

    def _update_rect(self, instance, value):
        self.rect.pos = instance.pos
        self.rect.size = instance.size


if __name__ == '__main__':
    TestApp().run()