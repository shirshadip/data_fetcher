import mysql.connector as m 
def database (p,d):
    con=m.connect(
        host="localhost",
        username="root",
        passwd=p
    )
    cur=con.cursor()
    sql= f"CREATE DATABASE IF NOT EXISTS {d}"
    cur.execute(sql)
    con.commit()
    con.close()