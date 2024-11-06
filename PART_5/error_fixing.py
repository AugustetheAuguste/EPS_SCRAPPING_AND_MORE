import os
import hashlib

def sanitize_filename(name):
    """Sanitize strings to be used as filenames by hashing."""
    return hashlib.md5(name.encode()).hexdigest()

def find_empty_directories(root_dir):
    """Find all directories within the given root directory that contain 10 items or less."""
    small_dirs = []
    for dirpath, dirnames, filenames in os.walk(root_dir):
        total_items = len(dirnames) + len(filenames)  # Total count of subdirectories and files
        if total_items <= 30:  # Check if the total number of items is 10 or less
            small_dirs.append(dirpath)
    return small_dirs

def map_directories_to_urls(directories, urls):
    """Map directory names back to their corresponding URLs."""
    url_map = {sanitize_filename(url): url for url in urls}
    empty_url_list = [url_map.get(os.path.basename(dir)) for dir in directories if os.path.basename(dir) in url_map]
    return [url for url in empty_url_list if url]

def extract_error_urls(log_file_path):
    """Extract URLs with errors from the log file."""
    error_urls = []
    with open(log_file_path, "r") as file:
        for line in file:
            if "URL" in line:
                try:
                    start = line.index("URL ") + 4
                    end = line.index(":", start)
                    url = line[start:end]
                    error_urls.append(url)
                except ValueError:
                    continue  # Handle the case where the formatting might not match
    return list(set(error_urls))

def main():
    root_directory = "IMAGE_DIRECTORIES"  # Update this to your directories path
   
    urls = [
    "https://efreipicturestudio.fr/gallery/rentree-l1-2020-2020",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv-21102020-2020",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-promo-2019-2021",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2019-2021",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-promo-2020-2021",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2020-2021",
    "https://efreipicturestudio.fr/gallery/journee-dintegration-2021-2021",
    "https://efreipicturestudio.fr/gallery/soiree-parrainage-alumni-2021",
    "https://efreipicturestudio.fr/gallery/concert-unicef-2022",
    "https://efreipicturestudio.fr/gallery/aki-party-2021-2021",
    "https://efreipicturestudio.fr/gallery/studio-bordeaux-2022",
    "https://efreipicturestudio.fr/gallery/photos-cv-2021",
    "https://efreipicturestudio.fr/gallery/journee-de-la-technologie-au-service-de-lhumain-2022https://efreipicturestudio.fr/gallery/journee-portes-ouvertes-janvier-2022",
    "https://efreipicturestudio.fr/gallery/journee-portes-ouvertes-janvier-2022",
    "https://efreipicturestudio.fr/gallery/jpo-bordeaux-2022",
    "https://efreipicturestudio.fr/gallery/battle-of-bands-2-2022",
    "https://efreipicturestudio.fr/gallery/journee-portes-ouvertes-mars-2022",
    "https://efreipicturestudio.fr/gallery/concours-puissance-alpha-2022",
    "https://efreipicturestudio.fr/gallery/efrei-trackmania-cup-jour-1-2022",
    "https://efreipicturestudio.fr/gallery/efrei-trackmania-cup-jour-2-2022",
    "https://efreipicturestudio.fr/gallery/journee-portes-ouvertes--conference-micode-2022",
    "https://efreipicturestudio.fr/gallery/match-hockefrei-2022",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-des-pex-2022",
    "https://efreipicturestudio.fr/gallery/rdd-des-pex-2022",
    "https://efreipicturestudio.fr/gallery/journee-porte-ouverte-2022",
    "https://efreipicturestudio.fr/gallery/forum-international-de-la-cybersecurite-2022",
    "https://efreipicturestudio.fr/gallery/challenge-sciences-2024-2022",
    "https://efreipicturestudio.fr/gallery/soiree-nologie-alumni-2022",
    "https://efreipicturestudio.fr/gallery/conference-token-economy--efrei-business-angels-2022",
    "https://efreipicturestudio.fr/gallery/gala-passation-sep-2022",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2021-2022",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-promo-2021-2022",
    "https://efreipicturestudio.fr/gallery/studio-photo-bureaux-des-assos-et-photo-cv-2022",
    "https://efreipicturestudio.fr/gallery/photobooth-soiree-alumni-les-chouettes-dor-2022",
    "https://efreipicturestudio.fr/gallery/soiree-alumni-les-chouettes-dor-2022",
    "https://efreipicturestudio.fr/gallery/forum-des-assos--natsu-matsuri-2022",
    "https://efreipicturestudio.fr/gallery/meet-your-future-1-2022",
    "https://efreipicturestudio.fr/gallery/rezal--godzillan-2022",
    "https://efreipicturestudio.fr/gallery/evenements-integration-bordeaux-2022",
    "https://efreipicturestudio.fr/gallery/studio-photo-bordeaux-2022",
    "https://efreipicturestudio.fr/gallery/soiree-4esport-2022",
    "https://efreipicturestudio.fr/gallery/jpo-15-octobre-2022",
    "https://efreipicturestudio.fr/gallery/shooting-photo-bds-2022",
    "https://efreipicturestudio.fr/gallery/fete-des-lumieres--diwali-2022",
    "https://efreipicturestudio.fr/gallery/shooting-photo-bds-tenis-2022",
    "https://efreipicturestudio.fr/gallery/soiree-partenariat-societe-generale-2022",
    "https://efreipicturestudio.fr/gallery/jpo-3-decembre-2022",
    "https://efreipicturestudio.fr/gallery/journee-efrei-for-good-2022",
    "https://efreipicturestudio.fr/gallery/journee-efrei-for-good-2022",
    "https://efreipicturestudio.fr/gallery/tournoi-valorant-sorbonne--4esport-2022",
    "https://efreipicturestudio.fr/gallery/jpo-21-janvier-2023",
    "https://efreipicturestudio.fr/gallery/jpo-bordeaux-2023",
    "https://efreipicturestudio.fr/gallery/aki-party-2023-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-aki-party-2023-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv-2023",
    "https://efreipicturestudio.fr/gallery/jpo-11-fevrier-2023",
    "https://efreipicturestudio.fr/gallery/afterwork-efrei-for-women-2023",
    "https://efreipicturestudio.fr/gallery/paradons--jour-1-2023",
    "https://efreipicturestudio.fr/gallery/paradons--jour-2-2023",
    "https://efreipicturestudio.fr/gallery/paradons--jour-3-2023",
    "https://efreipicturestudio.fr/gallery/concert-live--programher-2023",
    "https://efreipicturestudio.fr/gallery/degustation-de-vin-millesime-2023",
    "https://efreipicturestudio.fr/gallery/match-efreifoot-2023",
    "https://efreipicturestudio.fr/gallery/rezal-rezoblivion--clubrezo-2023",
    "https://efreipicturestudio.fr/gallery/journee-sante--sport-2023",
    "https://efreipicturestudio.fr/gallery/spectacle-de-fin-dannee-jour-1-2023",
    "https://efreipicturestudio.fr/gallery/spectacle-de-fin-dannee-jour-2-2023",
    "https://efreipicturestudio.fr/gallery/jpo-25-mars-2023",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-debat-des-presidents-2023",
    "https://efreipicturestudio.fr/gallery/campagne-bde-2023-jeudi-2023",
    "https://efreipicturestudio.fr/gallery/etc-2023--j1-2023",
    "https://efreipicturestudio.fr/gallery/etc-2023--j2-2023",
    "https://efreipicturestudio.fr/gallery/student-sport-day-2023",
    "https://efreipicturestudio.fr/gallery/journee-internationale-2023",
    "https://efreipicturestudio.fr/gallery/conference--devoteam-x-capefrei-2023",
    "https://efreipicturestudio.fr/gallery/namastday-2023",
    "https://efreipicturestudio.fr/gallery/exposition-art-efrei-x-isit-2023",
    "https://efreipicturestudio.fr/gallery/espot-v2--4esport-2023",
    "https://efreipicturestudio.fr/gallery/semaine-learning-xp-2023",
    "https://efreipicturestudio.fr/gallery/finale-des-playoffs--efrei-foot-2023",
    "https://efreipicturestudio.fr/gallery/jpo-13-mai-2023",
    "https://efreipicturestudio.fr/gallery/match-de-basket--efrei-basketball-2023",
    "https://efreipicturestudio.fr/gallery/bapteme-soufflerie--efrei-para-2023",
    "https://efreipicturestudio.fr/gallery/battle-of-the-band-2023",
    "https://efreipicturestudio.fr/gallery/flyforeveryone--efrei-falcon-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-bds-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-hockefrei-2023",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2022-2023",
    "https://efreipicturestudio.fr/gallery/photobooth-rdd-promo-2022-2023",
    "https://efreipicturestudio.fr/gallery/anniversaire-promo-1993-2023",
    "https://efreipicturestudio.fr/gallery/cocktail-de-passation-sep-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-hockefrei--2023",
    "https://efreipicturestudio.fr/gallery/boost-ton-alternance-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv--2023",
    "https://efreipicturestudio.fr/gallery/tournoi-de-basket-2023",
    "https://efreipicturestudio.fr/gallery/soiree-chouettes-dor-2023",
    "https://efreipicturestudio.fr/gallery/photobooth-soiree-chouettes-dor-2023",
    "https://efreipicturestudio.fr/gallery/conference-impact-environnemental-de-la-tech-2023",
    "https://efreipicturestudio.fr/gallery/solution-factory-2023",
    "https://efreipicturestudio.fr/gallery/fly-for-everyone-2023",
    "https://efreipicturestudio.fr/gallery/rentree-l1-2023",
    "https://efreipicturestudio.fr/gallery/village-des-assos-2023",
    "https://efreipicturestudio.fr/gallery/feria-del-tejon-2023",
    "https://efreipicturestudio.fr/gallery/meet-your-future-2-2023",
    "https://efreipicturestudio.fr/gallery/journee-wei-x-bde-2023",
    "https://efreipicturestudio.fr/gallery/decouverte-de-paris-1-2023",
    "https://efreipicturestudio.fr/gallery/rezamigos-2023",
    "https://efreipicturestudio.fr/gallery/journees-associatives-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-deguisement-2023",
    "https://efreipicturestudio.fr/gallery/journee-associative-2023",
    "https://efreipicturestudio.fr/gallery/journee-sport-et-sante-2023",
    "https://efreipicturestudio.fr/gallery/debat-ffde--ogma-vs-la-joute-de-vinci-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-bounty--efrei-poker-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-de-programmation-2023",
    "https://efreipicturestudio.fr/gallery/jpo-21-octobre-2023",
    "https://efreipicturestudio.fr/gallery/seance-boxe--efight-2023",
    "https://efreipicturestudio.fr/gallery/meet-your-future-bordeaux-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-halloween-2023",
    "https://efreipicturestudio.fr/gallery/seance-de-lutte--efight-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv-09-novembre-2023",
    "https://efreipicturestudio.fr/gallery/el-dia-de-los-muertos-2023",
    "https://efreipicturestudio.fr/gallery/semaine-des-arts-2023",
    "https://efreipicturestudio.fr/gallery/studio-photo-cv-14-novembre-2023",
    "https://efreipicturestudio.fr/gallery/cybernight-2023",
    "https://efreipicturestudio.fr/gallery/jpo-25-novembre-2023",
    "https://efreipicturestudio.fr/gallery/soiree-parrainage-alumni-2023",
    "https://efreipicturestudio.fr/gallery/competition-regionale-de-nage-2023",
    "https://efreipicturestudio.fr/gallery/match-hockefrei-vs-evry-viry-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-poker-secret-santa-2023",
    "https://efreipicturestudio.fr/gallery/efrei-for-good-7-decembre-2023",
    "https://efreipicturestudio.fr/gallery/competition-universitaire-de-tir-a-larc-2023",
    "https://efreipicturestudio.fr/gallery/noel-des-enfants-2023",
    "https://efreipicturestudio.fr/gallery/before-soiree-de-noel--bordeaux-2024",
    "https://efreipicturestudio.fr/gallery/village-des-associations-de-noel-2024",
    "https://efreipicturestudio.fr/gallery/match-efrei-rugby-vs-lycee-sainte-genevieve-2023",
    "https://efreipicturestudio.fr/gallery/tournoi-poker--bordeaux-2024",
    "https://efreipicturestudio.fr/gallery/journee-du-cinema-2024",
    "https://efreipicturestudio.fr/gallery/seminaire-orientation-l3-2024",
    "https://efreipicturestudio.fr/gallery/tournoi-duo-poker-2024",
    "https://efreipicturestudio.fr/gallery/bapteme-soufflerie-2024",
    "https://efreipicturestudio.fr/gallery/jpo-27-janvier-2024",
    "https://efreipicturestudio.fr/gallery/match-amical-basket-2024",
    "https://efreipicturestudio.fr/gallery/startup-day-2024",
    "https://efreipicturestudio.fr/gallery/espot-v3-2024",
    "https://efreipicturestudio.fr/gallery/paradons--vendredi-2024",
    "https://efreipicturestudio.fr/gallery/paradons--samedi-2024",
    "https://efreipicturestudio.fr/gallery/paradons--dimanche-2024",
    "https://efreipicturestudio.fr/gallery/match-rugbiere-vs-enpc-2024",
    "https://efreipicturestudio.fr/gallery/jpo-2-mars-2024",
    "https://efreipicturestudio.fr/gallery/african-day-2024-2024",
    "https://efreipicturestudio.fr/gallery/student-sport-day-2024",
    "https://efreipicturestudio.fr/gallery/soiree-patinoire-2024",
    "https://efreipicturestudio.fr/gallery/studio-photo-bordeaux-2024",
    "https://efreipicturestudio.fr/gallery/journee-internationale-2024",
    "https://efreipicturestudio.fr/gallery/sfa-2024-2024",
    "https://efreipicturestudio.fr/gallery/8e-de-finale-nationale--ogma-2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--jour-1-2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--jour-2-2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--jour-3--2024",
    "https://efreipicturestudio.fr/gallery/campagne-bde--jour-4--2024",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2023--cocktail-2024",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2023--ceremonie-2024",
    "https://efreipicturestudio.fr/gallery/rdd-promo-2023--photobooth-2024",
    "https://efreipicturestudio.fr/gallery/semaine-learning-xp-2024",
    "https://efreipicturestudio.fr/gallery/pitch-m1-mon-stage-en-180-secondes--2024",
    "https://efreipicturestudio.fr/gallery/printemps-des-entrepreneurs-2024"
]


    log_file_path = "error_log.txt"  # Make sure this path is correct

    empty_dirs = find_empty_directories(root_directory)
    empty_urls = map_directories_to_urls(empty_dirs, urls)
    
    error_urls = extract_error_urls(log_file_path)
    
    all_problematic_urls = list(set(empty_urls + error_urls))
    
    with open("error_fixing_urls.txt", "w") as file:
        for url in all_problematic_urls:
            file.write(url + "\n")

    print("Identified URLs with issues have been written to error_fixing_urls.txt")

if __name__ == "__main__":
    main()

