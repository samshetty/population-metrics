import os
import pandas as pd
import sqlite3
import xlrd

def load_file(file_type, file_url):
    """
    Loads online census data file into a dataframe

    file_type: csv or xls
    file_url: urls of file to load
    RETURNS: Dataframe with file data
    """
    if file_type == "csv":
        df = pd.read_csv(file_url, encoding="ISO-8859-1")
    else:
        df = pd.read_excel(file_url, "Unemployment Med HH Inc", skiprows=7, encoding="ISO-8859-1", index_col=0)
    return df

def create_database_connection(database_file_path):
    """
    Creates aconnection to sqlite database

    database_file_path (string): local path to store the sqlite database
    RETURNS: connection to sqlite database
    """
    conn = sqlite3.connect(database_file_path)
    return conn

def create_staging_table(database_connection, table_name, data):
    """
    Creates staging table in database with input data. Drops table if it exists already

    database_connection: connection to sqlite database
    table_name: name of staging table to create
    data: data to load in the staging
    """
    cursor = database_connection.cursor()
    sql_drop_table_if_exists = 'DROP TABLE IF EXISTS ' + table_name
    cursor.execute(sql_drop_table_if_exists)
    data.to_sql(name=table_name, con=database_connection)

def main():
    try:
        database_file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'database.sqlite3')
        
        file_urls = []
        file_urls.append(["population_estimates", "csv", "https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/metro/totals/cbsa-est2018-alldata.csv"])
        file_urls.append(["counties_unemployment", "xls", "https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls?v=9115.7"])

        database_connection = create_database_connection(database_file_path)

        with database_connection:
            for file_url in file_urls:
                df = load_file(file_url[1], file_url[2])
                create_staging_table(database_connection, file_url[0], df)

        print("Staging files loaded succesfully into {0}.".format(database_file_path))
    except Exception as e:
        print("Error: ", e)

if __name__ == '__main__':
    main()
