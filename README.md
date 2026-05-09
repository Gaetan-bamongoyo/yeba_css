# Flexbox Learning Game

Un mini-jeu web interactif conçu pour aider les débutants à apprendre et maîtriser **CSS Flexbox**. À la manière de *Flexbox Froggy*, l'utilisateur doit écrire du code CSS pour déplacer un élément et atteindre une cible.

## 🚀 Fonctionnalités

- **Éditeur de code intégré** : Utilise **CodeMirror** (via CDN) pour offrir une véritable expérience de développement avec coloration syntaxique et numéros de ligne.
- **Retour visuel en temps réel** : Le CSS tapé dans l'éditeur s'applique instantanément à l'aire de jeu sans avoir besoin de recharger la page.
- **Validation automatique** : Le jeu détecte automatiquement quand le carré atteint sa cible (superposition parfaite) et déclenche une animation de victoire (changement de couleur en vert avec un effet lumineux).
- **Design moderne** : Interface épurée et professionnelle avec un effet de grille en perspective dans la zone de jeu.

## 📂 Structure du projet

Le projet est conçu pour être simple et ultra léger, sans dépendances complexes (pas de Node.js, pas de framework JavaScript ou CSS).

```text
e_learning/
├── index.html          # Structure de la page, import de CodeMirror et logique JavaScript
└── assets/
    └── style.css       # Design de l'interface utilisateur et de l'aire de jeu
```

### Détail des fichiers

#### `index.html`
C'est le cœur de l'application. Il contient :
1. **La structure UI** : L'en-tête de navigation principal, le panneau de jeu (`.game-view-panel`) et le panneau d'édition de code (`.code-editor-panel`).
2. **L'éditeur CodeMirror** : La configuration pour transformer le simple `<textarea>` en un véritable éditeur de code.
3. **Le moteur de jeu (JavaScript intégré)** : 
   - La fonction `applyCSS()` récupère le code saisi dans l'éditeur et l'injecte dans une balise `<style id="dynamic-styles">`.
   - La fonction `checkWin()` utilise la méthode `getBoundingClientRect()` pour vérifier mathématiquement si le joueur a réussi à superposer l'élément (`.item`) sur la cible (`.target`). Si c'est le cas, la classe `.success` est ajoutée.

#### `assets/style.css`
Ce fichier gère toute l'esthétique du jeu :
- **Variables CSS** (`:root`) : Pour une gestion centralisée et facile des couleurs (vert d'accentuation, fonds gris, couleurs du code, etc.).
- **Mise en page UI** : Utilisation de Flexbox pour aligner les deux grands panneaux de manière réactive.
- **Aire de jeu** : Création d'un arrière-plan en grille grâce à des gradients radiaux et des masques CSS (`mask-image`) pour donner un effet de profondeur/perspective.
- **Animations** : Transition fluide du carré lorsqu'il se déplace sur l'écran et style d'état spécifique (`.success`) lorsqu'il atteint sa cible.

## 🛠️ Comment lancer le projet

1. Clonez ce dépôt ou téléchargez le dossier `e_learning`.
2. Ouvrez simplement le fichier `index.html` dans n'importe quel navigateur web moderne (Chrome, Firefox, Safari, Edge). Aucune installation de serveur n'est requise.
3. Dans l'éditeur de code à droite, tapez du CSS valide. Par exemple pour le niveau 1 :
   ```css
   #container {
     display: flex;
     justify-content: center;
     align-items: center;
   }
   ```
4. Observez le carré bouger en temps réel. S'il se superpose parfaitement, c'est gagné !

## 🔮 Pistes d'améliorations futures (Roadmap)

Si vous souhaitez étendre ce projet, voici quelques idées :
- **Système de niveaux complet** : Créer un tableau en JavaScript contenant les objectifs de plusieurs niveaux et les charger dynamiquement.
- **Bouton Suivant** : Faire apparaître un bouton "Niveau Suivant" uniquement lorsque la classe `.success` est validée.
- **Support de nouvelles propriétés** : Ajouter des obstacles ou des cibles multiples pour faire travailler `flex-direction`, `flex-wrap` ou `align-self`.
# yeba_css
