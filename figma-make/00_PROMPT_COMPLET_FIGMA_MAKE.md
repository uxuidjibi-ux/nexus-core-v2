# PROMPT PRINCIPAL À COPIER DANS FIGMA MAKE

Crée une application web responsive complète appelée **AutoCommerce**, destinée au marché automobile canadien. Il s’agit d’un MVP fonctionnel de marketplace automobile pour les acheteurs et les vendeurs professionnels.

Utilise **React**, une architecture claire par composants et des données locales de démonstration. L’application doit fonctionner immédiatement dans l’aperçu Figma Make, sans clé API et sans backend externe.

Ne crée pas une landing page marketing. Construis directement l’interface fonctionnelle du produit.

## Référence concurrentielle prioritaire

Utilise cette page Cars.ca comme référence fonctionnelle principale pour la profondeur des informations et la logique d’un inventaire automobile canadien :

```text
https://www.cars.ca/fr/voitures-a-vendre-vlp?vid=gAK5PhIOR2WAoQAMDrtpZA
```

Ne reproduis pas littéralement son identité visuelle, sa mise en page ou ses éléments propriétaires. Analyse et adapte uniquement les fonctions utiles :

- structure d’une page d’inventaire automobile ;
- recherche par localisation et rayon ;
- distinction neuf/occasion ;
- année, marque, modèle et version ;
- prix, financement et kilométrage ;
- badges de confiance liés au prix ;
- présence et disponibilité du rapport CARFAX ;
- informations du concessionnaire ;
- sauvegarde d’une annonce ;
- tri et pagination ;
- consultation rapide des détails ;
- affichage clair des résultats sans surcharger la navigation.

AutoCommerce doit aller plus loin avec :

- des filtres entièrement rétractables ;
- une navigation plus fluide et plus légère ;
- un aperçu véhicule intégré sans changement de page obligatoire ;
- une comparaison persistante de trois véhicules ;
- la vérification et le décodage du VIN ;
- un contrôle intelligent des photographies ;
- la génération assistée de descriptions ;
- un parcours de publication pensé pour les commerçants.

## 1. Vision du produit

AutoCommerce doit permettre :

- de rechercher facilement un véhicule au Canada ;
- de masquer ou afficher les filtres afin qu’ils ne dominent jamais l’écran ;
- de consulter rapidement les informations importantes d’un véhicule ;
- de sauvegarder et comparer jusqu’à trois véhicules ;
- de contacter un vendeur ou demander un financement ;
- de créer intelligemment une annonce avec un VIN, des photos et une description générée par IA ;
- de proposer ultérieurement un tableau de bord complet aux vendeurs professionnels.

L’expérience doit être plus simple, plus fluide et plus claire que les marketplaces automobiles traditionnelles.

## 2. Direction artistique obligatoire

Respecte précisément cette palette :

- fond principal : `#FFFFFF` ;
- navigation et texte principal : `#111111` ;
- rouge AutoCommerce : `#D71920` ;
- rouge foncé au survol : `#B60F15` ;
- succès et vérification VIN : `#198754` ;
- surface neutre : `#F6F7F8` ;
- surface secondaire : `#EEF0F2` ;
- bordure : `#DFE2E5` ;
- texte secondaire : `#626970`.

Typographie :

```css
font-family: "Helvetica Neue", Helvetica, Arial, sans-serif;
```

Principes visuels :

- interface premium, claire et professionnelle ;
- fond véritablement blanc, pas beige ou crème ;
- noir dominant dans la navigation ;
- rouge réservé aux actions principales et aux états sélectionnés ;
- vert réservé aux confirmations et validations ;
- espaces généreux et hiérarchie typographique forte ;
- bordures fines et ombres très légères ;
- angles de 8 à 12 pixels ;
- aucun gradient ;
- aucun glassmorphism ;
- aucune accumulation de petites cartes décoratives ;
- aucune statistique inventée ;
- aucun badge décoratif inutile ;
- icônes cohérentes de type Lucide.

## 3. Navigation principale

Crée une barre de navigation noire, compacte et fixe en haut de l’écran.

Elle doit contenir :

- logo texte `AUTOCOMMERCE`, avec `AUTO` en rouge et `COMMERCE` en blanc ;
- navigation : `Buy`, `Sell`, `Financing`, `Saved` ;
- sélecteur `EN / FR` ;
- accès `My account` ;
- bouton secondaire `Seller dashboard`.

L’onglet `Buy` doit être actif avec une fine ligne rouge sous le texte.

Sur mobile :

- afficher un bouton menu ;
- transformer la navigation en menu vertical ;
- conserver le logo visible ;
- réduire le bouton Seller dashboard à son icône.

## 4. Écran principal de recherche automobile

Construis une interface composée de trois zones :

1. panneau de filtres rétractable à gauche ;
2. résultats de recherche au centre ;
3. aperçu rapide du véhicule à droite.

### En-tête de la zone centrale

Afficher :

```text
CANADIAN MARKETPLACE
Find your next vehicle
6 curated vehicles near you
```

Ajouter à droite le bouton :

```text
Sell your vehicle
```

### Barre d’outils

Ajouter :

- un champ `Search make, model or keyword` ;
- une liste de classement :
  - Recommended ;
  - Price: low to high ;
  - Price: high to low ;
  - Lowest mileage ;
- un contrôle grille/liste ;
- un bouton `Filters` lorsque le panneau de filtres est masqué.

La recherche et le classement doivent fonctionner avec l’état React local.

## 5. Panneau de filtres rétractable

Afficher :

```text
REFINE RESULTS
Filters
Clear all
```

Inclure les champs suivants :

- Location : valeur par défaut `Toronto, ON` ;
- Make :
  - All makes ;
  - Honda ;
  - Toyota ;
  - Ford ;
  - Mazda ;
  - BMW ;
  - Tesla ;
- Body type :
  - All body types ;
  - SUV ;
  - Sedan ;
  - Truck ;
- Fuel type :
  - All fuel types ;
  - Gasoline ;
  - Electric ;
- Maximum price : curseur de 20 000 à 50 000 CAD.

Ajouter les boutons :

```text
Show [nombre] vehicles
Save this search
```

Fonctionnement obligatoire :

- le bouton X masque le panneau ;
- le bouton Filters le rouvre ;
- les filtres mettent immédiatement à jour les résultats ;
- Clear all réinitialise tous les filtres ;
- si aucun résultat ne correspond, afficher un état vide avec Reset search.

Sur mobile, le panneau devient une surface plein écran sous la navigation.

## 6. Données des véhicules

Créer six véhicules de démonstration :

1. 2022 Honda CR-V — EX-L AWD — 32 490 CAD — 188 CAD/mois — 45 120 km — Toronto, ON — SUV — Gasoline — VIN `2HKRW2H85NH201234`.
2. 2021 Toyota RAV4 — XLE AWD — 28 995 CAD — 168 CAD/mois — 78 450 km — Vancouver, BC — SUV — Gasoline.
3. 2019 Ford F-150 — XLT 4×4 — 29 900 CAD — 173 CAD/mois — 91 300 km — Calgary, AB — Truck — Gasoline.
4. 2020 Mazda CX-5 — GS AWD — 24 995 CAD — 145 CAD/mois — 62 210 km — Ottawa, ON — SUV — Gasoline.
5. 2021 BMW 3 Series — 330i xDrive — 35 900 CAD — 207 CAD/mois — 38 900 km — Mississauga, ON — Sedan — Gasoline.
6. 2023 Tesla Model 3 — Long Range AWD — 42 900 CAD — 248 CAD/mois — 24 600 km — Montréal, QC — Sedan — Electric.

Chaque objet véhicule doit contenir :

```ts
{
  id,
  year,
  make,
  model,
  trim,
  price,
  monthly,
  mileage,
  location,
  body,
  fuel,
  transmission,
  colour,
  vin,
  verified,
  image
}
```

Utiliser des images automobiles distantes de démonstration avec `object-fit: cover`. Prévoir une surface neutre si une image ne charge pas.

## 7. Cartes des véhicules

En mode grille, afficher trois colonnes sur grand écran, deux sur tablette et une sur mobile.

Chaque carte doit contenir :

- photographie ;
- bouton cœur ;
- état `VIN verified` lorsque disponible ;
- année, marque et modèle ;
- finition ;
- prix ;
- estimation mensuelle ;
- kilométrage ;
- emplacement ;
- bouton Compare ou Added.

Interactions :

- cliquer sur la carte ouvre le Quick view ;
- le cœur sauvegarde ou retire le véhicule ;
- Compare ajoute ou retire le véhicule ;
- maximum trois véhicules comparés ;
- la carte sélectionnée possède une bordure rouge légère.

Ajouter également un mode liste.

## 8. Aperçu rapide du véhicule

Créer un panneau droit `Quick view` qui possède son propre défilement vertical indépendant.

Comportement obligatoire :

- la liste des véhicules à gauche reste en place pendant la consultation ;
- l’en-tête du panneau reste visible ;
- le contenu du panneau peut défiler de haut en bas ;
- le panneau contient une véritable fiche véhicule longue et structurée ;
- le défilement de la fiche ne doit pas déplacer toute la page ;
- sur mobile, la fiche occupe toute la largeur et conserve son défilement interne.

Afficher :

- titre du véhicule ;
- bouton de fermeture ;
- grande galerie photographique ;
- flèches précédente/suivante ;
- compteur de photographies ;
- miniatures sélectionnables ;
- encadré vert `VIN verified and decoded` ;
- prix ;
- estimation mensuelle ;
- indicateur de positionnement du prix ;
- partage et sauvegarde ;
- bouton rouge `Contact seller` ;
- bouton secondaire `Request financing` ;
- section Overview avec kilométrage, état, carrosserie, carburant, moteur, passagers, transmission et numéro de stock ;
- description repliable avec Read more / Read less ;
- section Options en deux colonnes ;
- formulaire complet Contact the dealer ;
- section Vehicle details sous forme de tableau ;
- section Technical characteristics ;
- section Dealer information ;
- mentions sur les taxes, frais et exactitude des informations ;
- bouton Add to comparison ou Remove from comparison.

Sur les écrans intermédiaires et mobiles, ce panneau doit devenir un panneau superposé. Sur mobile, il doit occuper toute la largeur.

## 9. Barre de comparaison

Créer une barre fixe en bas lorsqu’au moins un véhicule est comparé.

Afficher :

- titre Compare ;
- compteur `[nombre]/3` ;
- miniature et nom de chaque véhicule ;
- bouton de suppression individuel ;
- emplacement Add vehicle ;
- bouton Clear all ;
- bouton Compare now.

Le bouton Compare now reste désactivé s’il y a moins de deux véhicules.

## 10. Parcours vendeur intelligent

Lorsque l’utilisateur clique sur Sell ou Sell your vehicle, ouvrir une fenêtre modale nommée :

```text
Smart listing studio
Sell your vehicle
```

Créer trois étapes réellement interactives.

### Étape 1 — Decode VIN

Afficher :

```text
Start with the VIN
AutoCommerce decodes the technical details so you do not have to enter them manually.
17-character VIN
Decode vehicle
```

Le bouton reste désactivé tant que le VIN est trop court.

La validation peut être simulée localement.

### Étape 2 — Add photos

Afficher une confirmation :

```text
2022 Honda CR-V EX-L AWD identified
```

Créer une zone de téléchargement :

```text
Upload vehicle photos
Drag and drop or select up to 24 images
AI quality check, blur detection and smart ordering included
```

Ajouter le bouton :

```text
Use demo photos
```

Le téléchargement et l’analyse peuvent être simulés.

### Étape 3 — Generate listing

Afficher :

```text
AI Listing Assistant
Vehicle data and 12 photos are ready. Generate a transparent, factual description in seconds.
Generate listing
```

Après activation, générer localement :

```text
2022 Honda CR-V EX-L AWD — one-owner, versatile and refined

Well-equipped Canadian SUV with leather interior, all-wheel drive,
heated seats and advanced safety technology. VIN details verified
by AutoCommerce.
```

Afficher ensuite le bouton :

```text
Publish listing
```

## 11. Accessibilité et responsive

Obligatoire :

- HTML sémantique ;
- labels accessibles ;
- textes alternatifs pour les images ;
- focus clavier visible ;
- contrastes compatibles WCAG ;
- commandes atteignables au clavier ;
- boutons d’icônes avec aria-label ;
- prise en charge de `prefers-reduced-motion` ;
- aucun débordement horizontal sur mobile ;
- zones tactiles suffisamment grandes.

Points de rupture recommandés :

```css
1320px
1050px
820px
580px
```

## 12. Architecture du code

Structurer l’application avec ces composants :

```text
App
├── Header
├── Filters
│   └── SelectField
├── Inventory
│   └── VehicleCard
├── VehicleDetail
├── CompareBar
└── SellModal
```

Séparer les données des véhicules de l’interface.

Utiliser :

- React ;
- `useState` ;
- `useMemo` ;
- composants fonctionnels ;
- CSS responsive ;
- `lucide-react` pour les icônes si disponible.

Ne pas utiliser de backend, de base de données ou de clé API dans cette version.

## 13. Critères de réussite

Avant de considérer l’application terminée, vérifier :

1. la recherche filtre les véhicules ;
2. Make, Body type, Fuel type et Maximum price fonctionnent ;
3. Filters peut être masqué et rouvert ;
4. Grid/List fonctionne ;
5. Save fonctionne ;
6. Quick view s’ouvre et se ferme ;
7. Compare accepte au maximum trois véhicules ;
8. la barre Compare apparaît et se met à jour ;
9. le parcours vendeur atteint Publish listing ;
10. l’application reste utilisable sur mobile ;
11. aucun contrôle principal n’est statique ;
12. aucune landing page marketing n’est ajoutée.

Génère maintenant l’intégralité de l’application et affiche directement l’aperçu fonctionnel.
