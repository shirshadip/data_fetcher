import mysql.connector as m
def est(p,table_name):
    con= m.connect(
        host="localhost",
        user="root",
        passwd=p,


    )
    cur = con.cursor()

    sql = "CREATE DATABASE IF NOT EXISTS data_fetcher;"
    # Select the database
    cur.execute(f"USE data_fetcher;")

    # Create table if not exists
    cur.execute(f"""
           CREATE TABLE IF NOT EXISTS {table_name}(
               id INT AUTO_INCREMENT PRIMARY KEY,
               name VARCHAR(255)
           );
       """)
    cur.execute(sql)
    con.commit()
    con.close()
