# Population and Unemployment metrics in Sqlite 

Download online census data files, create sqlite staging tables and transform the data into fact table with metrics 

## Getting Started

These steps will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Install requirements

```
pip install -r requirements.txt
```

### Steps to execute

Run sqlite_load_as_is.py (attached)
This python program downloads the online census data files, connects to sqlite, creates staging tables and loads the raw data

Next, run the below queries for the 2 Analyst requirements to get data in the required format (metric with dimensions) 
Task #1 - You are working with an analyst that would like to be able to graph the population of any major metropolitan area in the US over time. 
```
--Pivots the population column into a metric from the staging data, and puts it into a fact table for easy querying
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
Task #2 - A different analyst wants to know about population and unemployment rates of the US at the county level.
```
--Pivot the population and unemployment from 2 different sources into respective temp tables and join the 2 tables on the county column and year. Then insert it into a new fact table for querying
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

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Author

* **Sam Shetty** - *Initial work* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

