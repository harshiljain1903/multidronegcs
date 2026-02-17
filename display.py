'''
Docstring for gcs.map_visualization
Real-time drone marker
Flight path trail
Waypoint display
Geofencing zones
Home location marker
No-fly zones
Multi-drone display (important for you)
'''

import tkinter as tk 
from tkinter import messagebox
from tkintermapview import TkinterMapView
from database import ConnectDb
from telemerty import Drone , Telemetry

class Display():
    def __init__(self):
        self.tk = tk.Tk()
        self.width = self.tk.winfo_screenwidth()
        self.height= self.tk.winfo_screenheight()
        self.satte = 0
        self.db_display= ConnectDb()
        self.map_widget = None
    def change_titles(self):
        if self.satte == 0:
            self.map_widget.set_tile_server("https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}")
            self.satte = 1
        else:
            self.map_widget.set_tile_server( "https://a.tile.openstreetmap.org/{z}/{x}/{y}.png")
            self.satte =0 
    def add_drone_db(self):
        self.db_display.connectdb()
        name = self.name_entry.get()
        ip = self.ip_entry.get()
        port = self.port_entry.get()
        type = self.type 
        firmware = self.firmware_entry.get()
        name_query = 'select * from drone_info where drone_name = %s'
        params_name = (name,)
        name_data = self.db_display.execute_select(name_query, params_name)
        if(len(name_data) != 0):
            messagebox.showinfo(title='Error' , message='Name already exists')
        else:
            insert_query = 'insert into drone_info values(%s , %s , %s , %s ,%s)'
            insert_params = (name,type,firmware,ip,port)
            self.db_display.execute_instruction(insert_query , insert_params)
            print('query executed')
        self.db_display.disconnectdb()
    def sitl_bt(self):
        sitl_box = tk.Toplevel(self.connection_type_level)
        sitl_box.title('sitl options')
        sitl_box.geometry(f'{self.width}x{self.height}')
        frame1 = tk.Frame(sitl_box , height=250)
        frame1.pack(side='top' , fill='x')
        frame2 = tk.Frame(sitl_box , height=250)
        frame2.pack(side='top' , fill='x')
        ip_label = tk.Label(frame1 , text='Enter ip address: ')
        ip_label.pack(side='left' , padx=20)
        self.ip_entry = tk.Entry(frame1)
        self.ip_entry.pack(side='left' , padx=20)
        name = tk.Label(frame1 , text='Enter the name of the drone: ')
        name.pack(side='left' , padx=20)
        self.name_entry = tk.Entry(frame1)
        self.name_entry.pack(side='left')
        port_label = tk.Label(frame2 , text='Enter port number: ')
        port_label.pack(side='left' , padx=20)
        self.port_entry = tk.Entry(frame2)
        self.port_entry.pack(side='left' , padx=30)
        firmware_label = tk.Label(frame2 , text='Enter the firmware: ')
        firmware_label.pack(side='left' , padx=20)
        self.firmware_entry = tk.Entry(frame2)
        self.firmware_entry.pack(side='left' , padx=20)
        self.type = 'sitl'
        submit_btn = tk.Button(frame2 , text='Submit' ,command=self.add_drone_db)
        submit_btn.pack(side='left')
    def add_drone(self):
        self.connection_type_level = tk.Toplevel(self.tk)
        self.connection_type_level.title('connect drone type')
        self.connection_type_level.geometry(f'{self.width}x{self.height}')
        frame_selection = tk.Frame(self.connection_type_level , height=100)
        frame_selection.pack(side='top' , fill='x')
        sitl_btn = tk.Button(frame_selection , text='SITL', command=self.sitl_bt)
        sitl_btn.pack(side='left' , padx='15')
        network_btn = tk.Button(frame_selection , text='Network connection', command=None)
        network_btn.pack(side='left' , padx='15')
        radio_btn = tk.Button(frame_selection , text='Radio', command=None)
        radio_btn.pack(side='left' , padx='15')
    def check_drone(self):
        self.db_display.connectdb()
        name_check = self.check_name_entry.get()
        query_name_check = 'select * from drone_info where drone_name = %s '
        chech_params_name = (name_check,)
        check_data = self.db_display.execute_select(query_name_check , chech_params_name)
        if(len(check_data)==0):
            messagebox.showinfo(title='Error' , message='Drone not found in the database')
        else:
            connection_type_check = check_data[0][1]
            telemetry_connect = Telemetry(name_check , connection_type_check)
            self.db_display.disconnectdb()
            telemetry_connect.connect_drone()
            telemetry_connect.get_telemetry_drone()
    def connect_drone(self):
        self.connect_window = tk.Toplevel(self.tk)
        self.connect_window.title('connect drone')
        self.connect_window.geometry(f'{self.width}x{self.height}')
        frame1 = tk.Frame(self.connect_window , height=250)
        frame1.pack(side='top' , fill='x')
        name_label = tk.Label(frame1 , text='Enter the name of the drone: ')
        name_label.pack(side='left' , padx=20)
        self.check_name_entry = tk.Entry(frame1)
        self.check_name_entry.pack(side='left')
        check_btn = tk.Button(frame1 , text='check drone' ,command=self.check_drone)
        check_btn.pack(side='left' , padx=20)
    def display(self):
        self.tk.title('white cloud gcs version 1.0')
        self.tk.geometry(f'{self.width}x{self.height}')
        frame1 = tk.Frame(self.tk , height=100)
        frame1.pack(side='top' , fill='x')
        #top frame buttonsq
        add_btn = tk.Button(frame1 , text='add drone to database' , command=self.add_drone)
        toggle_map = tk.Button(frame1 , text='toggle map' , command=self.change_titles)
        connect_drone = tk.Button(frame1 , text='connect the drone' , command=self.connect_drone)
        #packing the buttons
        add_btn.pack(side='right' , padx=10)
        toggle_map.pack(side='right' ,padx=10)
        connect_drone.pack(side='right' , padx=10)
        #map display 
        map_frame = tk.Frame(self.tk)
        map_frame.pack(side='top' , fill='both' , expand=True)
        self.map_widget = TkinterMapView(map_frame)
        self.map_widget.set_position(23.0225, 72.5714)
        self.map_widget.set_marker(23.0225, 72.5714, text="Ahmedabad")
        self.map_widget.pack(fill='both' , expand=True)
        self.tk.mainloop()
