import mysql.connector

class ConnectDb:
    def __init__(self):
        self.conn = None 
        self.cursor = None 
    @staticmethod
    def logs(text):
        file = open('log.txt' , 'a')
        file.write(f"{text} \n")
        file.close()
    def connectdb(self):
        try:
            self.conn = mysql.connector.connect(database='drone' , user='root' , passwd='harshiljain')
            self.cursor = self.conn.cursor()
        except Exception as e:
            ConnectDb.logs(e)
    def disconnectdb(self):
        try:
            self.conn.close()
        except Exception as disconnect_error:
            ConnectDb.logs(disconnect_error)
    def execute_select(self, query , params=None):
        try:
            self.cursor.execute(query , params)
            return self.cursor.fetchall()
        except Exception as selection_query:
            ConnectDb.logs(selection_query)
    def execute_instruction(self , query , params=None):
        try:
            self.cursor.execute(query, params)
            self.conn.commit()
        except Exception as execute_ins_query:
            print("SQL ERROR:", execute_ins_query)
            ConnectDb.logs(execute_ins_query)