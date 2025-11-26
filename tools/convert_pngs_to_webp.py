#!/usr/bin/env python3
"""
Optimise les images PNG et génère des WebP à plusieurs largeurs.

Usage:
  python tools/convert_pngs_to_webp.py --root public --sizes 480 800 1200 --quality 80

Le script cherche récursivement les fichiers `.png` sous `--root`, puis génère
des fichiers WebP nommés `basename_<width>.webp` dans le même dossier.

Par défaut, il n'agrandit pas les images (pas d'upscale). Utilisez `--allow-upscale`
pour forcer la génération même si la taille cible est supérieure à la largeur originale.
"""
from __future__ import annotations

import argparse
import logging
from pathlib import Path
from typing import List

from PIL import Image


def find_pngs(root: Path) -> List[Path]:
    return sorted(root.rglob('*.png'))


def make_webp_for_image(path: Path, sizes: List[int], quality: int, overwrite: bool, allow_upscale: bool) -> int:
    """Génère plusieurs WebP pour une image PNG. Retourne le nombre de fichiers créés."""
    created = 0
    try:
        with Image.open(path) as im:
            orig_w, orig_h = im.size
            for target_w in sizes:
                if target_w <= 0:
                    logging.debug('Taille ignorée (<=0): %s', target_w)
                    continue
                if (orig_w < target_w) and (not allow_upscale):
                    logging.info('Skip upscale: %s (%d < %d)', path.name, orig_w, target_w)
                    continue
                target_h = max(1, int(orig_h * (target_w / orig_w)))
                resized = im.resize((target_w, target_h), resample=Image.LANCZOS)

                out_name = f"{path.stem}_{target_w}.webp"
                out_path = path.with_name(out_name)

                if out_path.exists() and (not overwrite):
                    logging.info('Fichier existe, skip: %s', out_path.name)
                    continue

                save_kwargs = {
                    'format': 'WEBP',
                    'quality': quality,
                    'method': 6,
                }
                # Sauvegarder
                resized.save(out_path, **save_kwargs)
                created += 1
                logging.info('Créé: %s', out_path)
    except Exception as e:
        logging.error('Erreur traitement %s: %s', path, e)
    return created


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Convertit et optimise les PNG en WebP à plusieurs tailles')
    parser.add_argument('--root', '-r', type=Path, default=Path('public'), help='Dossier racine à scanner (défaut: public)')
    parser.add_argument('--sizes', '-s', nargs='+', type=int, default=[480, 800, 1200], help='Largeurs cibles (px)')
    parser.add_argument('--quality', '-q', type=int, default=80, help='Qualité WebP (0-100). Défaut 80')
    parser.add_argument('--overwrite', action='store_true', help='Écrase les WebP existants')
    parser.add_argument('--allow-upscale', action='store_true', help="Autorise l'upscale si la largeur cible est > largeur originale")
    parser.add_argument('--verbose', '-v', action='store_true', help='Affiche plus de logs')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO), format='[%(levelname)s] %(message)s')

    root = args.root
    if not root.exists() or not root.is_dir():
        logging.error('Dossier introuvable: %s', root)
        return 2

    sizes = sorted(set(args.sizes))
    logging.info('Recherche .png sous: %s', root)
    pngs = find_pngs(root)
    if not pngs:
        logging.info('Aucune image .png trouvée sous %s', root)
        return 0

    total_created = 0
    for p in pngs:
        logging.info('Traitement: %s', p)
        created = make_webp_for_image(p, sizes, args.quality, args.overwrite, args.allow_upscale)
        total_created += created

    logging.info('Terminé — fichiers WebP créés: %d', total_created)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
