# Description

The CNN's Fear and Greed website doesn't offer a historical dataset and the datasets that do exist have different values.

I tried to collect the most accurate data I could find combining three different sources into one file.  I have included where i found the data and the csv/json.

# Canonical dataset

The up-to-date combined file is **[`fear-greed.csv`](fear-greed.csv)** at the repo root.

| Column     | Notes                                                 |
|------------|-------------------------------------------------------|
| Date       | ISO `YYYY-MM-DD`                                      |
| Fear Greed | Float score 0-100 (CNN era) / integer (pre-2021 era)  |
| Rating     | CNN label (`extreme fear`, `fear`, `neutral`, `greed`, `extreme greed`). CNN supplies this directly for 2021-02-01+; for older rows it is computed from the score using CNN's own band cutoffs. |

Coverage:
- 2011-01-03 through 2021-01-29 is frozen, sourced from [`datasets/archive/fear-greed-pre-2021.csv`](datasets/archive/fear-greed-pre-2021.csv) (derived from the hackingthemarkets + openstockalert combined file; see history sections below).
- 2021-02-01 onward is regenerated from the live CNN endpoint on every run.

The previous file `fear-greed-2011-2023.csv` (M/D/YYYY dates, integer scores) has been replaced by `fear-greed.csv`.

# Automation

A GitHub Actions workflow ([`.github/workflows/update-data.yml`](.github/workflows/update-data.yml)) rebuilds [`fear-greed.csv`](fear-greed.csv) every Friday at 23:00 UTC (after US market close) and also supports manual runs via **workflow_dispatch**. It commits the diff directly to `main` as `github-actions[bot]`.

Scripts:
- [`scripts/fetch_cnn.py`](scripts/fetch_cnn.py) - fetches CNN endpoint, writes [`datasets/cnn_fear_greed.csv`](datasets/cnn_fear_greed.csv) and [`json/cnn_output.json`](json/cnn_output.json).
- [`scripts/build_combined.py`](scripts/build_combined.py) - merges the frozen archive with the CNN tail into [`fear-greed.csv`](fear-greed.csv).
- [`scripts/convert_macromicro.py`](scripts/convert_macromicro.py) - one-shot helper (not in CI) that regenerates [`datasets/macromicro_fear_greed_data.csv`](datasets/macromicro_fear_greed_data.csv) from a manually captured [`json/macromicro.json`](json/macromicro.json).

To run locally:

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
.venv/bin/python scripts/fetch_cnn.py        # -> datasets/cnn_fear_greed.csv + json/cnn_output.json
.venv/bin/python scripts/build_combined.py   # -> fear-greed.csv
```

Dependencies are pinned in [`requirements.txt`](requirements.txt). `build_combined.py` aborts rather than writing if the combined output would be shorter than the archive, contains duplicate dates, or is more than 7 days stale.

The third-party comparison datasets under `datasets/` (openstockalert, hackingthemarkets, alexey-formalmethods, macromicro, archive.org) are historical snapshots and are **not** refreshed by the workflow.

# Datasets

I have pulled multiple datasets and json files from different websites that had historical Fear and Greed data.  I've included them in the datasets and json folder.

## Openstockalert.com

* Data is from 2015-2022
* https://openstockalert.com/FearGreedChart.php
* Note: https://openstockalert.com/GetFnGMktIndex.php - Pulled json from here in response
* File: [`datasets/openstockalert_fear_greed_data.csv`](datasets/openstockalert_fear_greed_data.csv) (also [`datasets/openstockalert_cnn_fear_greed_data.csv`](datasets/openstockalert_cnn_fear_greed_data.csv))

## Hackingthemarkets

* Data is from 2011-2020
* https://raw.githubusercontent.com/hackingthemarkets/sentiment-fear-and-greed/master/datasets/fear-greed.csv
* File: [`datasets/hackingthemarkets_fear_greed_data.csv`](datasets/hackingthemarkets_fear_greed_data.csv)

## alexey-formalmethods

* Data is from 2011-2022 and is expanded from hackingthemarkets
* https://raw.githubusercontent.com/alexey-formalmethods/datasets/main/money.cnn%20fear-and-greed/data.csv
* File: [`datasets/alexey-formalmethods_fear_greed_data.csv`](datasets/alexey-formalmethods_fear_greed_data.csv)

## macromicro.me

* Data is from 2021-current
* https://en.macromicro.me/collections/34/us-stock-relative/50108/cnn-fear-and-greed
* Note: In order to see the data you need an account (free) and in network tab of inspector you have to view: https://en.macromicro.me/charts/data/50108  The json data saved as macromicro.json from the response
* File: [`datasets/macromicro_fear_greed_data.csv`](datasets/macromicro_fear_greed_data.csv) (regenerated via [`scripts/convert_macromicro.py`](scripts/convert_macromicro.py) from [`json/macromicro.json`](json/macromicro.json))

## cnn.com

* Data from 2021-02-01 is accurate, however before that date data is not accurate.
* See https://izy.codes/backtest-strategy-fear-and-greed-index-en/
* See https://github.com/gman4774/fear_and_greed_index github issues
* Data scraped from https://production.dataviz.cnn.io/index/fearandgreed/graphdata/2021-03-01 (now refreshed automatically; see **Automation** above)
* Files: [`datasets/cnn_fear_greed.csv`](datasets/cnn_fear_greed.csv), [`json/cnn_output.json`](json/cnn_output.json)

# archive.org scrape

* Scraped available data from 2012-2022 from waybackmachine
* Not everyday is covered
* File: [`datasets/archive_org_fear_greed_data.csv`](datasets/archive_org_fear_greed_data.csv)


# Correlation with archive.org data

Higher the coefficent the more correlated with archive.org data:

| DATASET   | CORRELATION |
|---------------------------------------|--------|
| openstockalert_fear_greed_data:       | 0.4078 |
| alexey-formalmethods_fear_greed_data: | 0.4029 |
| macromicro_fear_greed_data:           | 0.3437 |

# Combining all the Data

The original combined file used hackingthemarkets (2011-2016), openstockalert (2016-2022), and CNN scrape (2022-2023). That file has been superseded by `fear-greed.csv` (see **Canonical dataset** above), which uses the same 2011 - 2021-01-29 archive but pulls 2021-02-01 onward directly from the live CNN endpoint.

* File: [`fear-greed.csv`](fear-greed.csv)

## About the data

CNN's score bands (derived empirically from its own labels in [`datasets/cnn_fear_greed.csv`](datasets/cnn_fear_greed.csv)):

| EMOTION       | RANGE        |
|---------------|--------------|
| Extreme Fear  | 0 - < 25     |
| Fear          | 25 - < 45    |
| Neutral       | 45 - < 55    |
| Greed         | 55 - < 75    |
| Extreme Greed | >= 75        |

Number of total days in each range from 2011-2023

| Range         | Days      |
|---------------|-----------|
| Extreme Fear  | 503 days  |
| Fear          | 1072 days |
| Neutral       | 1283 days |
| Greed         | 240 days  |
| Extreme Greed | 154 days  |

Average number of days in each range from 2011-2023

| Range          | Average Duration (Days) |
|----------------|-------------------------|
| Extreme Fear   | 41.6                    |
| Fear           | 56.8                    |
| Neutral        | 16.0                    |
| Greed          | 11.8                    |
| Extreme Greed  | 7.7                     |
