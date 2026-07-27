# Ordre d’utilisation dans Figma Make

## Méthode recommandée — le prompt seul

1. Ouvrir un nouveau projet Figma Make.
2. Ouvrir le fichier `00_PROMPT_COMPLET_FIGMA_MAKE.md`.
3. Sélectionner tout le texte.
4. Copier le texte.
5. Coller le texte dans Figma Make.
6. Envoyer l’instruction.
7. Attendre la première génération.

Cette méthode ne nécessite pas le fichier ZIP.

## Si Figma Make demande les fichiers de code

Ajouter les fichiers individuellement dans cet ordre :

1. `package.json`
2. `vite.config.js`
3. `index.html`
4. `src/data.js`
5. `src/App.jsx`
6. `src/styles.css`
7. `src/main.jsx`

Le dossier `design-reference` est facultatif. Il contient uniquement la référence visuelle et la capture de contrôle.

## Instruction à envoyer après l’ajout des fichiers

```text
Utilise ces fichiers comme source canonique. Exécute l’application React/Vite
sans remplacer son architecture ni simplifier ses fonctionnalités.
Corrige uniquement les incompatibilités nécessaires à l’environnement Figma Make.
Conserve les filtres, la recherche, le quick view, la comparaison et le parcours
vendeur VIN → photos → génération IA → publication.
```

## Vérification

Tester dans cet ordre :

1. masquer puis rouvrir Filters ;
2. rechercher Honda ;
3. sélectionner SUV ;
4. ouvrir une fiche véhicule ;
5. ajouter et retirer un véhicule de Compare ;
6. ouvrir Sell your vehicle ;
7. saisir `2HKRW2H85NH201234` ;
8. continuer avec Use demo photos ;
9. sélectionner Generate listing ;
10. vérifier l’apparition de Publish listing.
