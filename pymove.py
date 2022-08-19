import time
from Rosmaster_Lib import Rosmaster
import threading
import bot_vision


bot = Rosmaster()
mag_data = {}
current_mag = 1

class BaseMove():
    def __init__(self):
        print('init')
        self.bot = Rosmaster()
        self.bot.create_receive_threading()
        self.bot.set_auto_report_state(True, forever=False)

        # 启动接收数据线程，只能启动一次，所有读取数据的功能都是基于此方法
        thread_mag_record = threading.Thread(target=self.record_mag)
        thread_mag_record.daemon = True
        thread_mag_record.start()

    # 直行
    def go_straight(self, speed=-0.2, proc_time=10):
        self.bot.set_car_motion(speed, 0, 0)
        time.sleep(proc_time)
    
    # 右转
    def turn_right(self, speed=0.25, proc_time=0.05):
        self.bot.set_car_motion(0, 0, speed)
        time.sleep(proc_time)

    # 左转
    def turn_left(self, speed=0.25, proc_time=0.05):
        self.bot.set_car_motion(0, 0, -speed)
        time.sleep(proc_time)

    # 停止
    def stop_move(self, proc_time=5):
        self.bot.set_car_motion(0, 0, 0)
        time.sleep(proc_time)

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

    # 启用光线追踪 无终止，仅最后阶段使用！！！
    def yel_track(self):
        while True:
            x, y, shape, img = bot_vision.sigDetect()
            dire = bot_vision.direction(x, y, shape)
            print(dire)

            if dire == "right":
                print('turn right')
                self.turn_right()
            elif dire == "left":
                print('turn left')
                self.turn_left()

            elif dire == "straight":
                print('go straight')
                self.go_straight()
            
            else:
                print('not found turning right')
                self.turn_right()

            time.sleep(0.1)

    def record_mag(self):
        global mag_data
        global current_mag
        while True:
            inst_mag_data = []
            for i in range(1, 50):
                time.sleep(0.02) # 采样速度
                current_mag = self.bot.get_magnetometer_data()[1]
                print("current: ", current_mag)
                inst_mag_data.append(current_mag)
            ave_mag = sum(inst_mag_data) / len(inst_mag_data)
            mag_data[time.time()] = ave_mag


class AbstractMove():
    def __init__(self):
        self.Absbot = BaseMove()

    def turn_back(self):
        self.Absbot.turn_to(180)

    def straight_and_back(self, distance=10):
        self.Absbot.go_straight(proc_time=distance)
        self.Absbot.stop_move()
        self.turn_back()
        self.Absbot.go_straight(proc_time=distance)
        self.Absbot.stop_move()


robo = AbstractMove()
robo.straight_and_back(5)