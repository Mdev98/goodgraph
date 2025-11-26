# Conversion PNG -> WebP (optimisé)

Ce petit outil permet d'optimiser vos images PNG et de générer des versions WebP à plusieurs largeurs.

Fichiers ajoutés:
- `tools/convert_pngs_to_webp.py` — script principal
- `requirements.txt` — dépendance `Pillow`

Exemples d'utilisation (depuis la racine du projet):

Install (virtuenv recommandé):
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Générer WebP 480, 800, 1200 px avec qualité 80 (défaut):
```bash
python tools/convert_pngs_to_webp.py --root public --sizes 480 800 1200 --quality 80
```

Forcer écrasement des fichiers déjà présents:
```bash
python tools/convert_pngs_to_webp.py --root public --sizes 480 800 1200 --quality 80 --overwrite
```

Autoriser l'upscale (générer une taille plus large que l'original — déconseillé):
```bash
python tools/convert_pngs_to_webp.py --root public --sizes 1200 --allow-upscale
```

Notes:
- Le script ne traite que les fichiers avec l'extension `.png`.
- Les fichiers WebP seront créés dans le même dossier que le PNG d'origine, nommés `nom_<width>.webp`.
- Qualité recommandée: 75-85. Par défaut le script utilise 80.
