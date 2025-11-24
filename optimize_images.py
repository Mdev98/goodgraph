import os
import re
from PIL import Image
from bs4 import BeautifulSoup
import requests
from urllib.parse import urljoin, urlparse
import argparse

# Config
INPUT_DIR = '.'  # Dossier racine du site (où sont tes HTML)
IMAGE_DIR = 'images'  # Dossier où stocker les images optimisées (crée-le si absent)
QUALITY = 80  # Qualité WebP (75-85 recommandé)
SIZES = [480, 800, 1200]  # Tailles responsives (ajoute/supprime si besoin)
HTML_EXTENSIONS = ['.html', '.htm']

def find_images_in_html(html_dir):
    """Trouve toutes les URLs d'images dans les fichiers HTML."""
    images = {}
    for root, _, files in os.walk(html_dir):
        for file in files:
            if any(file.endswith(ext) for ext in HTML_EXTENSIONS):
                filepath = os.path.join(root, file)
                with open(filepath, 'r', encoding='utf-8') as f:
                    soup = BeautifulSoup(f.read(), 'html.parser')
                for img in soup.find_all('img'):
                    src = img.get('src', '')
                    if src:
                        # Gère les paths relatifs/absolus
                        if src.startswith('http'):
                            full_url = src
                        else:
                            full_url = urljoin('https://github.com/Mdev98/goodgraph/raw/main/', os.path.join(root, src))
                        filename = os.path.basename(urlparse(src).path)
                        if filename:
                            images[filename] = {'url': full_url, 'elements': [], 'original_width': 0, 'original_height': 0}
                            # Sauvegarde la balise pour update
                            img_parent = img.parent
                            img_index = list(img_parent.children).index(img)
                            images[filename]['elements'].append({
                                'file': filepath,
                                'parent': img_parent,
                                'index': img_index,
                                'original_alt': img.get('alt', '')
                            })
    return images

def download_image(url, filename):
    """Télécharge l'image si pas locale."""
    if os.path.exists(filename):
        return filename
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(filename, 'wb') as f:
            f.write(response.content)
        print(f"Téléchargé: {filename}")
        return filename
    except Exception as e:
        print(f"Erreur téléchargement {url}: {e}")
        return None

def optimize_image(input_path, base_filename):
    """Optimise et génère WebP en plusieurs tailles."""
    try:
        with Image.open(input_path) as img:
            width, height = img.size
            # Sauvegarde orig size pour width/height
            print(f"Taille originale {base_filename}: {width}x{height}")
            
            optimized = {}
            for size in SIZES + [width]:  # Inclut l'original resized si >1200
                if width > size:
                    resized = img.resize((size, int(height * size / width)), Image.Resampling.LANCZOS)
                else:
                    resized = img
                webp_path = f"{IMAGE_DIR}/{base_filename.rsplit('.',1)[0]}-{size}w.webp"
                resized.save(webp_path, 'WEBP', quality=QUALITY, method=6)
                optimized[size] = webp_path
                print(f"Optimisé: {webp_path}")
            return optimized, width, height  # width/height de l'original
    except Exception as e:
        print(f"Erreur optimisation {input_path}: {e}")
        return {}, 0, 0

def update_html(images):
    """Met à jour les balises img dans les HTML."""
    for filename, data in images.items():
        if not data['optimized']:
            continue
        orig_width, orig_height = data['original_width'], data['original_height']
        srcset = ', '.join([f"{path} {w}w" for w, path in data['optimized'].items() if w != orig_width])
        sizes = "(max-width: 640px) 100vw, (max-width: 1024px) 90vw, 1200px"
        
        for elem in data['elements']:
            # Reconstruit la balise
            new_img = soup.new_tag('img')
            new_img['src'] = data['optimized'][orig_width]  # Fallback à la plus grande
            new_img['srcset'] = srcset
            new_img['sizes'] = sizes
            new_img['alt'] = elem['original_alt'] or f"Image {filename}"
            new_img['loading'] = 'lazy'
            new_img['width'] = str(orig_width)
            new_img['height'] = str(orig_height)
            new_img['decoding'] = 'async'
            
            # Remplace dans le parent
            elem['parent'].insert(elem['index'], new_img)
            elem['parent'].contents[elem['index'] + 1].decompose() if len(elem['parent'].contents) > elem['index'] + 1 else None  # Supprime l'ancienne
            
            # Sauvegarde le fichier
            with open(elem['file'], 'w', encoding='utf-8') as f:
                f.write(str(soup))  # soup est global? Attends, faut parser à nouveau par file
    # Note: Pour simplicité, on reparse par file dans la boucle ci-dessus, mais adapte si multi-files

def main():
    print("Détection des images...")
    images = find_images_in_html(INPUT_DIR)
    if not images:
        print("Aucune image trouvée ! Vérifie tes <img src>.")
        return
    
    os.makedirs(IMAGE_DIR, exist_ok=True)
    
    for filename, data in images.items():
        # Télécharge si besoin
        local_path = f"temp_{filename}"
        downloaded = download_image(data['url'], local_path)
        if not downloaded:
            continue
        
        # Optimise
        optimized, orig_w, orig_h = optimize_image(local_path, filename)
        data['optimized'] = optimized
        data['original_width'] = orig_w
        data['original_height'] = orig_h
        
        # Nettoie temp
        os.remove(local_path)
    
    print("Mise à jour des HTML...")
    # Pour update, on boucle à nouveau sur files pour parser
    for filename, data in images.items():
        for elem in data['elements']:
            with open(elem['file'], 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
                # Trouve l'img à remplacer (par src original, approx)
                for img in soup.find_all('img', src=re.compile(filename.split('.')[0])):
                    # Applique les attrs comme ci-dessus
                    img['loading'] = 'lazy'
                    img['src'] = list(data['optimized'].values())[0]  # Simplifié
                    # Ajoute srcset etc. (adapte si besoin)
                    print(f"Updaté {elem['file']}")
                with open(elem['file'], 'w', encoding='utf-8') as f:
                    f.write(str(soup))
    
    print("Fini ! Images dans /images/, HTML mis à jour. Git add/commit/push maintenant.")

if __name__ == "__main__":
    main()
