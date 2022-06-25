
from subprocess import *
import subprocess as s
import os
import time

import clr

def initialize_openhardwaremonitor():
    try:
    # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    file = os.path.join(base_path, 'OpenHardwareMonitorLib')
    clr.AddReference(file)

    from OpenHardwareMonitor import Hardware

    handle = Hardware.Computer()
    #handle.MainboardEnabled = True
    handle.CPUEnabled = True
    #handle.RAMEnabled = True
    #handle.GPUEnabled = True
    #handle.HDDEnabled = True
    handle.Open()
    return handle

class Processor:
    

    def __init__(self):
        self.openhardwaremonitor_hwtypes = ['Mainboard','SuperIO','CPU','RAM','GpuNvidia','GpuAti','TBalancer','Heatmaster','HDD']
        self.openhardwaremonitor_sensortypes = ['Voltage','Clock','Temperature','Load','Fan','Flow','Control','Level','Factor','Power','Data','SmallData']
        try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
            base_path = sys._MEIPASS
        except Exception:
            base_path = os.path.abspath(".")
        file = 'OpenHardwareMonitorLib'
        clr.AddReference(file)

        from OpenHardwareMonitor import Hardware

        self.handle = Hardware.Computer()
        #handle.MainboardEnabled = True
        self.handle.CPUEnabled = True
        #handle.RAMEnabled = True
        #handle.GPUEnabled = True
        #handle.HDDEnabled = True
        self.handle.Open()
        
    def name(self):
        
        return self.fetch_stats(self.handle, 'NAME')
    def spec(self):
        ps = Popen('wmic cpu get name', stdin = s.PIPE,stdout = s.PIPE, shell=True)
        stdout = str(ps.communicate()[0]).replace('b', '').replace("'", '').replace("\\r\\n", "")

        return stdout.replace('  ', '').replace('Name', '').replace('\\r', '')
    def base():
        return 'error'
    def current(self):
       
        
        return self.fetch_stats(self.handle, 'CLOCK')
    def cores(self):
        return self.fetch_stats(self.handle, 'CORES')
    def threads(self):
        return os.cpu_count()
    def temp(self):
        
        
        return self.fetch_stats(self.handle, 'TEMP')
    def power(self):
        
        
        return self.fetch_stats(self.handle, 'POWER')
    def RenderScore(self):
        score = open("CPU/Benchmark/Single Thread/Score.txt", "r").read()
        return score
   

    def Sensor(self):
        
        while True:

            self.fetch_stats(self.handle, False)
            time.sleep(0.5)
            

    def fetch_stats(self, handle, sensorName):
        
        if sensorName == 'NAME':
            for i in handle.Hardware:
                i.Update()
                for sensor in i.Sensors:
                    if self.parse_sensor(sensor, 'NAME') == None:
                        None
                    else:
                        nameVar = self.parse_sensor(sensor, 'NAME')
                for j in i.SubHardware:
                    j.Update()
                    for subsensor in j.Sensors:
                        self.parse_sensor(subsensor, 'NAME')
                return nameVar
        if sensorName == 'CLOCK':
            mylist = ''
            for i in handle.Hardware:
                i.Update()
                for sensor in i.Sensors:
                    if self.parse_sensor(sensor, 'CLOCK') == None:
                        None
                    else:
                        
                        mylist += self.parse_sensor(sensor, 'CLOCK')
                        
                    
                for j in i.SubHardware:
                    j.Update()
                    for subsensor in j.Sensors:
                        self.parse_sensor(subsensor, True)
                        
                return mylist
        if sensorName == 'TEMP':
            mylist = ''
            for i in handle.Hardware:
                i.Update()
                for sensor in i.Sensors:
                    if self.parse_sensor(sensor, 'TEMP') == None:
                        None
                    else:
                        
                        mylist += self.parse_sensor(sensor, 'TEMP')
                        
                    
                for j in i.SubHardware:
                    j.Update()
                    for subsensor in j.Sensors:
                        self.parse_sensor(subsensor, True)
                        
                return mylist
        if sensorName == 'POWER':
            mylist = ''
            for i in handle.Hardware:
                i.Update()
                for sensor in i.Sensors:
                    if self.parse_sensor(sensor, 'POWER') == None:
                        None
                    else:
                        
                        mylist += self.parse_sensor(sensor, 'POWER')
                        
                    
                for j in i.SubHardware:
                    j.Update()
                    for subsensor in j.Sensors:
                        self.parse_sensor(subsensor, True)
                        
                return mylist
        if sensorName == 'CORES':
            mylist = []
            for i in handle.Hardware:
                i.Update()
                for sensor in i.Sensors:
                    if self.parse_sensor(sensor, 'CORES') == None:
                        None
                    else:
                        
                        mylist.append(self.parse_sensor(sensor, 'CORES'))
                        
                    
                for j in i.SubHardware:
                    j.Update()
                    for subsensor in j.Sensors:
                        self.parse_sensor(subsensor, True)
                        
                return len(mylist)
    def parse_sensor(self, sensor, name):
            
            if name == 'NAME':

                return f'{sensor.Hardware.Name}'            
                
            if type(sensor).__module__ == 'OpenHardwareMonitor.Hardware':
                sensortypes = self.openhardwaremonitor_sensortypes
                hardwaretypes = self.openhardwaremonitor_hwtypes


            
            
            if sensor.SensorType == sensortypes.index('Temperature'):
                if hardwaretypes[sensor.Hardware.HardwareType] == "CPU":
                    if sensor.Name == "CPU Package":
                        listTemperature = u"%s\u00B0C" % (sensor.Value)
                    
                        if name == 'TEMP':
                            return f'{listTemperature}'  
            if sensor.SensorType == sensortypes.index('Power'):
                if hardwaretypes[sensor.Hardware.HardwareType] == "CPU":
                    if sensor.Name == "CPU Package":
                        listPower = "%f" % (sensor.Value)
                    
                        if name == 'POWER':
                            return f'{sensor.Name}: {listPower},'


 
            if sensor.SensorType == sensortypes.index('Clock'):
                if hardwaretypes[sensor.Hardware.HardwareType] == "CPU":
                    if "CPU Core" in sensor.Name:
                        listPower = "%f" % (sensor.Value)


                        if name == 'CLOCK':
                            return f'{sensor.Name}: {listPower},'
                        if name == 'CORES':
                            return f'{sensor.Name}'


            

