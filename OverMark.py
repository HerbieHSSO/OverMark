from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import sys
from cpu import Processor
import threading

from threading import Thread
from PyQt5.QtGui import QPixmap
from PyQt5.QtCore import *
from PyQt5.QtGui import *


from CPU.vector import *
import multiprocessing as mp

import time
import os
import requests

from PyQt5.QtCore import pyqtSignal


try:
# PyInstaller creates a temp folder and stores path in _MEIPASS
    base_path = sys._MEIPASS
except Exception:
    base_path = os.path.abspath(".")
    

vector_form, vector_base = uic.loadUiType(os.path.join(base_path, 'Designer/vector.ui'))









class OverMark(QMainWindow):
    def __init__(self):
        super().__init__()

        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")

        self.overmark = uic.loadUi(os.path.join(base_path, 'Designer/main.ui'), self)
        

        self.processor = Processor()
        
        try:
            self.processor.name().find('Intel')
            pixmap = QPixmap(os.path.join(base_path, 'Designer/intel.png'))
            self.overmark.logo.setPixmap(pixmap)
            self.overmark.logo.setScaledContents(True)
            
        except:
            try:
                self.processor.name().find('AMD')
                pixmap = QPixmap(os.path.join(base_path, 'Designer/AMD.png'))
                self.main_window.logo.setPixmap(pixmap)
                self.main_window.logo.setScaledContents(True)
            except:
                None

  
        #--------------------CPU---------------------
        
        self.overmark.cpu.setText(f'{self.processor.name()}')
        self.overmark.specification.setText(self.processor.spec())

        #Cores------------------------------
        self.overmark.cores.setText('{}'.format(self.processor.cores()))
        self.overmark.threads.setText('{}'.format(self.processor.threads()))

        self.overmark.Core1.setHidden(True)
        self.overmark.Core2.setHidden(True)
        self.overmark.Core3.setHidden(True)
        self.overmark.Core4.setHidden(True)
        self.overmark.Core5.setHidden(True)
        self.overmark.Core6.setHidden(True)
        self.overmark.Core7.setHidden(True)
        self.overmark.Core8.setHidden(True)
        self.overmark.Core9.setHidden(True)
        self.overmark.Core10.setHidden(True)
        self.overmark.Core11.setHidden(True)
        self.overmark.Core12.setHidden(True)

        
        
        self.overmark.SingleCore.clicked.connect(self.SCBenchmarkUI)
        self.overmark.MultiCore.clicked.connect(self.MCBenchmarkUI)
        self.overmark.upload.clicked.connect(self.UPLOAD)
        
        self.pill2kill = threading.Event()
        self.t1 = Thread(target=self.update, args=(self.pill2kill, "task"))
        self.t1.start()
        
    def closeEvent(self, event):

        event.accept()
        self.pill2kill.set()
        self.t1.join()
        


    def UPLOAD(self):
        None
        



    def setRenderScore(self, the_signal):
        print(f'.{the_signal}')
        self.overmark.RenderScore.setText(f'{the_signal}')
        
    def setFP32Score(self, vector_signal):
        print(f'.{vector_signal}')
        self.overmark.FPScore.setText(f'{vector_signal}')
    def setINT32Score(self, vector_signal):
        print(f'.{vector_signal}')
        self.overmark.INTScore.setText(f'{vector_signal}')  
    def setMultiFP32Score(self, vector_signal):
        print(f'.{vector_signal}')
        self.overmark.MultiFPScore.setText(f'{vector_signal}') 
    def update(self, stop_event, arg):

        cores = self.processor.cores()
        
        if cores == 2:
            self.overmark.Core1.setHidden(False)
            self.overmark.Core2.setHidden(False)

            
            while not stop_event.wait(1):
           
                
                clock = self.processor.current()
                self.overmark.clockCPU0.setText('%.2f MHz' % float(clock.split('#1: ')[1].split(',')[0]))
                self.overmark.clockCPU1.setText('%.2f MHz' % float(clock.split('#2: ')[1].split(',')[0]))

                    
                self.overmark.tdp.setText('%.1fW' % float(self.processor.power().split(': ')[1].split(',')[0]))


             
                self.overmark.temp.setText(f'{self.processor.temp()}')

  
    def SCBenchmarkUI(self):


     
            
        if self.overmark.benchmark.currentText() == "Floating Point":
            self.FloatingPoint = SingleVectorUI(self)
            
        if self.overmark.benchmark.currentText() == "Integer":
            self.Integer = SingleIntegerUI(self)
      
    def MCBenchmarkUI(self):
            
        if self.overmark.benchmark.currentText() == "Floating Point":
            self.FloatingPoint = MultiVectorUI(self)







              








class SingleVectorUI(vector_form, vector_base):
    got_signal = pyqtSignal(str)
    def __init__(self, parent):
        super(vector_base, self).__init__()
        self.setupUi(self)

        self.parent = parent
        
        DEFAULT_STYLE = """
        QProgressBar{
            border: 1px solid #cccccc;
            border-radius: 5px;
            text-align: center
        }

        QProgressBar::chunk {
            background-color: #00aa7f;
            border-radius: 5px;
            border: 1px #00aa7f;
        }
        """

        
        tFP32 = Thread(target=self.FP32)
        tFP32.start()
        
        self.save.clicked.connect(self.btnClicked)
            
        
        self.show()
    def btnClicked(self):
      
        
        self.got_signal.connect(self.parent.setFP32Score)
        self.got_signal.emit(self.fp32.text())
        
        self.close()
    def FP32(self):
        queue = mp.Queue()
        
        pFP16 = mp.Process(target=SingleThread.FP16, args=(queue, ))
        pFP16.start()
        pFP16.join()

        self.fp16.setText(queue.get())
        
        queue = mp.Queue()
        
        pFP32 = mp.Process(target=SingleThread.FP32, args=(queue, ))
        pFP32.start()
        pFP32.join()
        

        self.fp32.setText(queue.get())

        queue = mp.Queue()
        
        pFP64 = mp.Process(target=SingleThread.FP64, args=(queue, ))
        pFP64.start()
        pFP64.join()
        
        self.fp64.setText(queue.get())

        self.save.setEnabled(True)

        
class MultiVectorUI(vector_form, vector_base):
    got_signal = pyqtSignal(str)
    def __init__(self, parent):
        super(vector_base, self).__init__()
        self.setupUi(self)

        self.parent = parent
        
        DEFAULT_STYLE = """
        QProgressBar{
            border: 1px solid #cccccc;
            border-radius: 5px;
            text-align: center
        }

        QProgressBar::chunk {
            background-color: #00aa7f;
            border-radius: 5px;
            border: 1px #00aa7f;
        }
        """

        self.label_5.setText('MultiThread')
        tFP32 = Thread(target=self.FP32)
        tFP32.start()
        
        
        self.save.clicked.connect(self.btnClicked)    
        
        self.show()
    def btnClicked(self):
      
        
        self.got_signal.connect(self.parent.setMultiFP32Score)
        self.got_signal.emit(self.fp32.text())
        
        self.close()
    def FP32(self):
        queue = mp.Queue()
        
        pFP16 = mp.Process(target=MultiThread.FP16, args=(queue, ))
        pFP16.start()
        pFP16.join()

        self.fp16.setText(queue.get())
        
        queue = mp.Queue()
        
        pFP32 = mp.Process(target=MultiThread.FP32, args=(queue, ))
        pFP32.start()
        pFP32.join()
        

        self.fp32.setText(queue.get())

        queue = mp.Queue()
        
        pFP64 = mp.Process(target=MultiThread.FP64, args=(queue, ))
        pFP64.start()
        pFP64.join()
        
        self.fp64.setText(queue.get())

        self.save.setEnabled(True)






class SingleIntegerUI(vector_form, vector_base):
    got_signal = pyqtSignal(str)
    def __init__(self, parent):
        super(vector_base, self).__init__()
        self.setupUi(self)

        self.parent = parent
        
        DEFAULT_STYLE = """
        QProgressBar{
            border: 1px solid #cccccc;
            border-radius: 5px;
            text-align: center
        }

        QProgressBar::chunk {
            background-color: #00aa7f;
            border-radius: 5px;
            border: 1px #00aa7f;
        }
        """
        self.label.setText("Integer Benchmark")
        self.label_3.setText("INT16: ")
        self.label_2.setText("INT32: ")
        self.label_4.setText("INT64: ")
        
        tINT = Thread(target=self.INT)
        tINT.start()
        
        self.save.clicked.connect(self.btnClicked)
            
        
        self.show()
    def btnClicked(self):
      
        
        self.got_signal.connect(self.parent.setINT32Score)
        self.got_signal.emit(self.fp32.text())
        
        self.close()
    def INT(self):
        queue = mp.Queue()
        
        pINT16 = mp.Process(target=SingleThread.INT16, args=(queue, ))
        pINT16.start()
        pINT16.join()

        self.fp16.setText(queue.get())
        
        queue = mp.Queue()
        
        pINT32 = mp.Process(target=SingleThread.INT32, args=(queue, ))
        pINT32.start()
        pINT32.join()
        

        self.fp32.setText(queue.get())

        queue = mp.Queue()
        
        pINT64 = mp.Process(target=SingleThread.INT64, args=(queue, ))
        pINT64.start()
        pINT64.join()
        
        self.fp64.setText(queue.get())

        self.save.setEnabled(True)






        
if __name__ == '__main__':
    mp.freeze_support()
    app = QApplication(sys.argv)
    app.setStyle("fusion")
    window = OverMark()
    window.show()
    
    sys.exit(app.exec_()) 
 
    
