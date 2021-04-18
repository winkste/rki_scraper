#%%
import requests
import pprint
import celle
import noh
from matplotlib import pyplot
import pandas as pd
import paho.mqtt.publish as publish
import logging
import logging.config
import datetime
import secrets
import time

SW_NAME = 'RKI Scraper'
SW_VERSION = 'v0.0.1'

# %%
def update_rki_data_file(location, dataset, api_link):
    res = requests.get(api_link).json()
    features = res.get('features')
    feat = features[0]
    attrib = feat.get('attributes')
    date_key = attrib.get('last_update')
    dataset.data[date_key] = attrib
    file = open(location + '.py', 'w')
    file.write('data =' + pprint.pformat(dataset.data))
    file.close()
    return date_key

def plot_cases7_100k(location, dataset):
    x = datetime.datetime.now()
    file_name = x.strftime('%y%m%d%H%M') + '_' + location + '.png'
    my_panda = pd.DataFrame.from_dict(dataset.data, orient='index')
    p = pd.DataFrame.from_dict(dataset.data, orient='index')
    fig, ax = pyplot.subplots()
    ax.plot(p['cases7_per_100k'], 'o-')
    ax.set_title("7 day incident per 100k for: " + location)
    ax.set_xlabel('Time')
    ax.set_ylabel('7 day incident per 100k')
    pyplot.savefig('../logs/' + file_name)
    #pyplot.show()

def subplot_cases7_100k(loc1, data1, loc2, data2):
    x = datetime.datetime.now()
    file_name = x.strftime('%y%m%d%H%M') + '_' + loc1 + '-' + loc2 + '.png'
    p1 = pd.DataFrame.from_dict(data1.data, orient='index')
    p2 = pd.DataFrame.from_dict(data2.data, orient='index')
    fig, ax = pyplot.subplots()
    ax.plot(p1['cases7_per_100k'], 'o-')
    ax.plot(p2['cases7_per_100k'], '.-')
    ax.set_title("7 day incident per 100k")
    legend = ax.legend([loc1, loc2], loc='best', shadow=True, fontsize='x-large')
    pyplot.savefig('../logs/' + file_name)
    #pyplot.show()

def publish_actual_cases(topic, payload): 
    publish.single(topic, payload, hostname=secrets.hostname, port=secrets.port, client_id=secrets.client_id, auth=secrets.auth)

if __name__ == '__main__':
    last_date_key = None
    logging.config.fileConfig('logging.conf')
    logger = logging.getLogger('rki_scraper')


    logger.info('Software information: ' + SW_NAME + ' ' + SW_VERSION)
    while True:
        logger.info('retrieve latest values from RKI...')
        date_key = update_rki_data_file('celle', celle, 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2034%20AND%20OBJECTID%20%3C%3D%2035&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json')
        update_rki_data_file('noh', noh, 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=OBJECTID%20%3E%3D%2055%20AND%20OBJECTID%20%3C%3D%2056&outFields=OBJECTID,GEN,BEZ,death_rate,cases,deaths,cases_per_100k,cases_per_population,last_update,cases7_per_100k,recovered,cases7_bl_per_100k,cases7_bl,death7_bl,cases7_lk,death7_lk,cases7_per_100k_txt,AdmUnitId&outSR=4326&f=json')
        if date_key != last_date_key:
            last_date_key = date_key
            logger.info('plot curves to files...')
            plot_cases7_100k('Celle', celle)
            plot_cases7_100k('Nordhorn', noh)
            subplot_cases7_100k('Celle', celle, 'Nordhorn', noh)

            logger.info('publish latest cases to MQTT broker...')
            actual = str(round(celle.data[date_key]['cases7_per_100k'], 3))
            topic = "std/dev200/s/rki/ce/c7"
            publish_actual_cases(topic, actual)
            actual = str(round(noh.data[date_key]['cases7_per_100k'], 3))
            topic = "std/dev200/s/rki/noh/c7"
            publish_actual_cases(topic, actual)
        
        logger.info('sleep...')
        time.sleep(60 * 5) #check every five minutes for the new values

