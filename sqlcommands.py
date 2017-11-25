import os
import sqlite3

def create_connection(database):
    try:
        conn = sqlite3.connect(database)
        return conn
    except error as e:
        print(e)
        
    return None

def create_table(database):
    
    # Get sql syntax from db sub-directory
    alerts_table_file = open(os.getcwd() + '//db//alerts-table.txt','r')
    alerts_table = alerts_table_file.read().replace('\n','')
    
    # Close out sql syntax file 
    alerts_table_file.close()  
    
    # Create connection and tables
    conn = create_connection(database)
    if conn is not None:
        c = conn.cursor()
        c.execute(alerts_table)
        
def commit_alert(conn,message):
    
    # Craft sql statement with fields for inputs
    sql = 'INSERT INTO alerts VALUES(?,?,?,?,?,?,?,?,?)'
    
    # Execute sql statement using cursor 
    conn.cursor().execute(sql,message)
    
    conn.commit()