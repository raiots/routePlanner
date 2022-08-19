import time
from Rosmaster_Lib import Rosmaster
import threading

bot = Rosmaster()
mag_data = {}
current_mag = 1

class BaseMove():
    def __init__(self):
        self.bot = Rosmaster()
        self.bot.create_receive_threading()
        self.bot.set_auto_report_state(True, forever=False)

        # 启动接收数据线程，只能启动一次，所有读取数据的功能都是基于此方法
        thread_mag_record = threading.Thread(target=self.record_mag)
        thread_mag_record.daemon = True
        thread_mag_record.start()

    # 直行
    def go_straight(self, speed=-0.2, time=10):
        self.bot.set_car_motion(speed, 0, 0)
        time.sleep(time)
    
    # 右转
    def turn_right(self, speed=0.25, time=0.05):
        self.bot.set_car_motion(0, 0, speed)
        time.sleep(time)

    # 左转
    def turn_left(self, speed=0.25, time=0.05):
        self.bot.set_car_motion(0, 0, -speed)
        time.sleep(time)

    # 指定角度转弯
    def turn_to(self, target_degree):
        target_degree = mag_data.get(list(mag_data.keys())[-1]) + target_degree  # 计算目标磁力计角度
        while True:
            if current_mag < target_degree - 5:
                self.turn_right()
            elif current_mag > target_degree + 5:
                self.turn_left()
            else:
                break

    def record_mag(self):
        global mag_data
        global current_mag
        while True:
            inst_mag_data = []
            for i in range(1, 50):
                time.sleep(0.02) # 采样速度
                current_mag = bot.get_magnetometer_data()[1]
                print("current: ", current_mag)
                inst_mag_data.append(current_mag)
            ave_mag = sum(inst_mag_data) / len(inst_mag_data)
            mag_data[time.time()] = ave_mag


class AbstractMove():
    def __init__(self):
        self.Absbot = BaseMove()

    def turn_back(self):
        self.Absbot.turn_to(180)


robo = AbstractMove()
robo.turn_back()