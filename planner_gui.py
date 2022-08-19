import datetime
from optparse import Values
from turtle import color, position
from unicodedata import name
import npyscreen
import os, time
import threading
from Rosmaster_Lib import Rosmaster

# 这里应用充当了 curses 初始化封装器的角色
# 同时也管理着应用的实际形态.

logo = """
        .__              .__             __________.__                                     
  _____ |__| ______ _____|__| ____   ____\______   \  | _____    ____   ____   ___________ 
 /     \|  |/  ___//  ___/  |/  _ \ /    \|     ___/  | \__  \  /    \ /    \_/ __ \_  __ \\
|  Y Y  \  |\___ \ \___ \|  (  <_> )   |  \    |   |  |__/ __ \|   |  \   |  \  ___/|  | \/
|__|_|  /__/____  >____  >__|\____/|___|  /____|   |____(____  /___|  /___|  /\___  >__|   
      \/        \/     \/               \/                   \/     \/     \/     \/       
============================================================================================
"""
class routePlanner(npyscreen.NPSAppManaged):
    def onStart(self):
        self.main_form = MainForm()
        self.registerForm("MAIN", self.main_form)

    #     thread_time = threading.Thread(target=self.update_time,args=())
    #     thread_time.daemon = True
    #     thread_time.start()

    # def update_time(self):
    #     bot = Rosmaster()
    #     # 启动接收数据，只能启动一次，所有读取数据的功能都是基于此方法
    #     # Start to receive data, can only start once, all read data function is based on this method
    #     bot.create_receive_threading()
    #     bot.set_auto_report_state(True, forever=False)

    #     while True:
    #         current_mag = bot.get_magnetometer_data()[1]
    #         self.main_form.mag_value.value = str(current_mag)
    #         self.main_form.date_time.value = str(datetime.datetime.now())
    #         self.main_form.display()
    #         time.sleep(1)


class RecordListDisplay(npyscreen.FormMutt):
    def beforeEditing(self):
        self.update_list()


# 这个窗口类定义了展示给用户的显示内容.

class MainForm(npyscreen.Form):
    def create(self):
        self.name = "Route Planner"
        self.color = 'STANDOUT'
        # self.add(npyscreen.TitleFixedText, name="Start Point", value="0,0")
        self.add(npyscreen.MultiLineEdit, max_height=9, value=logo, editable=False)
        # self.add(RecordListDisplay, name="Route List", values=[1,11,1])
        self.date_time = self.add(npyscreen.TitleText, name = "Current Time:", value= "NOT Connected", editable=False, color="CONTROL")
        self.add(npyscreen.TitleText, name="Driver Board Status: ", value="Connected", editable=False, color="CONTROL")
        self.add(npyscreen.TitleText, name = "IMU Status:", value= "OK", editable=False, color="CONTROL")
        self.add(npyscreen.TitleText, name = "Motor 1 Control:", value= "ONLINE", editable=False, color="CONTROL")
        self.add(npyscreen.TitleText, name = "Motor 3 Control:", value= "ONLINE", editable=False, color="CONTROL")
        self.mag_value = self.add(npyscreen.TitleText, name = "Magnetometer:", value= "NULL", editable=False, color="CONTROL")
        
        self.route_selected = self.add(npyscreen.TitleSelectOne, max_height=4, value = [0], name="Move Mode",
                values = ["Straight and back","Round","Grass Cutter"], scroll_exit=True)


    def afterEditing(self):
        self.parentApp.setNextForm(None)
    def txt(name,text):              #定义函数名
        b = os.getcwd()[:-4] + 'new\\'
    
        if not os.path.exists(b):     #判断当前路径是否存在，没有则创建new文件夹
            os.makedirs(b)
    
        xxoo = b + name + '.txt'    #在当前py文件所在路径下的new文件中创建txt
    
        file = open(xxoo,'w')
    
        file.write(text)        #写入内容信息
    
        file.close()
        print ('ok')
    

    def on_ok(self):
        print(111)
        print(self.route_selected.value)
        self.txt('test','hello,python')       #创建名称为test的txt文件，内容为hello,python



if __name__ == '__main__':
    TA = routePlanner()
    TA.run()