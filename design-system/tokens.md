# Design tokens

À remplir depuis `DESIGN.md` §5 et les images de `refs/`. Tout écran réutilise ces valeurs.
Si un token manque, on l'ajoute **ici d'abord**, on n'invente pas une valeur dans un écran.

## Couleurs

| Token | Classe Tailwind | Usage |
|---|---|---|
| primaire | `indigo-600` | actions, accents |
| texte fort | `neutral-900` | titres, valeurs |
| texte faible | `neutral-500` | libellés, secondaire |
| bordure | `neutral-200` | cartes, séparateurs |
| fond | `white` | fond d'écran |

## Typographie

| Rôle | Taille / graisse | Classe |
|---|---|---|
| titre écran | 34px bold | `text-[34px] font-bold tracking-tight` |
| section | 22px semibold | `text-[22px] font-semibold` |
| corps | 16px regular | `text-[16px]` |
| libellé | 14px regular | `text-[14px] text-neutral-500` |
| micro | 13px regular | `text-[13px] text-neutral-400` |

## Espacement & formes

- Gouttière horizontale de l'écran : `px-6` (24px)
- Rayon carte : `rounded-2xl` (16px)
- Hauteur bouton principal : `h-[54px]`
- Status bar : 54px · home indicator : 34px

## Chrome iOS

Status bar et home indicator sont copiables depuis `screens/test.html` (SVG inline, pas d'image).
