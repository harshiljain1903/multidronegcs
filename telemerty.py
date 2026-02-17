from database import ConnectDb
from pymavlink import mavutil
import threading
import time 
from tkinter import messagebox



class Drone:
    def __init__(self , name , type):
        self.name = name
        self.type_connection = type
class Telemetry(Drone):
    def __init__(self, name, type):
        super().__init__(name, type)
        self.db_tele = ConnectDb()
        self.connection = None 
        self.connected = False
        self.running = False
    #creating thread for listening
    def listener(self):
        while self.running:
            msg = self.connection.wait_heartbeat(timeout=5)
            if msg:
                print(msg)
                print('message recieved from ',self.name)
            else:
                print('connection lost from the drone')
                self.connected = False
                self.running = False
                self.connection.close()
            time.sleep(5)
    def connect_drone(self):
        self.db_tele.connectdb()
        query_name = 'select * from drone_info where drone_name = %s'
        params = (self.name,)
        data = self.db_tele.execute_select(query_name , params)
        if(self.type_connection == 'sitl'):
            self.ip = data[0][3].strip()
            self.port = data[0][4].strip()
            try:
                self.connection = mavutil.mavlink_connection(f"udp:{self.ip}:{self.port}")
                msg = self.connection.wait_heartbeat(timeout=10)
                if msg:
                    self.connected = True
                    self.running = True
                    thread = threading.Thread(target=self.listener , daemon=True)
                    thread.start()
                    messagebox.showinfo(message='drone connected' , title='success')
                else:
                    messagebox.showinfo(title='Error' , message=f'{self.name} has lost connection')
            except Exception as e:
                self.connected = False
                print('error occured ' , e)
            self.db_tele.disconnectdb()
        elif(self.type_connection == 'radio'):
            pass
        elif(self.type_connection == 'network'):
            pass
        self.db_tele.disconnectdb()
    