import os
from rki_scraper import loop_rki_scraper
from rki_scraper import run_rki_scraper_once



if __name__ == '__main__':
    sys_path = os.getcwd()
    os.chdir(os.path.dirname(os.path.realpath(__file__)))
    run_rki_scraper_once()
    os.chdir(sys_path)
