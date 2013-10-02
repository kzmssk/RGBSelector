import Tkinter as Tk
import serial
import time

class Frame(Tk.Frame):
	def __init__(self, master=None):
		self.serialPort = serial.Serial('/dev/tty.usbmodem1412', timeout = 0.1)
		self.R = 0
		self.G = 0
		self.B = 0
		self.tmpR = 0
		self.tmpG = 0
		self.tmpB = 0
		self.sw = 0
		
		Tk.Frame.__init__(self, master)
		self.master.title('RGB Selector')
		self.scaleR = Tk.Scale(master, label='R', orient='h', from_=0, to=255, command=self.scaleR)
		self.scaleR.pack()
		self.scaleG = Tk.Scale(master, label='G', orient='h', from_=0, to=255, command=self.scaleG)
		self.scaleG.pack()
		self.scaleB = Tk.Scale(master, label='B', orient='h', from_=0, to=255, command=self.scaleB)
		self.scaleB.pack()
		self.sampleColor = Tk.Label(master, text = 'target color')
		self.sampleColor.pack()
		
	def __del__(self):
		self.serialPort.close()
	
	def scaleR(self, n):
		self.R= int(n)
		self.changeColorSamlple()
		
	def scaleG(self, n):
		self.G = int(n)
		self.changeColorSamlple()
		
	def scaleB(self, n):
		self.B = int(n)
		self.changeColorSamlple()
		
	def outRGB(self):
		#ouput char[12] code for mbed
		rgbMessage='%03d,%03d,%03d\n' % (self.R, self.G, self.B)
		#print rgbMessage
		
		self.serialPort.write(rgbMessage)
		time.sleep(0.1)
	
	def changeColorSamlple(self):
		color = '#%02x%02x%02x' % (int(self.R), int(self.G), int(self.B))
		self.sampleColor.configure(bg = color)
	
	def selfupdate(self):
		#serial read
		data = self.serialPort.readline()
		print data
		#after sw was on, and R or G or B is changed
		if self.sw == 1:
			if self.tmpR != self.R:
				self.G = self.tmpG
				self.B = self.tmpB
				self.sw = 0
			elif self.tmpG != self.G:
				self.R = self.tmpR
				self.B = self.tmpB
				self.sw = 0
			elif self.tmpB != self.B:
				self.R = self.tmpR
				self.G = self.tmpG
				self.sw = 0
		
		#if sw is on, self.R self.G self.B = 000 000 000  and save buff
		if data == '1':
			print 'sw on'
			self.sw = 1
			self.tmpR = self.R
			self.tmpG = self.G
			self.tmpB = self.B
			self.R = 0
			self.G = 0
			self.B = 0			
			print '%03d,%03d,%03d\n' % (self.R, self.G, self.B)

		self.outRGB()
		self.tmpData = data
		#loop
		self.after(50, self.selfupdate)
		
	
		
if __name__ == '__main__':
	f = Frame()
	f.pack()
	f.selfupdate()
	f.mainloop()
