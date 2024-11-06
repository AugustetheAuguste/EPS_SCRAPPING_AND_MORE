from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import WebDriverException
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

def download_images(url, max_retries=5, max_album_retries=3):
    album_attempt = 0
    while album_attempt < max_album_retries:
        try:
            options = webdriver.ChromeOptions()
            options.headless = True
            options.binary_location = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
            driver = webdriver.Chrome(options=options)
            driver.get(url)
            time.sleep(2)
            
            screen_height = driver.execute_script("return window.innerHeight")
            scrolled_height = 0
            while True:
                driver.execute_script("window.scrollBy(0, arguments[0]);", screen_height)
                scrolled_height += screen_height
                time.sleep(1)
                new_height = driver.execute_script("return document.body.scrollHeight")
                if scrolled_height >= new_height:
                    break
            time.sleep(5)

            links = driver.find_elements(By.CSS_SELECTOR, 'a[data-lightbox]')
            directory_name = sanitize_filename(url)
            if not os.path.exists(directory_name):
                os.makedirs(directory_name)
            all_images_downloaded = True

            for i, link in enumerate(links):
                relative_url = link.get_attribute('href')
                if relative_url:
                    img_url = relative_url if relative_url.startswith(('http', 'https')) else 'https://baseurl.com' + relative_url
                    retries = 0
                    while retries < max_retries:
                        try:
                            response = requests.get(img_url, timeout=10)
                            if response.status_code == 200:
                                file_name = os.path.join(directory_name, f'{directory_name}_image_{i}.jpg')
                                with open(file_name, 'wb') as f:
                                    f.write(response.content)
                                    print(f'Downloaded high-quality image: {file_name}')
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
            driver.quit()
            if all_images_downloaded:
                break
        except WebDriverException as e:
            log_error(f"WebDriver error for URL {url}: {str(e)}")
        except Exception as e:
            log_error(f"General error for URL {url}: {str(e)}")
        album_attempt += 1
        if album_attempt >= max_album_retries:
            log_error(f"Failed to complete download process for {url} after {max_album_retries} attempts")


urls = [
    "https://efreipicturestudio.fr/gallery/forum-international-de-la-cybersecurite-2022",
    "https://efreipicturestudio.fr/gallery/battle-of-bands-2-2022",
    "https://efreipicturestudio.fr/gallery/shooting-photo-bds-tenis-2022",
    "https://efreipicturestudio.fr/gallery/meet-your-future-2-2023",
    "https://efreipicturestudio.fr/gallery/match-amical-basket-2024",
    "https://efreipicturestudio.fr/gallery/shooting-photo-bds-2022",
    "https://efreipicturestudio.fr/gallery/efrei-trackmania-cup-jour-1-2022",
    "https://efreipicturestudio.fr/gallery/studio-photo-bordeaux-2024",
    "https://efreipicturestudio.fr/gallery/paradons--jour-3-2023",
    "https://efreipicturestudio.fr/gallery/efrei-for-good-7-decembre-2023",
    "https://efreipicturestudio.fr/gallery/conference--devoteam-x-capefrei-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-bureaux-des-assos-et-photo-cv-2022",
    "https://efreipicturestudio.fr/gallery/jpo-25-mars-2023",
    "https://efreipicturestudio.fr/gallery/match-rugbiere-vs-enpc-2024",
    "https://efreipicturestudio.fr/gallery/concert-live--programher-2023",
    "https://efreipicturestudio.fr/gallery/concours-puissance-alpha-2022",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-promo-2020-2021",
    "https://efreipicturestudio.fr/gallery/campagne-bde--jour-1-2024",
    "https://efreipicturestudio.fr/gallery/student-sport-day-2023",
    "https://efreipicturestudio.fr/gallery/jpo-bordeaux-2023",
    "https://efreipicturestudio.fr/gallery/before-soiree-de-noel--bordeaux-2024",
    "https://efreipicturestudio.fr/gallery/rdd-des-pex-2022",
    "https://efreipicturestudio.fr/gallery/journee-portes-ouvertes-mars-2022",
    "https://efreipicturestudio.fr/gallery/espot-v2--4esport-2023",
    "https://efreipicturestudio.fr/gallery/cocktail-de-passation-sep-2023",
    "https://efreipicturestudio.fr/gallery/anniversaire-promo-1993-2023",
    "https://efreipicturestudio.fr/gallery/jpo-21-octobre-2023",
    "https://efreipicturestudio.fr/gallery/spectacle-de-fin-dannee-jour-1-2023",
    "https://efreipicturestudio.fr/gallery/seance-boxe--efight-2023",
    "https://efreipicturestudio.fr/gallery/semaine-learning-xp-2024",
    "https://efreipicturestudio.fr/gallery/soiree-partenariat-societe-generale-2022",
    "https://efreipicturestudio.fr/gallery/soiree-parrainage-alumni-2021",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2023--photobooth-2024",
    "https://efreipicturestudio.fr/gallery/jpo-15-octobre-2022",
    "https://efreipicturestudio.fr/gallery/match-hockefrei-vs-evry-viry-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv--2023",
    "https://efreipicturestudio.fr/gallery/soiree-patinoire-2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-debat-des-presidents-2023",
    "https://efreipicturestudio.fr/gallery/soiree-parrainage-alumni-2023",
    "https://efreipicturestudio.fr/gallery/8e-de-finale-nationale--ogma-2024",
    "https://efreipicturestudio.fr/gallery/jpo-27-janvier-2024",
    "https://efreipicturestudio.fr/gallery/etc-2023--j2-2023"
]


for url in urls:
    download_images(url)
