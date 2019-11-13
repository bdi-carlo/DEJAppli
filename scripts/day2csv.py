import sys
import sqlite3
import csv
from sqlite3 import Error
from datetime import date
from datetime import datetime
from datetime import timedelta

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_all_tasks(conn, csvdate):
    cur = conn.cursor()
    cur.execute("SELECT * FROM calculdej_dossier WHERE date BETWEEN ? AND ?", (csvdate-timedelta(days=1), csvdate+timedelta(days=1)))

    rows = cur.fetchall()

    for row in rows:
        print(row)

    return rows

def main():
    database = r"D:\Projets\DEJAppli\app\db.sqlite3"
    csvfolder = "D:\\Projets\\DEJAppli\\app\\csv\\"

    # Create connection with db
    conn = create_connection(database)
    # Get the J-1 or the date in argument
    if len(sys.argv) == 2:
        csvdate = datetime.strptime(str(sys.argv[1]), "%Y-%m-%d")
        print(csvdate)
    else:
        csvdate = date.today() - timedelta(days=1)

    with conn:
        # Get datas from J-1
        rows = select_all_tasks(conn, csvdate)

        # Write in the csv file the datas for J-1
        with open(csvfolder + csvdate.strftime("%Y%m%d") + "_" + "dossiers.csv", 'a') as csvfile:
            writer = csv.writer(csvfile)
            if rows:
                for row in rows:
                    writer.writerow(row)

if __name__ == '__main__':
    main()
