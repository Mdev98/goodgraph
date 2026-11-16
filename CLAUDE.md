# The Good Graph — site portfolio de Vanessa Santos

Site statique (accueil, projets, boutique, contact en une seule page HTML, vues pilotées par l'ancre), hébergé sur Netlify (build : `sh build.sh`, dossier publié : `public/`). Le formulaire de contact utilise Netlify Forms (`data-netlify="true"`) : les demandes arrivent dans l'onglet Forms du site Netlify.

- `src/index.html` : toute la page (styles, contenu FR/EN, script). Les projets sont dans le tableau `PROJECTS` du script.
- `img/` : images optimisées (JPEG ~1600 px, qualité 80). Les logos sont recolorés en bordeaux (`-wine`) et rose poudré (`-blush`).
- `build.sh` : ajoute l'en-tête HTML complet et copie les images dans `public/`.
- La même source sert d'aperçu en Artifact claude.ai : ne pas y ajouter de `<!doctype>`, `<html>`, `<head>` ou `<body>`.

Palette : bordeaux #8C2D44, rose poudré #F1D9DF, rose vif #FF8AB5, vert olive #556B2F. Polices : Elms Sans (texte), Outfit (titres, à la place de Nourd) et Gloock (accents serif). Documentation complète pour un développeur : README.md.

Ajouter un projet : redimensionner les images dans `img/`, ajouter une entrée à `PROJECTS` (titre, catégories et description en FR et EN, images, couverture), puis pousser sur `main`. Netlify redéploie tout seul.

Boutique : les produits sont dans le tableau `PRODUCTS` du script (titre, description FR/EN, format, `price` en texte, `url` vers la page du produit sur Chariow (paiement Wave et Orange Money), `image` facultative dans `img/`). Les quatre produits actuels sont des exemples (`example:true`, badge « Exemple ») à remplacer par les vrais. Sans `url`, le bouton affiche « Bientôt disponible ».
