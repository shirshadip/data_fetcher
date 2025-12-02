import mysql.connector as m 
def database (p,t):
    con=m.connect(
        host="localhost",
        username="root",
        passwd=p
        database="data_fetcher"
    )
    cur=con.cursor()
    sql=f""
    cur.execute(sql)
    con.commit()
    con.close()