#!/bin/sh
# Assemble le site publiable dans public/ : ajoute l'en-tête HTML complet autour de src/index.html.
set -e
cd "$(dirname "$0")"
rm -rf public && mkdir -p public
cp -r img public/img
{
  printf '%s\n' '<!doctype html>' '<html lang="fr">' '<head>' \
    '<meta charset="utf-8">' \
    '<meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">' \
    '<link rel="icon" type="image/png" href="img/monogram-wine.png">' \
    '<meta property="og:title" content="The Good Graph — Vanessa Santos">' \
    '<meta property="og:description" content="Stratégie de marque et direction créative, Dakar.">' \
    '<meta property="og:image" content="img/simel-7.jpg">'
  # le <title>, les <meta>/<link> et le <style> de la source restent en tête de document
  sed -n '1,/<\/style>/p' src/index.html
  printf '%s\n' '</head>' '<body>'
  sed '1,/<\/style>/d' src/index.html
  printf '%s\n' '</body>' '</html>'
} > public/index.html
echo "public/ prêt : $(du -sh public | cut -f1)"
