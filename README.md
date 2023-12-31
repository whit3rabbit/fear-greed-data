# Description

The CNN's Fear and Greed website doesn't offer a historical dataset and the datasets that do exist have different values.

I tried to collect the most accurate data I could find combining three different sources into one file.  I have included where i found the data and the csv/json.

# Datasets

I have pulled multiple datasets and json files from different websites that had historical Fear and Greed data.  I've included them in the datasets and json folder.

## Openstockalert.com

* Data is from 2015-2022
* https://openstockalert.com/FearGreedChart.php
* Note: https://openstockalert.com/GetFnGMktIndex.php - Pulled json from here in response
* File: openstockalert_fear_greed_data.csv

## Hackingthemarkets

* Data is from 2011-2020
* https://raw.githubusercontent.com/hackingthemarkets/sentiment-fear-and-greed/master/datasets/fear-greed.csv
* File: hackingthemarkets_fear_greed_data.csv

## alexey-formalmethods

* Data is from 2011-2022 and is expanded from hackingthemarkets
* https://raw.githubusercontent.com/alexey-formalmethods/datasets/main/money.cnn%20fear-and-greed/data.csv
* File: alexey-formalmethods_fear_greed_data.csv

## macromicro.me

* Data is from 2021-current
* https://en.macromicro.me/collections/34/us-stock-relative/50108/cnn-fear-and-greed
* Note: https://en.macromicro.me/charts/data/50108 - the data saved as macromicro.json from the response
* File: macromicro_fear_greed_data.csv
* See json folder

## cnn.com

* Data from 2021-02-01 is accurate, however before that date data is not accurate.
* See https://izy.codes/backtest-strategy-fear-and-greed-index-en/
* See https://github.com/gman4774/fear_and_greed_index github issues
* Data scraped from https://production.dataviz.cnn.io/index/fearandgreed/graphdata/2021-03-01
* See json folder

# archive.org scrape

* Scraped available data from 2012-2022 from waybackmachine
* Not everyday is covered
* File: archive_org_fear_greed_data.csv


# Correlation with archive.org data

Higher the coefficent the more correlated with archive.org data:

hackingthemarkets_fear_greed_data: Correlation coefficient of 0.4111
openstockalert_fear_greed_data: Correlation coefficient of 0.4078
alexey-formalmethods_fear_greed_data: Correlation coefficient of 0.4029
macromicro_fear_greed_data: Correlation coefficient of 0.3437

# Combining all the Data

I've combined the early data from Hackingthemarket (2011-2016) with openstockalert data (2016-2022) then combined with latest data from CNN (2022-2023).

* File: fear-greed-2011-2023.csv
