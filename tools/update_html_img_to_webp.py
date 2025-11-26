#!/usr/bin/env python3
"""
Remplace les balises <img> ciblant des fichiers .png par des balises optimisées
utilisant les fichiers WebP générés par `convert_pngs_to_webp.py`.

Fonctionnalités:
- Parcourt récursivement les fichiers `.html` sous `--root` (défaut: racine du projet).
- Pour chaque `<img src="...*.png">`, remplace par:
  - `src` pointant vers la version WebP de largeur par défaut (800)
  - `srcset` listant les tailles (480,800,1200) avec suffixe `_WIDTH.webp`
  - ajoute `loading="lazy"` et `decoding="async"`
- Options: `--sizes`, `--prefer-size`, `--dry-run`, `--backup`.
"""
from __future__ import annotations

import argparse
import logging
import shutil
from pathlib import Path
from typing import List

from bs4 import BeautifulSoup


def process_html_file(path: Path, sizes: List[int], prefer_size: int, dry_run: bool, backup: bool) -> bool:
    logging.debug('Lecture %s', path)
    text = path.read_text(encoding='utf-8')
    soup = BeautifulSoup(text, 'html.parser')
    changed = False

    for img in soup.find_all('img'):
        src = img.get('src')
        if not src:
            continue
        if not src.lower().endswith('.png'):
            continue

        p = Path(src)
        dir_part = p.parent
        stem = p.stem

        # Construire chemins relatifs en conservant le prefix original
        prefix = ''
        if str(src).startswith('./'):
            prefix = './'
        elif str(src).startswith('/'):
            prefix = '/'

        # Générer noms webp
        webp_paths = []
        for w in sizes:
            name = f"{stem}_{w}.webp"
            if str(dir_part) in ('.', '/'):
                webp_paths.append(f"{prefix}{name}")
            else:
                webp_paths.append(f"{prefix}{dir_part.as_posix()}/{name}")

        # Choisir la source principale
        main_src = None
        if prefer_size in sizes:
            main_src = webp_paths[sizes.index(prefer_size)]
        else:
            main_src = webp_paths[len(sizes) // 2]

        # Construire srcset
        srcset = ',\n          '.join(f"{webp_paths[i]} {sizes[i]}w" for i in range(len(sizes)))

        # Appliquer modifications
        img['src'] = main_src
        img['srcset'] = srcset
        img['loading'] = 'lazy'
        img['decoding'] = 'async'
        if not img.get('alt'):
            img['alt'] = ''

        changed = True
        logging.info('Modifié %s dans %s', src, path)

    if changed:
        if backup:
            bak = path.with_suffix(path.suffix + '.bak')
            shutil.copy2(path, bak)
            logging.debug('Backup créé: %s', bak)
        if not dry_run:
            path.write_text(str(soup), encoding='utf-8')
            logging.debug('Fichier écrit: %s', path)

    return changed


def find_html(root: Path) -> List[Path]:
    return sorted(root.rglob('*.html'))


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description='Met à jour les <img> pour utiliser les WebP optimisés')
    parser.add_argument('--root', '-r', type=Path, default=Path('.'), help='Dossier racine où chercher les .html (défaut: .)')
    parser.add_argument('--sizes', '-s', nargs='+', type=int, default=[480, 800, 1200], help='Tailles à utiliser dans le srcset')
    parser.add_argument('--prefer-size', '-p', type=int, default=800, help='Taille principale pour l`attribut src (défaut: 800)')
    parser.add_argument('--dry-run', action='store_true', help="Ne modifie pas les fichiers, affiche ce qui serait changé")
    parser.add_argument('--backup', action='store_true', help='Crée une sauvegarde .bak avant d écraser')
    parser.add_argument('--verbose', '-v', action='store_true', help='Logs détaillés')
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    logging.basicConfig(level=(logging.DEBUG if args.verbose else logging.INFO), format='[%(levelname)s] %(message)s')

    root = args.root
    if not root.exists():
        logging.error('Racine introuvable: %s', root)
        return 2

    sizes = sorted(set(args.sizes))
    html_files = find_html(root)
    if not html_files:
        logging.info('Aucun fichier .html trouvé sous %s', root)
        return 0

    total_changed = 0
    for f in html_files:
        changed = process_html_file(f, sizes, args.prefer_size, args.dry_run, args.backup)
        if changed:
            total_changed += 1

    logging.info('Terminé — fichiers modifiés: %d', total_changed)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
