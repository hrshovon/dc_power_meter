import sys
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication,QWidget
from panalyze_gui import Ui_power_logger_gui
import serial
import serial.tools.list_ports
import threading
import time
import random

class logger_gui(QtWidgets.QMainWindow,Ui_power_logger_gui):
	def __init__(self):
		super(self.__class__,self).__init__()
		self.setupUi(self)
		#attach functions to events such as clicks etc
		self.bttnrefreshports.clicked.connect(self.load_ports)
		self.bttnconnect.clicked.connect(self.connect_event)
		self.rdoma.clicked.connect(self.set_c_ma)
		self.rdoa.clicked.connect(self.set_c_a)
		self.rdomw.clicked.connect(self.set_p_mw)
		self.rdow.clicked.connect(self.set_p_w)
		
		
		#load the ports
		self.load_ports()
		#initiate connect button toggle
		self.is_connect=True #means if button caption is Connect
		self.serial_connect=False
		#now, initiate plot buffer and things
		self.c_unit="mA"
		self.p_unit="mW"
		
		self.plotter_buffer_vy=[]
		self.plotter_buffer_x=[]
		
		self.plotter_buffer_cy=[]
		self.plotter_buffer_py=[]
		
		self.update_rate=int(self.txtupdaterate.text())
		
		self.serial_obj=serial.Serial()
		self.serial_obj.timeout=1
		self.serial_stop_event=threading.Event()
		self.serial_thread=threading.Thread(target=self.serial_function,args=(self.serial_stop_event,))
		self.serial_thread.start()
		print "starting timer"
		self.timer = QtCore.QTimer()
		self.timer.timeout.connect(self.plotupdater)
	
	def set_c_ma(self):
		self.c_unit="mA"
	def set_c_a(self):
		self.c_unit="A"
	def set_p_mw(self):
		self.p_unit="mW"
	def set_p_w(self):
		self.p_unit="W"
	
	
	def closeEvent(self, event):
		self.serial_stop_event.set()
		if self.serial_obj.is_open==True:
			self.serial_obj.close()
		event.accept()
		
	
	def connect_event(self):
		#print "test"
		if self.is_connect==True:
			try:
				self.serial_obj.port=str(self.cboportlist.currentText())
				self.serial_obj.baudrate=self.txtbaudrate.text()
				self.serial_obj.open()
				self.timer.setInterval((1/self.update_rate)*1000)
				self.timer.start()
				#return
				self.serial_connect=True
				self.bttnconnect.setText('Disconnect')
				self.is_connect=False
			except Exception,e: print str(e)
		elif self.is_connect==False:
			try:
				self.serial_connect=False
				self.timer.stop()
				self.bttnconnect.setText('Connect')
				self.is_connect=True
				self.serial_obj.close()
			except Exception,e: print str(e)
	def convert_current(self,current,rcv_unit):
		if rcv_unit=="A" and self.c_unit=="mA":
			return current*1000
		elif rcv_unit=="mA" and self.c_unit=="A":
			return current/1000
		else:
			return current
	
	def convert_power(self,power,rcv_unit):
		if rcv_unit=="W" and self.p_unit=="mW":
			return power*1000
		elif rcv_unit=="mW" and self.p_unit=="W":
			return power/1000
		else:
			return power
		
			
	def load_ports(self):
		port_list=[port[0] for port in serial.tools.list_ports.comports() if port[2]!='n/a']
		self.cboportlist.clear()
		self.cboportlist.addItems(port_list)
		
	def plotupdater(self):
		self.plotview_V.clear()
		self.plotview_C.clear()
		self.plotview_P.clear()
		self.plotview_V.setLabels(left=('Voltage(V)'),bottom=('time(ms)'))
		self.plotview_C.setLabels(left=('Current('+self.c_unit+')'),bottom=('time(ms)'))
		self.plotview_P.setLabels(left=('Power('+self.p_unit+')'),bottom=('time(ms)'))
		self.plotview_V.plot(self.plotter_buffer_x,self.plotter_buffer_vy)
		self.plotview_C.plot(self.plotter_buffer_x,self.plotter_buffer_cy)
		self.plotview_P.plot(self.plotter_buffer_x,self.plotter_buffer_py)
		
		#print "updating"
	def serial_function(self,stop_event):
		x=0
		y=0
		while not stop_event.isSet():
			if self.serial_connect==True:
				line=self.serial_obj.readline()
				data_list=line.split(',')
				if len(data_list)==5:					
					
					try:
						c_unit=data_list[2]
						p_unit=data_list[4][0:len(data_list[4])-2]
						voltage=float(str(data_list[0]))
						current=self.convert_current(float(str(data_list[1])),c_unit)
						power=self.convert_power(float(str(data_list[3])),p_unit)
						
						self.plotter_buffer_x.append(x)
						self.plotter_buffer_vy.append(voltage)
						self.plotter_buffer_cy.append(current)
						self.plotter_buffer_py.append(power)
						
						self.plotter_buffer_vy=self.plotter_buffer_vy[-100:]
						self.plotter_buffer_cy=self.plotter_buffer_cy[-100:]
						self.plotter_buffer_py=self.plotter_buffer_py[-100:]
						
						self.plotter_buffer_x=self.plotter_buffer_x[-100:]
					except Exception,e: print str(e)
				#plotter.plot([x],[y])
				#print len(self.plotter_buffer)
				time.sleep(0.001)
				x+=1
			else:
				time.sleep(0.01)
if __name__=="__main__":
	app=QtWidgets.QApplication(sys.argv)
	ui_logger=logger_gui()
	ui_logger.show()
	sys,exit(app.exec_())
