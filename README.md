# Population and unemployment metrics in sqlite 

Load online census data files into sqlite staging tables. Then transform the data into the required format of a metric with several dimensions.

Final sqlite database with data in the required format is [database.sqlite3](https://github.com/samshetty/population-metrics/blob/master/database.sqlite3).

Database Table for Analyst requirement #1: __metropolitan_areas_population_by_year__

Database Table for Analyst requirement #2: __counties_population_unemployment_rate_by_year__


## Getting Started

### Steps to execute

1. Download repo to a local folder

2. Install Prerequisites

   ```
   pip install -r requirements.txt
   ```
   
3. Run [create_staging_tables.py](https://github.com/samshetty/population-metrics/blob/master/create_staging_tables.py)

   ```
   python sqlite_load_as_is.py
   ```

   This python program loads the below census data files into staging tables in a sqlite database. The database gets saved in the same folder as the python program.
   
   https://www2.census.gov/programs-surveys/popest/datasets/2010-2018/metro/totals/cbsa-est2018-alldata.csv
   https://www.ers.usda.gov/webdocs/DataFiles/48747/Unemployment.xls?v=9115.7

4. Open the sqlite database from the above step in a client like [DB Browser SQLite](https://sqlitebrowser.org/dl/). Run the below queries to convert the raw data into the Analyst required format of a metric with several dimensions.
    1. **Analyst requirement #1:**

         _You are working with an analyst that would like to be able to graph the population of any major metropolitan area in the US over time._
      
         **Query:**

         _Converts population columns for each year into a metric and puts it into a new table ___metropolitan_areas_population_by_year___ for easy querying._
       
         ```sql
            DROP TABLE IF EXISTS metropolitan_areas_population_by_year;

            CREATE TABLE metropolitan_areas_population_by_year AS
            WITH population_data_cte AS
            (
                SELECT   [index] AS AREA_ID, NAME AS [METROPOLITAN_AREA], POPESTIMATE2010, POPESTIMATE2011, 
                        POPESTIMATE2012, POPESTIMATE2013, POPESTIMATE2014, POPESTIMATE2015, 
                        POPESTIMATE2016, POPESTIMATE2017, POPESTIMATE2018
                FROM     population_estimates
                WHERE    LSAD = 'Metropolitan Statistical Area'
            ) 
            SELECT   AREA_ID, METROPOLITAN_AREA, 2010 AS YEAR, POPESTIMATE2010 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2011 AS YEAR, POPESTIMATE2011 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2012 AS YEAR, POPESTIMATE2012 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2013 AS YEAR, POPESTIMATE2013 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2014 AS YEAR, POPESTIMATE2014 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2015 AS YEAR, POPESTIMATE2015 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2016 AS YEAR, POPESTIMATE2016 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2017 AS YEAR, POPESTIMATE2017 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   AREA_ID, METROPOLITAN_AREA, 2018 AS YEAR, POPESTIMATE2018 AS POPULATION
            FROM     population_data_cte;

            SELECT 	* 
            FROM 		metropolitan_areas_population_by_year 
            ORDER BY METROPOLITAN_AREA, YEAR

         ```
    
    2. **For Analyst requirement #2:** 
    
         _A different analyst wants to know about population and unemployment rates of the US at the county level._

         **Query:**

         _Pivots the population and unemployment rate numbers from the 2 staging tables and creates respective temp tables. Joins the temp tables on the county and year columns. Then inserts it into a new table ___counties_population_unemployment_rate_by_year___ for querying._

         ```sql
            DROP TABLE IF EXISTS temp_county_population_by_year;
            CREATE TEMPORARY TABLE temp_county_population_by_year AS
            WITH population_data_cte AS
            (
                SELECT   [index], NAME, POPESTIMATE2010, POPESTIMATE2011, 
                            POPESTIMATE2012, POPESTIMATE2013, POPESTIMATE2014, POPESTIMATE2015, 
                            POPESTIMATE2016, POPESTIMATE2017, POPESTIMATE2018
                FROM     population_estimates
                WHERE    LSAD = 'County or equivalent'
            )
            --COUNTY POPULATION DATA
            SELECT   [index], NAME, 2010 AS YEAR, POPESTIMATE2010 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2011 AS YEAR, POPESTIMATE2011 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2012 AS YEAR, POPESTIMATE2012 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2013 AS YEAR, POPESTIMATE2013 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2014 AS YEAR, POPESTIMATE2014 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2015 AS YEAR, POPESTIMATE2015 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2016 AS YEAR, POPESTIMATE2016 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2017 AS YEAR, POPESTIMATE2017 AS POPULATION
            FROM     population_data_cte
            UNION ALL
            SELECT   [index], NAME, 2018 AS YEAR, POPESTIMATE2018 AS POPULATION
            FROM     population_data_cte;

            --COUNTY UNEMPLOYMENT RATE DATA
            DROP TABLE IF EXISTS temp_county_unemployment_rate_by_year;

            CREATE TEMPORARY TABLE temp_county_unemployment_rate_by_year AS
            WITH counties_unemployment_cte AS
            (
                SELECT   FIPS, Area_name, Unemployment_rate_2010, Unemployment_rate_2011, 
                            Unemployment_rate_2012, Unemployment_rate_2013, Unemployment_rate_2014, Unemployment_rate_2015, 
                            Unemployment_rate_2016, Unemployment_rate_2017, Unemployment_rate_2018
                FROM     counties_unemployment
                WHERE    FIPS <> 0
            )
            SELECT   FIPS, Area_name, 2010 AS YEAR, Unemployment_rate_2010 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2011 AS YEAR, Unemployment_rate_2011 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2012 AS YEAR, Unemployment_rate_2012 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2013 AS YEAR, Unemployment_rate_2013 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2014 AS YEAR, Unemployment_rate_2014 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2015 AS YEAR, Unemployment_rate_2015 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2016 AS YEAR, Unemployment_rate_2016 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2017 AS YEAR, Unemployment_rate_2017 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte
            UNION ALL
            SELECT   FIPS, Area_name, 2018 AS YEAR, Unemployment_rate_2018 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment_cte;

            DROP TABLE IF EXISTS counties_population_unemployment_rate_by_year;

            --JOIN THE POPULATION AND UNEMPLOYMENT RATE NUMBERS ON COUNTY AND YEAR AND INSERT INTO FINAL TABLE
            CREATE TABLE counties_population_unemployment_rate_by_year AS
            SELECT     P.[index] AS COUNTY_ID, P.NAME, P.YEAR, P.POPULATION, U.UNEMPLOYMENT_RATE
            FROM     temp_county_population_by_year P INNER JOIN
                    temp_county_unemployment_rate_by_year U ON P.NAME = U.Area_name AND P.YEAR = U.YEAR
            ORDER BY P.NAME, P.YEAR;

            SELECT   *
            FROM     counties_population_unemployment_rate_by_year
            ORDER BY NAME, YEAR

         ```

## Conclusion

After running the above steps, the below tables in the sqlite database have the data in the required format for Analysts to use. Final sqlite database with data in the required format is [database.sqlite3](https://github.com/samshetty/population-metrics/blob/master/database.sqlite3).

Database Table for Analyst requirement #1: __metropolitan_areas_population_by_year__

Database Table for Analyst requirement #2: __counties_population_unemployment_rate_by_year__

## Author

* **Sam Shetty** 
