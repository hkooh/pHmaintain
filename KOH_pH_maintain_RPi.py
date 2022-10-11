#!/usr/bin/env python


import RPi.GPIO as GPIO
import serial
import time
import statistics


def receive_serial():
    #マイコンからシリアル通信を介してfloat型のpH値を取得する

    PHSENSOR_USB_PORT =  "/dev/ttyACM0" #マイコンのディレクトリ
    #使用するUSBポートを確認して変更する

    ser = serial.Serial(pHsensor_USB_port, 9600)
    time.sleep(2) #マイコンの起動待ち
    ser.write(b"1")
    time.sleep(60) #マイコンの処理待ち
    rcvdata = ser.readline()
    return  float(rcvdata.decode())


def shift_10frame_pHValue(arr, n):
    #リスト内のpH値のデータをn個右にずらす

    result = arr[n:] + arr[:n]
    result += [receive_serial()]
    return  result

def judge():
    #リストにpH値を10個格納する

    result = []
    for i in range(10):

        result += [receive_serial()]
    return  result


#10個のpH値からなるフレームを3個分作成する
LASTLAST_FRAME_PHVALUE = judge()
LAST_FRAME_PHVALUE = shift_10frame_pHValue(LASTLAST_FRAME_PHVALUE, 1)
FRAME_PHVALUE = shift_10frame_pHValue(LAST_FRAME_PHVALUE, 1)


try:

   while True:

       #3個のフレームから平均pH値をそれぞれ算出する
       SUMAVERAGE_LASTLAST_FRAME_PHVALUE = statistics.mean(LASTLAST_FRAME_PHVALUE)
       SUMAVERAGE_LAST_FRAME_PHVALUE = statistics.mean(LAST_FRAME_PHVALUE)
       SUMAVERAGE_FRAME_PHVALUE = statistics.mean(FRAME_PHVALUE)

       print(SUMAVERAGE_FRAME_PHVALUE) #マイコンから出力されるpH値を確認

       PH_THRESHOLD = 1.65
       KOH_OUTPUTCHANNEL = 22
       KOH_INJECTION_TIME = 0.75
       #pH値の閾値をPH_THRESHOLDに、ポンプが接続しているピン(BCM)をKOH_OUTPUTCHANNELに、KOHを注入する時間をKOH_INJECTION_TIME(秒)に代入する

       #3個のフレーム全部がpH値の閾値を下回っていたら、KOHを注入する
       if SUMAVERAGE_FRAME_PHVALUE < PH_THRESHOLD and SUMAVERAGE_LAST_FRAME_PHVALUE < PH_THRESHOLD and SUMAVERAGE_LASTLAST_FRAME_PHVALUE < PH_THRESHOLD:

           GPIO.setwarnings(False) #warningを出させない
           GPIO.setmode(GPIO.BCM)
           GPIO.setup(KOH_OUTPUTCHANNEL, GPIO.OUT, initial = GPIO.LOW)
           GPIO.output(KOH_OUTPUTCHANNEL, GPIO.HIGH)
           time.sleep(KOH_INJECTION_TIME)
           GPIO.output(KOH_OUTPUTCHANNEL, GPIO.LOW)
           GPIO.cleanup()
           print("Make_pump_on_and_pour_some_KOH")
           time.sleep(1800) #KOHが混ざりきるのを待つ

           LASTLAST_FRAME_PHVALUE = judge()
           LAST_FRAME_PHVALUE = shift_10frame_pHValue(LASTLAST_FRAME_PHVALUE, 1)
           FRAME_PHVALUE = shift_10frame_pHValue(LAST_FRAME_PHVALUE, 1)

       #3個のフレーム全部がpH値の閾値を下回っていなかったら、フレームを1個ずらしてもう一度判定を行う
       else:

           time.sleep(10)
           LASTLAST_FRAME_PHVALUE = LAST_FRAME_PHVALUE
           LAST_FRAME_PHVALUE = FRAME_PHVALUE
           FRAME_PHVALUE = shift_10frame_pHValue(FRAME_PHVALUE, 1)


except KeyboardInterrupt:
    #「Ctrl + C」でプログラムの中断

    print("Stop_maintaining_pH")
