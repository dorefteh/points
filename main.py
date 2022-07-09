# from db.database import engine, get_db
# from components.func import fetch_points, calc_points
from datetime import datetime
from time import time, sleep
import pandas as pd
from kivy.config import Config
from kivymd.app import MDApp
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.textinput import TextInput
from kivy.core.window import Window
import sqlite3

Window.size = (480, 853)


Builder.load_file('main.kv')

class MyBT(TabbedPanel):
        phone = ObjectProperty()
        name = ObjectProperty()
        purchase = ObjectProperty()
        points = ObjectProperty()
        preferences = ObjectProperty()
        notification = ObjectProperty()
        commentary = ObjectProperty()

        def checkbox_click(self, instance, value):
                if value == True:
                        self.ids.input_purchase.disabled = True
                        self.ids.input_pref.disabled = True
                        self.ids.input_notif.disabled = True
                        self.ids.input_comment.disabled = True
                else:
                        self.ids.input_purchase.disabled = False
                        self.ids.input_pref.disabled = False
                        self.ids.input_notif.disabled = False
                        self.ids.input_comment.disabled = False

        #для поиска по номеру
        def show_phone(self):
                self.ids.i2_label.text = ''

                ph = self.ids.find_phone.text

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:
                        c.execute("SELECT * FROM customers WHERE phone = ?", (ph, ))

                        ph_word = ""

                        res = c.fetchall()

                        for r in res:
                                for j in r:
                                        ph_word = f'{ph_word} {j}'
                                        self.ids.i2_label.text = ph_word
                        conn.commit()

                

                except:
                        self.ids.i2_label.text = "Что-то пошло не так"
                finally:
                        conn.close()
                        self.ids.find_phone.text = ''
                        
        def show_name(self):
                self.ids.i2_label.text = ''

                nm = self.ids.find_phone.text

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:
                        c.execute("SELECT * FROM customers WHERE name LIKE %?%", (nm, ))

                        ph_word = ""

                        res = c.fetchall()

                        for r in res:
                                for j in r:
                                        ph_word = f'{ph_word} {j}'
                                        self.ids.i2_label.text = ph_word
                        conn.commit()

                

                except:
                        self.ids.i2_label.text = "Что-то пошло не так"

                finally:
                        conn.close()
                        self.ids.find_phone.text = ''


        #функция для начисления баллов 
        def accural(self, perc = 0.03):

                if self.ids.add_percent:
                        if '.' not in str(perc):
                                perc = int(self.ids.add_percent.text) * 0.01
                        else:
                                perc = float(self.ids.add_percent.text)
                else:
                        pass

                ph = self.ids.phonefio.text

                pur= round(float(self.ids.add_purchase.text), 2)

                po = round(float(pur * perc), 2)

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:

                        c.execute("UPDATE customers SET purchase = purchase + ? WHERE phone = ?", (pur, ph, ))

                        c.execute("UPDATE customers SET points = points + ? WHERE phone = ?", (po, ph))
                        
                        conn.commit()

                        self.ids.i3_label.text = "Операция выполнения"
                except:
                        self.ids.i3_label.text = 'Данный ввод недопустим'

                finally:
                        conn.close()

                        self.ids.phonefio.text = ''

                        self.ids.add_purchase.text = ''

                        self.ids.add_percent.text = ''



        #функция для изменениня данных
        def update_cust(self):

                for_customer = self.ids.rew_for_cust.text

                rewrite_ph = self.ids.rew_phone.text

                rewrite_cust = self.ids.rew_customer.text

                rewrite_pur = self.ids.rew_purchase.text

                rewrite_po = self.ids.rew_points.text

                rewrite_pref = self.ids.rew_pref.text

                rewrite_notif = self.ids.rew_notif.text

                rewrite_comment = self.ids.rew_comment.text

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:

                        if rewrite_ph:

                                c.execute("UPDATE customers SET phone = ?  WHERE phone = ?", (rewrite_ph, for_customer))
                        if rewrite_cust:

                                c.execute("UPDATE customers SET name = ?  WHERE phone = ?", (rewrite_cust, for_customer))
                        if rewrite_pur:

                                c.execute("UPDATE customers SET purchase = ?  WHERE phone = ?", (rewrite_pur, for_customer))
                        if rewrite_po:

                                c.execute("UPDATE customers SET points = ?  WHERE phone = ?", (rewrite_po, for_customer))
                        if rewrite_pref:

                                c.execute("UPDATE customers SET preferences = ?  WHERE phone = ?", (rewrite_pref, for_customer))
                        if rewrite_notif:

                                c.execute("UPDATE customers SET notification = ?  WHERE phone = ?", (rewrite_notif, for_customer))
                        if rewrite_comment:

                                c.execute("UPDATE customers SET commentary = ?  WHERE phone = ?", (rewrite_comment, for_customer))


                        conn.commit()

                        self.ids.i4_label.text = "Данные изменены"
                except:
                        self.ids.i4_label.text = "Недопустимая операция"

                finally:
                        conn.close()

                self.ids.rew_for_cust.text = ''

                self.ids.rew_phone.text = ''

                self.ids.rew_customer.text = ''

                self.ids.rew_purchase.text = ''

                self.ids.rew_points.text = ''

                self.ids.rew_pref.text = ''

                self.ids.rew_notif.text = ''

                self.ids.rew_comment.text = ''


        def delete_cust(self):
                del_customer = self.ids.rew_for_cust.text
                conn = sqlite3.connect('points.db')
                c = conn.cursor()
                try:
                        c.execute("DELETE FROM customers WHERE phone = ?", (del_customer,))
                        conn.commit()
                        self.ids.i4_label.text = "Покупатель был удален из базы"

                except:
                        self.ids.i4_label.text = "Недопустимая операция. Такого покупаетля нет в базе"

                finally:
                        conn.close()
                        self.ids.rew_for_cust.text = ''
        #добавление новых записей
        def submit(self):

                self.ids.item_label.text = ''

                ph = '+'+f"7{self.ids.input_phone.text}"

                n =  self.ids.input_customer.text

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                if self.ids.input_purchase.disabled == False:

                        pur = float(self.ids.input_purchase.text)

                        po = round(pur * 0.03, 2)

                        pref = self.ids.input_pref.text

                        notif = int(self.ids.input_notif.text)

                        comment = self.ids.input_comment.text

                else:
                        pass


                try:
                        if self.ids.input_purchase.disabled == True:
                                #Добавление информации в таблицу
                                c.execute("INSERT INTO customers(phone, name) VALUES (?, ?)", (ph, n))

                                #Применяем изменения
                                conn.commit()

                                self.ids.item_label.text = f'Покупатель {n} добавлен'

                        else:
                                #Добавление информации в таблицу
                                c.execute("INSERT INTO customers VALUES (?, ?, ?, ?, ?, ?, ?)", (ph, n, pur, po, pref, notif, comment))

                                #Применяем изменения
                                conn.commit()

                                self.ids.item_label.text = f'Покупатель {n} добавлен'

                except:

                        self.ids.item_label.text = 'Данный ввод недопустим'

                finally:
                        #Закрытие соединения
                        conn.close()

                        self.ids.input_phone.text = ''
                        self.ids.input_customer.text = ''
                        self.ids.input_purchase.text = ''
                        self.ids.input_pref.text = ''
                        self.ids.input_notif.text = ''
                        self.ids.input_comment.text = ''


        #выгрузка текущего состояния бд
        def make_report(self):
                self.ids.i2_label.text = ''

                now = datetime.now()

                day = now.strftime("%d.%m.%Y")

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:
                        df_customers = pd.read_sql_query("SELECT * FROM customers", conn)

                        df_customers.to_excel(f'{day}otchet.xlsx', 'Отчет', startrow=4)

                except:
                        self.ids.i2_label.text = "Что-то пошло не так"

                finally:
                        conn.close()

        def all_data(self):
                self.ids.i2_label.text = ''

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                try:
                        c.execute("SELECT * FROM customers")

                        ph_word = ""

                        inc = 0

                        res = c.fetchall()

                        for r in res:
                                for j in r:
                                        if inc % 7 == 0:
                                                ph_word +="\n"
                                                ph_word = f'{ph_word} {j}'
                                                self.ids.i2_label.text = ph_word
                                                inc += 1
                                        else:
                                                ph_word = f'{ph_word} {j}'
                                                self.ids.i2_label.text = ph_word
                                                inc += 1
                        conn.commit()



                

                except:
                        self.ids.i2_label.text = "Что-то пошло не так"
                finally:
                        conn.close()





#Изменение настроек для появления экранной клавиатуры в мобильной версии
Config.set('kivy', 'keyboard_mode', 'systemanddock')



#класс приложения
class MyApp(MDApp):
        running = True

        def build(self):

                self.theme_cls.theme_style = "Dark"
                self.theme_cls.primary_palette = "LightBlue"
                self.theme_cls.secondary_palette = "Amber"
                self.theme_cls.accent_palette = "Gray"

                conn = sqlite3.connect('points.db')

                c = conn.cursor()

                c.execute("""CREATE TABLE if not exists customers(
                        phone TEXT NOT NULL,
                        name TEXT NOT NULL,
                        purchase REAL DEFAULT '0',
                        points REAL DEFAULT '0',
                        preferences TEXT DEFAULT '',
                        notification INTEGER DEFAULT '2',
                        commentary TEXT DEFAULT ''
                        )
                        """)

                conn.commit()

                conn.close()

                return MyBT()



        def on_stop(self):
                self.running = False

if __name__ == '__main__':
        MyApp().run() 