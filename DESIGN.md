# DESIGN.md — à remplir avant de produire les écrans

Ce fichier est la source de vérité produit. Claude le lit avant d'écrire le moindre HTML.
Tant qu'une section est vide, l'écran correspondant ne peut pas être fidèle : remplis d'abord.

## 1. Produit

- **Nom :** …
- **En une phrase :** …
- **Plateforme :** iOS, mockups statiques 390 × 844
- **Ton visuel :** (ex. sobre et dense type Revolut / chaleureux et aéré type Headspace)

## 2. Utilisateur

- **Persona principal :** prénom, âge, contexte d'usage
- **Ce qu'il vient faire dans l'app :** …
- **Moment d'usage :** (matin, en déplacement, 30 s par session…)

## 3. Écrans à produire

| # | Fichier | Écran | Réf. dans `refs/` | État |
|---|---|---|---|---|
| 1 | `screens/onboarding-1.html` | … | `refs/…png` | à faire |
| 2 | `screens/home.html` | … | `refs/…png` | à faire |

## 4. Données réalistes à réutiliser

Liste ici les vrais noms, montants, dates, libellés utilisés partout dans les mockups, pour
qu'ils soient cohérents d'un écran à l'autre. Exemple :

- Utilisateur : Léa Meier, Zurich
- Solde : CHF 2 847.30
- Transactions : Migros CHF 43.20 · SBB CHF 12.00 · Starbucks CHF 6.80

## 5. Direction artistique

- **Couleur primaire :** …
- **Police :** … (système par défaut si non précisé)
- **Rayons :** … px
- **Références visuelles :** ce qui dans `refs/` fait autorité, et sur quel aspect
  (ex. « `refs/revolut-home.png` pour la densité, `refs/linear-app.png` pour la typo »)
