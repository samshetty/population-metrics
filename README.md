# Population and unemployment metrics in sqlite 

Download online census data files, create sqlite staging tables and transform the data into fact table with metrics 

## Getting Started

### Prerequisites

Install requirements

```
pip install -r requirements.txt
```

### Steps to execute

1. Run [sqlite_load_as_is.py](https://github.com/samshetty/sqlite/blob/master/sqlite_load_as_is.py)

   This python program downloads the online census data files, connects to sqlite, creates staging tables and loads the raw data into them.

2. Run the below queries to get data in the required final format (metric with dimensions) 
    1. **Analyst requirement #1:**

         _You are working with an analyst that would like to be able to graph the population of any major metropolitan area in the US over time._
      
         **Query:**

         Pivots the population data into a metric and puts it into a fact table ___metropolitan_areas_population_by_year___ for easy querying.
       
         ```sql
           CREATE TABLE IF NOT EXISTS metropolitan_areas_population_by_year AS
           SELECT   [index], NAME, 2010 AS YEAR, POPESTIMATE2010 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2011 AS YEAR, POPESTIMATE2011 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2012 AS YEAR, POPESTIMATE2012 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2013 AS YEAR, POPESTIMATE2013 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2014 AS YEAR, POPESTIMATE2014 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2015 AS YEAR, POPESTIMATE2015 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2016 AS YEAR, POPESTIMATE2016 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2017 AS YEAR, POPESTIMATE2017 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'
           UNION ALL
           SELECT   [index], NAME, 2018 AS YEAR, POPESTIMATE2018 AS POPULATION
           FROM     population_estimates
           WHERE    LSAD = 'Metropolitan Statistical Area'

         ```
    
    2. **For Analyst requirement #2:** 
    
             _A different analyst wants to know about population and unemployment rates of the US at the county level._

         **Query:  **

             Pivots the population and unemployment from 2 different sources into respective temp tables and joins the temp tables on the county and year columns. Then inserts it into a new fact table ___counties_population_unemployment_rate_by_year___ for querying.

            ```

            DROP TABLE IF EXISTS temp_county_population_by_year;

            CREATE TEMPORARY TABLE IF NOT EXISTS temp_county_population_by_year AS
            SELECT   [index], NAME, 2010 AS YEAR, POPESTIMATE2010 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2011 AS YEAR, POPESTIMATE2011 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2012 AS YEAR, POPESTIMATE2012 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2013 AS YEAR, POPESTIMATE2013 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2014 AS YEAR, POPESTIMATE2014 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2015 AS YEAR, POPESTIMATE2015 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2016 AS YEAR, POPESTIMATE2016 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2017 AS YEAR, POPESTIMATE2017 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent'
            UNION ALL
            SELECT   [index], NAME, 2018 AS YEAR, POPESTIMATE2018 AS POPULATION
            FROM     population_estimates
            WHERE    LSAD = 'County or equivalent';

            DROP TABLE IF EXISTS temp_county_unemployment_rate_by_year;
            CREATE TEMPORARY TABLE IF NOT EXISTS temp_county_unemployment_rate_by_year AS
            SELECT   FIPS, Area_name, 2010 AS YEAR, Unemployment_rate_2010 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2011 AS YEAR, Unemployment_rate_2011 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2012 AS YEAR, Unemployment_rate_2012 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2013 AS YEAR, Unemployment_rate_2013 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2014 AS YEAR, Unemployment_rate_2014 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2015 AS YEAR, Unemployment_rate_2015 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2016 AS YEAR, Unemployment_rate_2016 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2017 AS YEAR, Unemployment_rate_2017 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0
            UNION ALL
            SELECT   FIPS, Area_name, 2018 AS YEAR, Unemployment_rate_2018 AS UNEMPLOYMENT_RATE
            FROM     counties_unemployment
            WHERE    FIPS <> 0;

            CREATE TABLE IF NOT EXISTS counties_population_unemployment_rate_by_year AS
            SELECT     P.[index] AS COUNTY_ID, P.NAME, P.YEAR, P.POPULATION, U.UNEMPLOYMENT_RATE
            FROM     temp_county_population_by_year P INNER JOIN
                    temp_county_unemployment_rate_by_year U ON P.NAME = U.Area_name AND P.YEAR = U.YEAR
            ORDER BY P.NAME, P.YEAR

            SELECT     ROWID, *
            FROM     counties_population_unemployment_rate_by_year
            ORDER BY NAME, YEAR
            ```

## Author

* **Sam Shetty** 
