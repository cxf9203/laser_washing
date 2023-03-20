#文件包括 pyuiclaser.py
import serial
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import*
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import pyuiclaser
import math
import pyfirmata
#字符替换函数
def strreplace(inputstr,index,des):
    lst = list(inputstr)
    lst[index] = des
    s = ''.join(lst)
    return s
class MainCode(QMainWindow, pyuiclaser.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #在这往下可以加功能
        self.pushButton.clicked.connect(self.redlight)#按钮绑定函数
        self.pushButton_2.clicked.connect(self.cf_energy)  # 按钮绑定函数
        self.pushButton_3.clicked.connect(self.cf_frequency)
        self.pushButton_4.clicked.connect(self.cancel_fre)#取消激光
        self.pushButton_5.clicked.connect(self.ena_laser)  # 出激光
        self.pushButton_6.clicked.connect(self.disena_laser)#关闭激光
        self.pushButton_7.clicked.connect(self.disena_energy)#关闭能量
        self.init()
    def init(self):
        # connect to the Arduino board
        self.ser = serial.Serial('COM7', 115200) # Change the COM port to match your Arduino
        self.cmd = '0000000000000' #初始字符串指令
        self.frequency = 0
        self.frequency_flag = False
        self.energy_flag = False
        self.laser_flag = False
        #print(self.pin13)
        #初始化出红光
        self.redflag = False
    def disena_energy(self):
        if not self.laser_flag:
            for i in range(8):
                self.cmd = strreplace(self.cmd, i + 1, '0')
                self.ser.write(self.cmd.encode())
                print(self.cmd)
    def ena_laser(self):
        try:
            if self.redflag :#先关闭红光
                self.cmd = strreplace(self.cmd, 0, '0')
                self.ser.write(self.cmd.encode())  # Send the "redlight close" signal to Arduino pin13
                self.pushButton.setText("开红光")
            if self.energy_flag and self.frequency_flag:#都设置好后才可以出激光
                self.cmd = strreplace(self.cmd, 12, '1')#激光使能
                self.ser.write(self.cmd.encode())
                self.laser_flag = True
                print(self.cmd)
        except:
            print("error happen")

    def disena_laser(self):
        #todo 关闭激光
        if self.laser_flag:
            self.cmd = strreplace(self.cmd, 12, '0')  # 激光使能
            self.ser.write(self.cmd.encode())
            self.laser_flag = False
            print(self.cmd)
    def cancel_fre(self):
        if self.frequency_flag:
            self.cmd = strreplace(self.cmd, 9, '0') #取消激光频率
            self.ser.write(self.cmd.encode())
            self.frequency_flag = False
            print(self.cmd)
            self.disena_laser()
    def cf_frequency(self):
        try:
            ret = int(self.lineEdit_2.text())
            if ret >=20 and ret <=60:
                print(ret*1000)
                self.frequency = ret * 1000 #set frequency
                period = 1 / self.frequency  # Blink period in seconds
                on_time = period / 2 # Time for LED to be on in seconds
                string_on_time = str(int(on_time*1000000))
                newchar = '0'
                new_string = newchar+string_on_time
                print(new_string )

                self.cmd = strreplace(self.cmd, 9, '1')
                self.cmd = strreplace(self.cmd, 10, new_string [-2])
                self.cmd = strreplace(self.cmd, 11,  new_string [-1])
                print(self.cmd)
                self.ser.write(self.cmd.encode())
                self.frequency_flag = True
            else:
                print("not in correct frequency range")
        except:
            print("incorrect input")


    def cf_energy(self):
        ret = self.lineEdit.text()
        try:
            num = float(ret)
            if num >= 0 and num<=100:
                ret =math.ceil(num * 255/100)
                b_ret1 = bin(ret)
                print(b_ret1)
                b_new_ret = '000000'+b_ret1[2:] #高位补齐
                b_ret = b_new_ret[-8:]  #取后八位
                print(b_ret)
                print("run here")
                for i in range(8):
                    self.cmd = strreplace(self.cmd, i+1, str(b_ret[i]))  
                print(self.cmd)
                self.energy_flag = True
                self.ser.write(self.cmd.encode())

            else:
                print("请输入正确数字")
        except:
            print("程序有误，可能数字输入错误")
    #def set_energy_IO(self,Dinput):
    def redlight(self):
        if not self.redflag:
            self.cmd = strreplace(self.cmd,0,'1')#红光开启
            self.ser.write(self.cmd.encode())  # Send the "redlight" signal to Arduino pin13
            self.pushButton.setText("关红光")
            self.redflag = True
        else:
            self.redflag = False
            self.cmd = strreplace(self.cmd, 0, '0')
            self.ser.write(self.cmd.encode()) # Send the "redlight close" signal to Arduino pin13
            self.pushButton.setText("开红光")




app = QApplication(sys.argv)
Main_gui = MainCode()
Main_gui.show()
sys.exit(app.exec_())
