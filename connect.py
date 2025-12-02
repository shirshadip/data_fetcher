import mysql.connector as m

def est(p, table_name):
    con = m.connect(
        host="localhost",
        user="root",
        passwd=p,
        database="data_fetcher"
    )
    cur = con.cursor()

    # Create table safely
    sql = f"""
    CREATE TABLE IF NOT EXISTS {table_name} (
        id INT AUTO_INCREMENT PRIMARY KEY
    );
    """

    cur.execute(sql)
    con.commit()
    con.close()


def inser(p, t_name, col_name, val):
    con = m.connect(
        host="localhost",
        user="root",
        passwd=p,
        database="data_fetcher"
    )
    cur = con.cursor()
    sql = f"ALTER TABLE {t_name} ADD COLUMN IF NOT EXISTS {col_name} VARCHAR(255);"
    cur.execute(sql)
    sql = f"INSERT INTO {t_name} ({col_name}) VALUES (%s);"
    cur.execute(sql, (val,))
    con.commit()
    con.close()
