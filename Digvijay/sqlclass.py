import mysql.connector

class sqlconnect():

    def GetallData(self):
      conn = mysql.connector.connect(host="localhost",user="root",password="tnt123",database="python")
      if(conn.is_connected):  
        try:          
           cursor = conn.cursor() 
           print("Connected to MySQL!")
        except mysql.connector.Error as e:
           print(f"Error connecting to MySQL: {e}")
        cursor.execute("SELECT * FROM srnovalidation")
        records = cursor.fetchall()
        for row in records:
           print(row)
        cursor.close()
        conn.close()
      else:
         print("database not connected....") 

    def check_sr_no_existence(self,conn, sr_no):
      cursor = conn.cursor()
      try:
           cursor.execute("SELECT COUNT(*), statusid FROM srnovalidation WHERE sr_no = %s", (sr_no,))
           row = cursor.fetchone()
           cursor.close()
           if row:
             if row[0] > 0:
                return True, row[1]        
             else:
                return False, None
           else:
             return False, None  # SR No does not exist
      except mysql.connector.Error as err:
         print("Error checking SR No existence:", err)
         return False, None      


    def InsertSrNo(self,srno):
      try:
         srno=str(srno)
         conn = mysql.connector.connect(host="localhost",user="root",password="tnt123",database="python")
         if(conn.is_connected):
             exists, status = self.check_sr_no_existence(conn, srno)
             if exists:                
                #print("SR No already exists in the table!  => status = >"+str(status))
                return status
             else:  
                insert_query = "INSERT INTO srnovalidation (sr_no) VALUES (%s)"
                cursor = conn.cursor()          
                cursor.execute(insert_query, (srno,))
                conn.commit()
                #print("SR No inserted successfully!") 
                return 0       
         else:
            print("database not connected....")
      except mysql.connector.Error as e:
         print(f"Error connecting to MySQL: {e}")
      finally:
       # Close cursor and connection
       if 'cursor' in locals():
           cursor.close()
       if 'conn' in locals():
           conn.close()  