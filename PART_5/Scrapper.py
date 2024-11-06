from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException

import os
import time
import requests
import hashlib
import datetime

def sanitize_filename(name):
    return hashlib.md5(name.encode()).hexdigest()

def log_error(message):
    with open("error_log.txt", "a") as log_file:
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_file.write(f"[{timestamp}] {message}\n")


def download_images(driver, url, max_retries=5, max_album_retries=3):
    album_attempt = 0
    base_url = "https://efreipicturestudio.fr"
    while album_attempt < max_album_retries:
        try:
            driver.get(url)
            wait = WebDriverWait(driver, 30)
            # Wait for the initial set of images to be loadable
            wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'a[data-lightbox]')))

            # Scroll to the bottom until no more new content loads
            last_height = driver.execute_script("return document.body.scrollHeight")
            while True:
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(3)  # Wait for page to load
                new_height = driver.execute_script("return document.body.scrollHeight")
                if new_height == last_height:
                    break
                last_height = new_height
            
            # Ensure all dynamic contents are loaded
            time.sleep(5)  # Additional wait if the page has very heavy JS after last scroll
            
            links = driver.find_elements(By.CSS_SELECTOR, 'a[data-lightbox]')
            directory_name = sanitize_filename(url)
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
            all_images_downloaded = True

            for i, link in enumerate(links):
                relative_url = link.get_attribute('href')
                img_url = f"{base_url}{relative_url}" if relative_url.startswith('/') else relative_url
                retries = 0
                while retries < max_retries:
                    try:
                        response = requests.get(img_url, timeout=10)
                        if response.status_code == 200:
                            file_name = os.path.join(directory_name, f'{directory_name}_image_{i}.jpg')
                            with open(file_name, 'wb') as f:
                                f.write(response.content)
                                print(f'Downloaded image: {file_name}')
                            break
                        else:
                            retries += 1
                            time.sleep(3)
                    except requests.RequestException as e:
                        log_error(f"Network error for {img_url}: {str(e)}")
                        retries += 1
                        time.sleep(3)
                if retries >= max_retries:
                    all_images_downloaded = False
                    log_error(f"Failed to download {img_url} after {max_retries} attempts")
            if all_images_downloaded:
                break
        except WebDriverException as e:
            log_error(f"WebDriver error for URL {url}: {str(e)}")
            album_attempt += 1
        except Exception as e:
            log_error(f"General error for URL {url}: {str(e)}")
            album_attempt += 1
        if album_attempt >= max_album_retries:
            log_error(f"Failed to complete download process for {url} after {max_album_retries} attempts")




# Setup WebDriver
options = webdriver.ChromeOptions()
options.headless = False
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")  
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36')
driver = webdriver.Chrome(options=options)

urls = [
    "https://efreipicturestudio.fr/gallery/rallye-culturel-2020",
    "https://efreipicturestudio.fr/gallery/rallye-culturel-2021",
    "https://efreipicturestudio.fr/gallery/repetitions-rdd-2019-2021",
    "https://efreipicturestudio.fr/gallery/repetitions-rdd-promo-2020-2021",
    "https://efreipicturestudio.fr/gallery/soiree-dintegration-retrofuturix-2021",
    "https://efreipicturestudio.fr/gallery/soiree-level-up-2022",
    "https://efreipicturestudio.fr/gallery/studio-photo--assemblee-sep-2022",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2022",
    "https://efreipicturestudio.fr/gallery/namastday-2022",
    "https://efreipicturestudio.fr/gallery/afterpod-2022",
    "https://efreipicturestudio.fr/gallery/soiree-passation-bde-2022",
    "https://efreipicturestudio.fr/gallery/journee-airsoft-2022",
    "https://efreipicturestudio.fr/gallery/studio-photo-bureaux-des-assos-2022",
    "https://efreipicturestudio.fr/gallery/photo-classe-l2int4-2022",
    "https://efreipicturestudio.fr/gallery/seminaire-des-associations-2022",
    "https://efreipicturestudio.fr/gallery/spectacle-de-fin-dannee-2022",
    "https://efreipicturestudio.fr/gallery/soiree-vegas-efrei-poker-2022",
    "https://efreipicturestudio.fr/gallery/kanon-day-2022",
    "https://efreipicturestudio.fr/gallery/pod-des-assos-2022",
    "https://efreipicturestudio.fr/gallery/journee-airsoft--2022",
    "https://efreipicturestudio.fr/gallery/soiree-dintegration-2022-2022",
    "https://efreipicturestudio.fr/gallery/pod-des-parrains-2022",
    "https://efreipicturestudio.fr/gallery/weisabi-2022--jour1-2022",
    "https://efreipicturestudio.fr/gallery/weisabi-2022---jour2-2022",
    "https://efreipicturestudio.fr/gallery/weisabi-2022--jour3-2022",
    "https://efreipicturestudio.fr/gallery/efrei-tir-partie-decouverte-2022",
    "https://efreipicturestudio.fr/gallery/franquette--2022",
    "https://efreipicturestudio.fr/gallery/concours-deguisement-halloween-bde-2022",
    "https://efreipicturestudio.fr/gallery/soiree-halloween-horreur-efraction-2022",
    "https://efreipicturestudio.fr/gallery/boat-party--bde-2022",
    "https://efreipicturestudio.fr/gallery/noel-des-enfants-2022",
    "https://efreipicturestudio.fr/gallery/cybernight-2022",
    "https://efreipicturestudio.fr/gallery/pod-de-noel--bde-2022",
    "https://efreipicturestudio.fr/gallery/tournoi-duo-poker-2023",
    "https://efreipicturestudio.fr/gallery/franquette-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-sep-2023",
    "https://efreipicturestudio.fr/gallery/startup-day-2023",
    "https://efreipicturestudio.fr/gallery/inauguration-incubateur-2023",
    "https://efreipicturestudio.fr/gallery/karting-efracing-2023",
    "https://efreipicturestudio.fr/gallery/25-ans-du-live-2023",
    "https://efreipicturestudio.fr/gallery/efrei-poker-tournoi-nintendo-2023",
    "https://efreipicturestudio.fr/gallery/soiree-patinoire--bde-x-hockefrei-2023",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-lundi-2023",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-mercredi-2023",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-debat-des-presidents-2023",
    "https://efreipicturestudio.fr/gallery/photobooth-soiree-vegas-2-2023",
    "https://efreipicturestudio.fr/gallery/soiree-vegas-2-2023",
    "https://efreipicturestudio.fr/gallery/seminaire-des-assos-2023",
    "https://efreipicturestudio.fr/gallery/voyage-bds-jour-1-2023",
    "https://efreipicturestudio.fr/gallery/voyage-bds-jour-2-2023",
    "https://efreipicturestudio.fr/gallery/voyage-bds-jour-3-et-4-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv--bureaux-des-assos-2023",
    "https://efreipicturestudio.fr/gallery/pot-de-depart--incubateur-efrei-2023",
    "https://efreipicturestudio.fr/gallery/gala-des-sponsors--efrei-rugby-2023",
    "https://efreipicturestudio.fr/gallery/pod-de-fin-dannee-2023",
    "https://efreipicturestudio.fr/gallery/forum-des-assos-bordeaux-2023",
    "https://efreipicturestudio.fr/gallery/pod-du-wei-2023",
    "https://efreipicturestudio.fr/gallery/ouverture-coupe-du-monde-rugby--france-vs-nouvelle-zelande-2023",
    "https://efreipicturestudio.fr/gallery/diffusion-match-foot-france-vs-allemagne--bds-2023",
    "https://efreipicturestudio.fr/gallery/soiree-dintegration-bde-2023",
    "https://efreipicturestudio.fr/gallery/soiree-vegas-3-2023",
    "https://efreipicturestudio.fr/gallery/photobooth-soiree-vegas-3-2023",
    "https://efreipicturestudio.fr/gallery/pod-des-parrains-2023",
    "https://efreipicturestudio.fr/gallery/weixico-2023--jour1-2023",
    "https://efreipicturestudio.fr/gallery/weixico-2023--jour2-2023",
    "https://efreipicturestudio.fr/gallery/weixico-2023--jour3-2023",
    "https://efreipicturestudio.fr/gallery/weixico-2023--jour4-2023",
    "https://efreipicturestudio.fr/gallery/partie-airsoft-efrei-tir-2023",
    "https://efreipicturestudio.fr/gallery/pod-des-arts-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-beer-pong-2023",
    "https://efreipicturestudio.fr/gallery/soiree-parrainage-alumni-2023",
    "https://efreipicturestudio.fr/gallery/pod-village-des-associations-de-noel-2024",
    "https://efreipicturestudio.fr/gallery/soiree-passation-wei-2024",
    "https://efreipicturestudio.fr/gallery/photobooth--25-ans-eps-2024",
    "https://efreipicturestudio.fr/gallery/photobooth--25-ans-eps-2024",
    "https://efreipicturestudio.fr/gallery/pod-de-ladmin-2024",
    "https://efreipicturestudio.fr/gallery/soiree-vegas-4-photobooth-2024",
    "https://efreipicturestudio.fr/gallery/soiree-vegas-4-2024",
    "https://efreipicturestudio.fr/gallery/pod-iweek-2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--soiree-2-2024",
    "https://efreipicturestudio.fr/gallery/camapagne-bde--soiree-3--2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--soiree-4--2024",
    "https://efreipicturestudio.fr/gallery/pod-des-resultats-2024"
]

driver.get(urls[0])
time.sleep(45)

reversed_list = urls[::-1]

for url in reversed_list:
    download_images(driver, url)

driver.quit()
