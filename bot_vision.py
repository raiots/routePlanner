import numpy as np
import cv2
import os, time
import bot_led as led


def sigDetect():
    capCamera = cv2.VideoCapture(0)
    return_value, image = capCamera.read()

    # 设定颜色HSV范围，假定为红色
    redLower = np.array([159, 160, 100])
    redUpper = np.array([179, 255, 255])

    # 读取图像
    img = image

    # 将图像转化为HSV格式
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # 去除颜色范围外的其余颜色
    mask = cv2.inRange(hsv, redLower, redUpper)

    # 二值化操作
    ret, binary = cv2.threshold(mask, 0, 255, cv2.THRESH_BINARY)

    # 膨胀操作，因为是对线条进行提取定位，所以腐蚀可能会造成更大间隔的断点，将线条切断，因此仅做膨胀操作
    kernel = np.ones((5, 5), np.uint8)
    dilation = cv2.dilate(binary, kernel, iterations=1)
    #
    # img2 = cv2.bitwise_and(img, img, mask=mask)
    # cv2.imshow('image', mask)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()

    # 获取图像轮廓坐标，其中contours为坐标值，此处只检测外形轮廓
    contours, hierarchy = cv2.findContours(dilation, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    aim_box = (0, 0, 0, 0)
    if len(contours) > 0:
        print('Run!')
        led.set_led('Green')
        # cv2.boundingRect()返回轮廓矩阵的坐标值，四个值为x, y, w, h， 其中x, y为左上角坐标，w,h为矩阵的宽和高
        boxes = [cv2.boundingRect(c) for c in contours]
        for box in boxes:
            x, y, w, h = box
            if box[2] * box[3] > aim_box[2] * aim_box[3]:
                aim_box = box
            # print(box)
    else:
        led.set_led('Red')

    x, y, w, h = aim_box
    # print(aim_box)
    # 绘制矩形框对轮廓进行定位
    cv2.rectangle(img, (x, y), (x + w, y + h), (153, 153, 0), 2)
    # 将绘制的图像保存并展示
    cv2.putText(img, 'DIST', (x, y), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
    # cv2.imshow('image', img)
    # cv2.waitKey(0)
    capCamera.release()
    cv2.destroyAllWindows()
    return x, y, img.shape, img


def direction(x, y, shape):
    wide = shape[0]
    print(wide)
    if x < wide * (2 / 5):
        return 'left'
    elif wide * (2 / 5) <= x <= wide * (3 / 5):
        return 'straight'
    elif x > wide * (3 / 5):
        return 'right'
    else:
        return 'error: 位置超出范围'


# while True:
#     # time.sleep(1)
#     x, y, shape, img = sigDetect()
#     # cv2.imshow("ss", img)
#     # if cv2.waitKey(1) & 0xFF == ord('q'):
#     #     break
#     print(x, y)
#     dire = direction(x, y, shape)
#     print(dire)