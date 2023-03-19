#文件包括 laser.py
import serial
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import*
from PyQt5.QtWidgets import *
from PyQt5 import QtGui
import sys
import laser
import math
import pyfirmata
class MainCode(QMainWindow, laser.Ui_MainWindow):
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        #在这往下可以加功能
        self.pushButton.clicked.connect(self.redlight)#按钮绑定函数
        self.pushButton_2.clicked.connect(self.cf_energy)  # 按钮绑定函数
        self.pushButton_3.clicked.connect(self.cf_frequency)
        self.init()
    def init(self):
        # connect to the Arduino board
        self.board = pyfirmata.Arduino('com7')
        # start an iterator thread to update the values of the pins
        self.it = pyfirmata.util.Iterator(self.board)
        self.it.start()
        # define the pins to control
        self.pins = [self.board.get_pin('d:{}:o'.format(i)) for i in range(2, 10)] #energy pin
        self.pin13 = self.board.get_pin('d:13:o') #red light
        self.pin10 = self.board.get_pin('d:10:p') #frequency
        self.pin11 = self.board.get_pin('d:11:o')  # pre output
        self.pin12 = self.board.get_pin('d:12:o')  # chuguang za
        self.pin10.mode=pyfirmata.PWM
        self.frequency_flag = False
        self.energy_flag = False
        #print(self.pin13)
        #初始化出红光
        self.redflag = False
    def cf_frequency(self):
        try:
            ret = int(self.lineEdit_2.text())
            if ret >=0 and ret <=60:
                print(ret*1000)
                self.pin10.frequency = ret * 1000 #set frequency
                #print()
                self.pin10.write(0.5) #set duty cycle
                #print("run here")

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
                b_ret = bin(ret)
                #print(ret)
                #print(b_ret)
                print(b_ret[2],b_ret[3],b_ret[4],b_ret[5],b_ret[6],b_ret[7],b_ret[8],b_ret[9])
                D0_7 = [b_ret[2],b_ret[3],b_ret[4],b_ret[5],b_ret[6],b_ret[7],b_ret[8],b_ret[9]]
                print("run here")
                for i in range(len(D0_7)):
                    self.pins[i].write(int(D0_7[i]))  # set do2-do9


            else:
                print("请输入正确数字")
        except:
            print("程序有误，可能数字输入错误")
    #def set_energy_IO(self,Dinput):
    def redlight(self):
        if not self.redflag:
            #print(self.pin13)
            self.pin13.write(1) # Send the "redlight" signal to Arduino pin13
            self.pushButton.setText("关红光")
            self.redflag = True
        else:
            self.redflag = False
            self.pin13.write(0)  # Send the "redlight close" signal to Arduino pin13
            self.pushButton.setText("开红光")




app = QApplication(sys.argv)
Main_gui = MainCode()
Main_gui.show()
sys.exit(app.exec_())