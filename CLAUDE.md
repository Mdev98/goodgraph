# The Good Graph — site portfolio de Vanessa Santos

Site statique (accueil, projets, boutique, contact en une seule page HTML, vues pilotées par l'ancre), hébergé sur **Vercel** (fichier `index.html` à la racine, publié tel quel, pas de build). Le formulaire de contact ne peut pas envoyer de données sur Vercel : il ouvre la messagerie du visiteur avec le message déjà rédigé vers thegoodgraph@gmail.com. Les demandes arrivent donc dans la boîte mail de Vanessa.

- `index.html` : toute la page (styles, contenu FR/EN, script). Les projets sont dans le tableau `PROJECTS` du script.
- `img/` : images optimisées (JPEG ~1600 px, qualité 80). Les logos sont recolorés en bordeaux (`-wine`) et rose poudré (`-blush`).
- Le fichier contient l'en-tête HTML complet : pas besoin de build.

Palette : bordeaux #8C2D44, rose poudré #F1D9DF, rose vif #FF8AB5, vert olive #556B2F. Polices : Elms Sans (texte), Outfit (titres, à la place de Nourd) et Gloock (accents serif). Documentation complète pour un développeur : README.md.

Ajouter un projet : redimensionner les images dans `img/`, ajouter une entrée à `PROJECTS` (titre, catégories et description en FR et EN, images, couverture), puis pousser sur `main`. Vercel redéploie tout seul en une à deux minutes.

Boutique : les produits sont dans le tableau `PRODUCTS` du script (titre, description FR/EN, format, `price` en texte, `url` vers la page du produit sur Chariow (paiement Wave et Orange Money), `image` facultative dans `img/`). Les quatre produits actuels sont des exemples (`example:true`, badge « Exemple ») à remplacer par les vrais. Sans `url`, le bouton affiche « Bientôt disponible ».
