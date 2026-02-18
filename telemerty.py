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
    def close_port(self):
        self.running = False
        self.connected = False
        if self.connection:
            self.connection.close()
        self.connection = None
    def disconn_drone(self , name):
        self.close_port()
        self.db_tele.connectdb()
        try:
            data = self.db_tele.execute_select('select * from active_drones where drone_name = %s',(name,))
            if(len(data) !=0):
                self.db_tele.execute_instruction('delete from active_drones where drone_name = %s',(name,))
                messagebox.showinfo(title='success' , message='drone disconnected ')
            else:
                messagebox.showerror(title='failure' , message='drone is not active')
        except Exception as e:
            messagebox.showinfo(title='fatal error' , message=e)
        self.db_tele.disconnectdb()
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
                    query_insert_active_drone = 'insert into active_drones values(%s , %s)'
                    params_insert_active_drone = (self.name , data[0][1] ,)
                    active_drone_check = self.db_tele.execute_select('select * from active_drones where drone_name = %s' , (self.name,))
                    if(len(active_drone_check) !=0):
                        messagebox.showinfo(title='Error' , message='drone already active')
                    else:
                        self.db_tele.execute_instruction(query_insert_active_drone,params_insert_active_drone)
                        messagebox.showinfo(message='drone connected' , title='success')
                else:
                    messagebox.showinfo(title='Error' , message=f'{self.name} has lost connection')
                    self.close_port()
            except Exception as e:
                self.connected = False
                print('error occured ' , e)
            self.db_tele.disconnectdb()
        elif(self.type_connection == 'radio'):
            pass
        elif(self.type_connection == 'network'):
            pass
        self.db_tele.disconnectdb()
    