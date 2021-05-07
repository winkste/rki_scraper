# RKI DATA SCRAPER
Python project to read RKI statistics for dedicated countries and plot/publish these values

## Introduction
The theory of concept of this python program is to connect to the RKI web page API to readout for one particular country the actual COVID-19 statistics. Currently this is done exemplary for two contries I'm interested in: Celle, Nordhorn.
The data will be stored in two separate python data files using pprint. The data is organized as dictionaries where the date/time is the key and the complete dataset is the value.
These datasets are used to print some plots: each country as single and both countries together for comparison. 

### Dataset Plots
![2104180802_Celle-Nordhorn](https://user-images.githubusercontent.com/9803344/115136140-18c5a080-a01e-11eb-9a87-ca09d0d4f310.png)
![2104180802_Celle](https://user-images.githubusercontent.com/9803344/115136144-1b27fa80-a01e-11eb-89ad-e1de62dbe11b.png)
![2104180802_Nordhorn](https://user-images.githubusercontent.com/9803344/115136146-1fecae80-a01e-11eb-92e1-06dc649a50a7.png)

The next feature is to publish the latest received datasets (here the 7 day incident value) to a MQTT broker to integrate it to Home Assistant.

<img width="382" alt="Bildschirmfoto 2021-04-22 um 05 58 14" src="https://user-images.githubusercontent.com/9803344/115653866-449f9980-a330-11eb-8991-7aa8b52b673f.png">


## Setup & Preparations
There are two methods provided to run the rki scraper:
- Python endless loop: run endless loop in Python with a dedicated sleep function
- Single shot: Run scraper once, can be combined with a cronjob

### Virtual environment setup
This project relates on several common python packages. All packages are stored in a requirements.txt file which can be used to generate a virtual environment. This virtual environment is used later in the cronjob execution method.

### MQTT configuration
All connection details to connect to a MQTT broker to publish the statistic data is read from a secrets.py file. As this contains security keys and passwords, this is not stored in this repository, you will find a template secrets.py file in the source file list which you can modify to your local settings. The mqtt messages are currently hardcoded.

### Identify another country
Under /resources there is an example export from the RKI database stored. This example include all countries and with this the country number needed to modify the api request. use this file to identify the correct country.
```
Example:
Celle has the Object ID 34, this leads to a api request with the following entry:
https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2034%20AND%20OBJECTID%20%3C%3D%2034&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json

find the 34 in the api request above.

```

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
