# RKI DATA SCRAPER
Python project to read RKI statistics for dedicated countries and plot/publish these values

## Introduction
The theory of concept of this python program is to connect to the RKI web page API to readout for one particular country the actual COVID-19 statistics. Currently this is done exemplary for two contries I'm interested in: Celle, Nordhorn.
The data will be stored in two separate python data files using pprint. The data is organized as dictionaries where the date/time is the key and the complete dataset is the value.
These datasets are used to print some plots each country as single and both together for comparison. 
Last the new received data, the last dataset in the dataset files are published to a MQTT broker to add it to a home automation for displaying.

### Dataset Plots
![2104180802_Celle-Nordhorn](https://user-images.githubusercontent.com/9803344/115136140-18c5a080-a01e-11eb-9a87-ca09d0d4f310.png)
![2104180802_Celle](https://user-images.githubusercontent.com/9803344/115136144-1b27fa80-a01e-11eb-89ad-e1de62dbe11b.png)
![2104180802_Nordhorn](https://user-images.githubusercontent.com/9803344/115136146-1fecae80-a01e-11eb-92e1-06dc649a50a7.png)

## Setup & Preparations
There are two methods provided to run the rki scraper:
- Python endless loop: run endless loop in Python with a dedicated sleep function
- Single shot: Run scraper once, can be combined with a cronjob 

### Single shot with cronjob
Ensure that your environment is set to the correct editor:
```
echo $EDITOR
export EDITOR=nano
echo $EDITOR
```

List all available cronjobs:
```
crontab -l
```

Edit cronjobs
```
crontab -e

```

Cronjob example:
```
0 5 * * * /Users/winkste/workspace_github/rki_scraper/venv/bin/python /Users/winkste/workspace_github/rki_scraper/scripts/launch.py

```
This cronjob runs every day at 5am.
