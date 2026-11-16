# The Good Graph — site de Vanessa Santos

Site vitrine et boutique de **The Good Graph** (Vanessa Santos, stratégie de marque et direction créative, Dakar).
HTML, CSS et JavaScript sans framework ni dépendance npm. Hébergement prévu sur **Netlify**.

## Démarrer

```sh
sh build.sh                                        # assemble le site dans public/
python3 -m http.server 8000 --directory public     # puis ouvrir http://localhost:8000
```

`public/` est déjà généré dans ce livrable : on peut le déposer tel quel sur Netlify (glisser-déposer sur app.netlify.com/drop).

## Arborescence

```
src/index.html        la page entière : styles, contenu FR/EN, script
img/                  images optimisées pour le web (servies par le site)
build.sh              ajoute l'en-tête HTML complet et copie img/ dans public/
netlify.toml          build : sh build.sh — dossier publié : public/
public/               site assemblé, prêt à déployer (régénéré par build.sh, ignoré par git)
assets-sources/logos/ logos d'origine en PNG haute définition (non servis)
CLAUDE.md             notes de travail courtes sur le projet
.git/                 historique des modifications
```

### Pourquoi `src/index.html` n'a pas de `<!doctype>`, `<html>` ni `<head>`

La même source sert aussi d'aperçu sur claude.ai, qui ajoute lui-même ce squelette. `build.sh` le reconstruit pour la version publiée (charset, viewport, favicon, balises Open Graph). Si l'aperçu claude.ai ne sert plus, on peut fusionner l'en-tête dans `src/index.html` et supprimer l'étape de build.

## Fonctionnement

### Vues et adresses
Une seule page HTML. Les vues sont pilotées par l'ancre de l'adresse (fonction `route()`) :

| Ancre | Vue |
|---|---|
| `#accueil` (ou rien) | Accueil |
| `#apropos` | Accueil, défilé jusqu'à la section À propos |
| `#projets` | Page Projets avec filtres |
| `#boutique` | Page Boutique avec filtres |
| `#contact` | Page Contact et formulaire |
| `#simel`, `#sene-panier`, `#contanna` | Fiche projet plein écran par-dessus la vue courante |

### Contenu modifiable
Tout le contenu dynamique est dans le script en bas de `src/index.html` :

- **`PROJECTS`** : projets (titre, couleur de la marque, catégories et secteur FR/EN, description FR/EN, couverture, image d'ouverture, galerie).
  Galerie : `[fichier]` = demi-largeur, `"wide"` = pleine largeur, `"solo"` = centrée seule, `"logo"` = logo sur fond blanc, non agrandissable.
- **`PRODUCTS`** : produits de la boutique (titre, description, format, `price` en texte libre, `url` vers la page Chariow, `image` facultative dans `img/`, `tone` = couleur de l'aperçu dessiné quand il n'y a pas d'image).
- **`T`** : textes d'interface FR/EN générés par le script.

### Traduction FR / EN
Le français est dans le HTML. L'anglais est dans les attributs `data-en` (texte simple) ou `data-en-html` (texte avec balises, échappées). Le choix de langue est mémorisé dans `localStorage` (`tgg-lang`).

### Formulaire de contact — Netlify Forms
Le formulaire `name="contact"` porte `data-netlify="true"`, avec un champ piège anti-spam `bot-field`. L'envoi se fait en AJAX (POST vers `/`).
Après le premier déploiement : Netlify → Forms → activer la détection des formulaires si besoin, puis ajouter une **notification email vers thegoodgraph@gmail.com**.
**L'envoi n'a pas encore été testé en production.** À vérifier dès la mise en ligne.

### Boutique — Chariow
Le paiement et la livraison des fichiers se font sur **Chariow** (Wave et Orange Money confirmés par Vanessa). Le site n'encaisse rien : le bouton « Acheter » ouvre la page du produit sur Chariow.
**Les 4 produits actuels sont des exemples** (`example:true`, badge « Exemple », boutons désactivés). Il faut les remplacer par les vrais produits et leurs liens Chariow.

## Charte

| Rôle | Valeur |
|---|---|
| Bordeaux (logo) | `#8C2D44` |
| Bordeaux très foncé (cartes sombres) | `#2B0F18` |
| Rose poudré | `#F1D9DF` |
| Rose vif | `#FF8AB5` |
| Vert olive | `#556B2F` |
| Fond de page | `#F4EEF0` |

Polices (Google Fonts) : **Elms Sans** (texte), **Outfit** (titres, remplace Nourd qui n'est pas libre), **Gloock** (accents serif qui rappellent le logo).
Motifs récurrents : arches (portraits, services), étoile du logo ✦, cartes arrondies (`--r: 20px`).

## Images
`img/` contient des versions allégées (1 600 px maximum, JPEG qualité 80). Les logos y sont recolorés en bordeaux (`-wine`) et en rose poudré (`-blush`) sur fond transparent.
Les logos d'origine sont dans `assets-sources/logos/`. Vanessa conserve les photos en haute définition.

## Compatibilité et accessibilité
- `prefers-reduced-motion` coupe toutes les animations.
- Les apparitions au défilement utilisent `animation-timeline: view()`. Sans support (Firefox, anciens Safari), le contenu s'affiche simplement sans animation.
- `color-mix()` est utilisé pour quelques transparences (navigateurs récents).
- Focus clavier visible, visionneuse d'images au clavier (Échap, flèches), mise en page testée à 390 px et 1 440 px de large.

## Reste à faire
1. **Nom de domaine** : à acheter (ex. thegoodgraph.com ou .sn), puis à brancher dans Netlify.
2. **Open Graph** : `og:image` (dans `build.sh`) est en chemin relatif. Les réseaux sociaux exigent une URL absolue : la mettre à jour une fois le domaine connu, et ajouter `og:url`.
3. **Boutique** : remplacer les produits d'exemple par les vrais (nom, description, format, prix, visuel, lien Chariow).
4. **Formulaire** : tester un envoi réel sur Netlify et activer la notification email.
5. **Contenus en attente** : avis clients, fourchettes de budget pour le formulaire, années et clients des projets.
6. **Mentions légales et politique de confidentialité** : à prévoir (le formulaire collecte nom et email).
