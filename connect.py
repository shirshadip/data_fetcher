import mysql.connector as m
def est(p,d,t):
    con= m.connect(
        host="localhost",
        user="root",
        passwd=p,
        database=d
    )
    cur = con.cursor()
    sql=f"select * from {t}"
    cur.execute(sql)
    rows = cur.fetchall()
    for row in rows:
        print(row)
    con.commit()
    con.close()
