import os
import pandas as pd
import sqlite3
import xlrd

def create_database_connection(db_file_path):
    conn = sqlite3.connect(db_file_path)
    return conn

def load_data_into_tables(conn, file_urls):
    for file_url in file_urls:
        if file_url[1] == "csv":
            df = pd.read_csv(file_url[2], encoding="ISO-8859-1")
        else:
            df = pd.read_excel(file_url[2], "Unemployment Med HH Inc", skiprows=7, encoding="ISO-8859-1", index_col=0)
        cursor = conn.cursor()
        sql_drop_table_if_exists = 'DROP TABLE IF EXISTS ' + file_url[0]
        cursor.execute(sql_drop_table_if_exists)
        df.to_sql(name=file_url[0], con=conn)

def main():
    try:
        db_file_path = os.path.join(os.path.dirname('__file__'), 'database.sqlite3')
        file_urls = []
        file_urls.append(["population_estimates", "csv", "https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/metro/totals/cbsa-est2018-alldata.csv"])
        #file_urls.append(["counties_population", "csv", "https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/counties/totals/co-est2018-alldata.csv"])
        file_urls.append(["counties_unemployment", "xls", "https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls?v=9115.7"])

        conn = create_database_connection(db_file_path)
        with conn:
            load_data_into_tables(conn, file_urls)
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    main()