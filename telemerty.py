from database import ConnectDb
from pymavlink import mavutil
import threading
import time 
from tkinter import messagebox

'''
2 errors:
1. what to do when the drone looses connection mid program 
2. what to do when address already in use s
'''

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
        pass 
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
                self.connection.wait_heartbeat()
                self.last_heartbeat = time.time()
                self.running = True
                thread_listener = threading.Thread(target=self.listener, daemon=True)
                thread_listener.start()
                self.connected = True
                print("Connected")
            except Exception as e:
                print("Connection error:", e)
                self.connected = False
            self.db_tele.disconnectdb()
        elif(self.type_connection == 'radio'):
            pass
        elif(self.type_connection == 'network'):
            pass
        self.db_tele.disconnectdb()
    