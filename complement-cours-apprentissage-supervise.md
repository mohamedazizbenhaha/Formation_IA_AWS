# Document Complémentaire — Apprentissage Supervisé : Classification et Régression
### Notes de cours approfondies, slide par slide

> Ce document accompagne le support de présentation *"Apprentissage Supervisé — Classification et Régression"*. Il ne remplace pas les slides : il les **approfondit**, slide par slide, avec des explications détaillées, des métaphores, des exemples concrets, des pièges courants à éviter, et des mini-exercices corrigés. Les mathématiques ne sont détaillées que lorsque c'est réellement nécessaire à la compréhension — l'objectif est l'intuition, pas la démonstration formelle.

---

## Slide 1 — Page de Titre

### Ce que la slide annonce
Le cours couvre l'apprentissage supervisé à travers ses deux grandes familles : la classification et la régression, dans le cadre plus large du Machine Learning et de la Data Science.

### Ce qu'il faut comprendre avant même de commencer

L'apprentissage supervisé n'est **pas tout le Machine Learning** — c'est l'une de ses trois grandes familles (avec l'apprentissage non-supervisé et l'apprentissage par renforcement, que ce cours ne couvre volontairement pas). Il représente cependant la famille la **plus utilisée en pratique** dans l'industrie aujourd'hui : la grande majorité des systèmes d'IA appliqués en entreprise (détection de fraude, scoring de crédit, diagnostic assisté, recommandation) reposent sur de l'apprentissage supervisé.

**Métaphore d'ouverture — l'élève et le corrigé :**
Imaginez un élève qui prépare un examen en s'entraînant sur des annales **avec leurs corrigés**. Il voit une question, essaie une réponse, compare avec le corrigé, ajuste sa méthode, et recommence sur une nouvelle annale. C'est exactement le principe de l'apprentissage supervisé : le modèle voit des exemples (les "questions"), fait une prédiction, compare avec la bonne réponse connue (le "corrigé"), et ajuste ses paramètres internes. La différence avec l'apprentissage non-supervisé serait un élève à qui on donnerait un tas de photos à trier par similarité, **sans jamais lui dire** ce qu'elles représentent.

Gardez cette image de "l'élève et le corrigé" en tête : elle reviendra pour expliquer presque tous les concepts qui suivent.

---

## Slide 2 — Plan du Cours

### Structure pédagogique du cours

Le plan suit une logique en quatre mouvements qu'il est utile de visualiser dès maintenant :

1. **Fondations** (Ch. 1-2) : qu'est-ce que l'apprentissage supervisé, et sa première grande bifurcation (classification vs régression).
2. **Approfondissement par famille** (Ch. 3-4) : chaque famille explorée en détail, avec ses algorithmes propres.
3. **Évaluation et diagnostic** (Ch. 5-6) : comment savoir si un modèle est *réellement* bon, et pourquoi il peut échouer.
4. **Application pratique** (Ch. 7-8) : comment choisir la bonne méthode face à un problème réel.

**Pourquoi cet ordre est important pédagogiquement :** on ne peut pas comprendre les métriques d'évaluation (Ch. 5) avant de comprendre ce qu'on évalue (Ch. 3-4), et on ne peut pas comprendre le compromis biais-variance (Ch. 6) sans avoir déjà vu concrètement des algorithmes simples et complexes (Ch. 3-4). Gardez cette carte mentale : chaque nouveau chapitre s'appuie explicitement sur le précédent.

### Mini-exercice
Avant de continuer, essayez de répondre sans relire : quelle est, selon vous, la différence fondamentale entre "classification" et "régression" ? Écrivez une phrase.

### Correction
La classification prédit une **catégorie** parmi un ensemble fini de choix (ex : spam ou non-spam). La régression prédit une **valeur numérique continue** qui peut prendre, en théorie, une infinité de valeurs (ex : un prix, une température). Si votre réponse spontanée tournait autour de "l'un donne un texte, l'autre un nombre", vous êtes sur la bonne piste — nous allons rendre cette intuition rigoureuse dans la slide suivante.

---

## Slide 3 — Chapitre 1 : Qu'est-ce que l'Apprentissage Supervisé ?

### Décortiquer la définition fondamentale

> *"L'apprentissage supervisé est une méthode d'apprentissage automatique où un modèle apprend à partir de données étiquetées — des données d'entrée pour lesquelles la sortie correcte est déjà connue."*

Chaque mot de cette définition compte :

- **"Données étiquetées"** : c'est le mot-clé absolu. Une donnée étiquetée est une paire **(entrée, sortie connue)**. Sans étiquette, il n'y a pas de "corrigé", et donc pas d'apprentissage supervisé possible.
- **"Modèle apprend"** : le modèle n'est pas programmé avec des règles explicites (`si email contient "gratuit" alors spam`), il **découvre** ces règles à partir de milliers d'exemples.
- **"Fonction de mapping"** : le modèle cherche mathématiquement une fonction `f` telle que `f(entrée) ≈ sortie_connue` pour toutes les données d'entraînement, et qui **généralise** correctement à de nouvelles entrées jamais vues.

**Métaphore approfondie — le traducteur qui apprend sur le tas :**
Imaginez un traducteur qui apprend une nouvelle langue uniquement à partir de milliers de phrases déjà traduites par des humains (les paires entrée-sortie). Après avoir vu suffisamment de paires "Bonjour" → "Hello", "Merci" → "Thank you", il commence à saisir des **patterns** (grammaire, vocabulaire, structure) qui lui permettent de traduire une phrase **qu'il n'a jamais vue** auparavant. Il n'a pas mémorisé un dictionnaire figé : il a appris une fonction de mapping généralisable. C'est exactement ce qu'on demande à un modèle supervisé.

### Le processus en 3 étapes — regard critique et approfondi

**1) Entraînement (Training) — 80% des données**
Le modèle ajuste ses paramètres internes pour minimiser l'écart entre ses prédictions et les vraies étiquettes, sur ces données précisément. C'est ici qu'intervient la **fonction de coût** (ou fonction de perte) : une formule qui quantifie "à quel point le modèle se trompe". Plus la valeur de cette fonction est basse, plus le modèle colle aux données d'entraînement.

**2) Validation**
Étape souvent sous-estimée par les débutants : on utilise un sous-ensemble de données **différent** de l'entraînement pour ajuster les **hyperparamètres** (des réglages du modèle qu'on ne peut pas apprendre directement à partir des données, comme la profondeur maximale d'un arbre de décision). C'est un peu comme un examen blanc : on l'utilise pour ajuster sa méthode de révision, mais ce n'est pas encore l'examen final.

**3) Test — 20% des données, jamais vues**
Ici se joue la vraie question : **le modèle a-t-il appris des patterns généraux, ou a-t-il simplement mémorisé les données d'entraînement ?** C'est la capacité de **généralisation** — le concept le plus important de tout ce cours, sur lequel repose littéralement toute la discipline du Machine Learning.

> ⚠️ **Piège fréquent chez les débutants :** évaluer son modèle sur les mêmes données que celles utilisées pour l'entraîner. Cela revient à donner à un élève, le jour de l'examen, exactement les mêmes questions que celles de ses fiches de révision — il aura l'air brillant sans que cela prouve qu'il a réellement compris quoi que ce soit. **Ne jamais évaluer un modèle sur des données qu'il a vues pendant l'entraînement.**

**Optimisation par descente de gradient — intuition, sans les maths :**
La "descente de gradient" est simplement la méthode par laquelle le modèle ajuste progressivement ses paramètres pour réduire son erreur, un peu petit pas après l'autre. Imaginez que vous êtes dans le brouillard sur une colline, et que vous voulez descendre au point le plus bas sans rien voir : vous tâtez le sol du pied, et vous avancez dans la direction qui descend le plus. Répété des milliers de fois, cela vous mène (progressivement) au point le plus bas.

### Mini-exercice
Un data scientist entraîne un modèle de diagnostic médical. Il obtient 99% de précision sur les données d'entraînement, mais seulement 62% sur les données de test. Que s'est-il probablement passé, et quelle étape du processus a été mal gérée ?

### Correction
Il s'agit très probablement d'un cas de **surapprentissage (overfitting)** : le modèle a mémorisé les particularités (voire le bruit) des données d'entraînement plutôt que d'apprendre des patterns généralisables. L'écart énorme entre 99% (train) et 62% (test) est le signal classique de ce problème — nous détaillerons ce diagnostic en profondeur au Chapitre 6 (slide 11). Ce qui a été "mal géré" ici, ce n'est pas forcément une étape unique, mais l'absence de vigilance sur la généralisation — potentiellement un modèle trop complexe pour la quantité de données disponible, ou une phase de validation insuffisamment exploitée pour ajuster les hyperparamètres avant le test final.

---

## Slide 4 — Chapitre 2 : Les Deux Piliers — Classification vs Régression

### Approfondissement du tableau comparatif

La distinction entre classification et régression n'est **pas une question de difficulté** ou de sophistication de l'algorithme — c'est une question de **nature de la variable à prédire** (la "target" ou variable cible). C'est la toute première question à se poser face à un nouveau problème de Machine Learning, avant même de penser à un algorithme.

**Test rapide et fiable pour trancher :** posez-vous la question — *"Est-ce que ça a un sens de faire une moyenne de mes valeurs cibles ?"*
- Prix immobiliers : la moyenne de 200 000€ et 300 000€ (= 250 000€) a un sens → **régression**.
- Spam/Non-Spam : la "moyenne" de "Spam" et "Non-Spam" n'a strictement aucun sens → **classification**.

**Métaphore — le juge vs le comptable :**
Un **juge** classe un dossier dans une catégorie prédéfinie (coupable/non-coupable) — c'est une classification. Un **comptable** calcule un montant précis, potentiellement n'importe quelle valeur dans une plage continue (le montant d'un remboursement) — c'est une régression. Le juge ne "calcule" pas une culpabilité à 63,4% de la même façon qu'un comptable calcule un montant (même si certains modèles de classification donnent des probabilités, la décision finale reste discrète : une catégorie tranchée).

### Nuance importante souvent oubliée dans les cours d'introduction

Certains problèmes sont **à la frontière** des deux catégories, et il est important de le savoir dès maintenant :
- Un problème de classification peut être construit à partir d'un problème de régression sous-jacent en "découpant" les valeurs continues en tranches (ex : transformer une température continue en catégories "froid / tempéré / chaud"). C'est ce qu'on appelle la **discrétisation**.
- Inversement, un modèle de classification produit souvent une **probabilité continue** en interne (entre 0 et 1) avant d'être converti en catégorie discrète via un seuil (souvent 0.5) — nous y reviendrons en détail à la slide 6 avec la régression logistique.

Cette zone grise n'est pas une contradiction du cours : elle montre que le choix classification/régression dépend souvent de **comment vous formulez le problème métier**, pas d'une loi de la nature immuable.

### Mini-exercice
Pour chacun des cas suivants, indiquez s'il s'agit de classification ou de régression, et justifiez en une phrase avec le "test de la moyenne" :
1. Prédire si un client va résilier son abonnement (churn) ce mois-ci.
2. Prédire le nombre de clients qui vont résilier leur abonnement ce mois-ci.
3. Prédire la note d'un film sur 5 étoiles (1,2,3,4 ou 5 étoiles uniquement, jamais de demi-étoiles).

### Correction
1. **Classification** (binaire) — la sortie est "oui" ou "non", faire une moyenne n'a pas de sens.
2. **Régression** — c'est un compte (un nombre de clients), la moyenne entre "3 clients" et "7 clients" (= 5) a parfaitement de sens.
3. Cas intéressant et volontairement piégeux : c'est généralement traité comme une **classification multi-classes** (5 catégories ordonnées) en pratique, bien que ce soit conceptuellement une variable ordinale à mi-chemin entre les deux — un excellent exemple de la "zone grise" évoquée plus haut.

---

## Slide 5 — Chapitre 3 : La Classification — Concepts et Applications

### La frontière de décision, en profondeur

Le concept central de cette slide est la **frontière de décision** : c'est la ligne (ou surface, en plus de deux dimensions) que le modèle "trace" dans l'espace des caractéristiques (features) pour séparer les classes.

**Métaphore — la clôture dans un champ :**
Imaginez un champ où les moutons blancs paissent d'un côté et les moutons noirs de l'autre. La frontière de décision est la **clôture** que vous installeriez pour séparer les deux troupeaux, en vous basant sur leur position actuelle. Si les moutons sont bien regroupés par couleur dans deux zones distinctes, une clôture **droite** (frontière linéaire) suffit. Si les deux troupeaux sont mélangés dans des motifs complexes (un peu de blanc ici, un peu de noir là), il vous faudra une clôture **très sinueuse** (frontière non-linéaire complexe) pour bien les séparer — au risque, si elle est trop sinueuse, de simplement "épouser" chaque mouton individuellement plutôt que de capturer une vraie séparation générale (ce qui nous ramènera au surapprentissage, Ch. 6).

**Les trois types de frontières évoqués sur la slide, avec exemples concrets :**
- **Linéaire** : une droite (ou un plan en plus haute dimension) sépare les classes. Exemple : séparer des tumeurs bénignes/malignes sur la seule base de leur taille, si les grosses tumeurs sont presque toujours malignes.
- **Non-linéaire** : une courbe sépare les classes. Exemple : classifier des transactions comme frauduleuses selon une combinaison complexe de montant, heure, et localisation, où la relation n'est pas une simple droite.
- **Complexe/irrégulière** : la frontière suit des détails très fins des données, souvent le signe qu'un modèle est en train de mémoriser du bruit plutôt que d'apprendre une vraie tendance (à surveiller de près — lien direct avec le Ch. 6).

### Classification binaire vs multi-classes — pourquoi cette distinction structure le choix d'algorithme

- **Binaire** : deux classes mutuellement exclusives (Oui/Non, Spam/Non-Spam). C'est le cas le plus simple, et beaucoup d'algorithmes (comme la régression logistique dans sa forme la plus simple) sont nativement conçus pour ce cas.
- **Multi-classes** : plus de deux classes (Chat/Chien/Oiseau). Certains algorithmes gèrent cela nativement (arbres de décision, forêts aléatoires), d'autres nécessitent des adaptations techniques (comme entraîner plusieurs classificateurs binaires "un contre tous").

### Mini-exercice
Un système de tri postal doit classer des colis en 4 catégories de poids : "léger", "moyen", "lourd", "très lourd". Est-ce une classification binaire, multi-classes, ou un cas particulier ? Décrivez en une phrase à quoi pourrait ressembler la frontière de décision dans ce cas si l'unique feature utilisée est le poids réel en kg.

### Correction
C'est une **classification multi-classes** (4 catégories). Puisque la seule feature est le poids (une seule dimension), la frontière de décision ne serait pas une courbe complexe mais simplement une série de **seuils** sur une ligne numérique (par exemple : <2kg = léger, 2-5kg = moyen, 5-15kg = lourd, >15kg = très lourd). C'est un excellent exemple montrant que même une classification multi-classes peut avoir une frontière de décision extrêmement simple si le problème sous-jacent est simple.

---

## Slide 6 — Algorithmes de Classification

### Vue d'ensemble pédagogique avant le détail

Cette slide présente six algorithmes très différents dans leur logique interne. Plutôt que de les mémoriser isolément, organisez-les mentalement en trois familles :

- **Famille "frontière mathématique"** : Régression Logistique, SVM → cherchent une équation qui sépare les classes.
- **Famille "règles de décision"** : Arbres de Décision, Forêts Aléatoires → posent une série de questions Oui/Non.
- **Famille "comparaison de proximité/probabilité"** : KNN, Naive Bayes → comparent un nouveau point à des références connues.

### 1. Régression Logistique — approfondissement

Malgré son nom contenant "régression", c'est bien un algorithme de **classification**. Le nom vient du fait qu'il repose sur une régression mathématique sous-jacente, dont le résultat est ensuite transformé.

**La fonction sigmoïde, expliquée sans jargon :** la formule `P(Y=1|X) = 1/(1+e⁻ᶻ)` a l'air intimidante, mais son rôle est simple : elle prend n'importe quel nombre (négatif, positif, très grand, très petit) et le "compresse" toujours dans une plage entre 0 et 1 — ce qui en fait naturellement une **probabilité**. C'est comme un entonnoir qui aplatit n'importe quelle quantité en un pourcentage interprétable.

**Métaphore :** imaginez un thermomètre de confiance qui, peu importe à quel point les preuves sont accablantes ou faibles, affiche toujours un chiffre entre 0% et 100% — jamais -30% ni 150%. C'est le rôle exact de la fonction sigmoïde.

**Forces/limites en contexte réel :** interprétable signifie qu'on peut littéralement dire "chaque euro supplémentaire de revenu augmente la probabilité d'accepter le prêt de X%" — une information précieuse pour un banquier qui doit justifier une décision. C'est pourquoi ce modèle reste très utilisé en finance et en assurance malgré son ancienneté : la réglementation exige souvent des décisions explicables.

### 2. SVM (Support Vector Machines) — approfondissement

**La marge maximale, en métaphore :** imaginez que vous devez tracer une route entre deux villages ennemis (les deux classes), et que vous voulez que cette route soit **la plus large possible** pour éviter tout conflit aux frontières. Le SVM ne cherche pas juste "une" frontière qui sépare les classes, il cherche **la frontière qui maximise la distance** avec les points les plus proches de chaque classe — ces points critiques s'appellent les **vecteurs de support** (d'où le nom de l'algorithme).

**Les "kernels" pour la non-linéarité — intuition sans les maths :** si les deux classes ne sont pas séparables par une droite dans leur espace d'origine, un kernel **projette** les données dans un espace de dimension supérieure où elles deviennent (souvent) séparables linéairement. Métaphore : imaginez des points rouges à l'intérieur d'un cercle et des points bleus tout autour — impossible de les séparer par une ligne droite sur une feuille plate. Mais si vous "soulevez" les points rouges du centre (comme si vous poussiez le centre d'une nappe vers le haut), ils se retrouvent séparés des points bleus par un simple plan horizontal. C'est cette astuce géométrique que réalise mathématiquement un kernel.

### 3. Arbres de Décision — approfondissement

**Métaphore — le questionnaire médical :** un arbre de décision fonctionne exactement comme un médecin qui pose une série de questions Oui/Non pour arriver à un diagnostic : "Le patient a-t-il de la fièvre ? Si oui, a-t-il aussi une toux ? Si oui..." Chaque question est un **nœud**, chaque diagnostic final est une **feuille**.

**Le "gain d'information" en intuition :** l'algorithme choisit, à chaque étape, la question qui **sépare le mieux** les données restantes en groupes les plus "purs" possible (le plus homogènes en termes de classe). C'est un peu comme trier un tas de cartes mélangées : vous poserez d'abord la question qui vous permet de séparer le tas en deux paquets les plus homogènes possible (par exemple, séparer d'abord par couleur avant de séparer par valeur, si la couleur est plus discriminante).

**Pourquoi l'instabilité est un vrai défaut pratique :** un tout petit changement dans les données d'entraînement peut faire choisir une question de découpage complètement différente au sommet de l'arbre, ce qui change en cascade toute la structure de l'arbre. C'est précisément la raison d'être des forêts aléatoires (point suivant).

### 4. Forêts Aléatoires (Random Forest) — approfondissement

**Métaphore — le jury plutôt qu'un juge unique :** au lieu de faire confiance à un seul arbre de décision (potentiellement instable et biaisé par les particularités de son entraînement), on entraîne des **centaines d'arbres différents**, chacun sur un sous-échantillon aléatoire différent des données et des features, puis on prend un **vote majoritaire**. Comme un jury de 100 personnes rend généralement un verdict plus robuste qu'un seul juge influençable, la moyenne (ou le vote) de nombreux arbres "imparfaits" produit une prédiction globalement plus stable et précise que n'importe lequel des arbres pris isolément. Ce principe s'appelle **l'apprentissage d'ensemble (ensemble learning)**.

### 5. K-Nearest Neighbors (KNN) — approfondissement

**Métaphore — "dis-moi qui sont tes voisins" :** pour classer un nouveau point, KNN regarde simplement les `k` points les plus proches de lui dans les données d'entraînement (selon une distance, souvent euclidienne — la distance "à vol d'oiseau"), et attribue la classe majoritaire parmi ces voisins. C'est l'équivalent algorithmique du dicton "dis-moi qui sont tes amis, je te dirai qui tu es".

**Pourquoi "lent à prédire" est un vrai défaut en production :** contrairement à la régression logistique ou aux arbres (qui, une fois entraînés, appliquent une formule ou une série de questions déjà fixées), KNN doit recalculer la distance à **tous** les points d'entraînement à chaque nouvelle prédiction. Sur un dataset de plusieurs millions de lignes, cela devient rapidement impraticable en production.

### 6. Naive Bayes — approfondissement

**Pourquoi "naïf" ?** L'algorithme suppose que toutes les features sont **statistiquement indépendantes** les unes des autres (l'apparition du mot "gratuit" dans un email n'a rien à voir avec l'apparition du mot "argent") — une hypothèse presque toujours fausse en réalité, mais qui, étonnamment, fonctionne remarquablement bien en pratique, notamment pour la classification de texte, où c'est un standard historique.

### Tableau de synthèse mémo (à apprendre par cœur)

| Algorithme | Idée en une phrase | Quand y penser en premier |
|---|---|---|
| Régression Logistique | Trace une frontière droite basée sur des probabilités | Besoin d'explications claires, relation simple |
| SVM | Trace la frontière la plus "large" possible, avec astuce pour la non-linéarité | Peu de données, features nombreuses |
| Arbres de Décision | Suite de questions Oui/Non | Besoin d'expliquer visuellement chaque décision |
| Forêts Aléatoires | Vote de centaines d'arbres | Priorité à la précision plus qu'à l'explication |
| KNN | Regarde les voisins les plus proches | Petit dataset, frontières irrégulières |
| Naive Bayes | Probabilités avec hypothèse d'indépendance | Classification de texte, besoin de rapidité |

### Mini-exercice
Une banque veut un modèle de scoring de crédit, et la réglementation exige de pouvoir **justifier légalement** chaque refus de prêt auprès du client. Parmi les 6 algorithmes vus, lesquels seraient de bons candidats en priorité, et lesquels seraient risqués à utiliser malgré une éventuelle bonne précision ? Justifiez.

### Correction
Bons candidats en priorité : **Régression Logistique** et **Arbres de Décision**, car les deux permettent d'expliquer clairement la décision (coefficients interprétables pour l'un, chemin de questions pour l'autre) — un exigence réglementaire critique dans le secteur bancaire. Risqués malgré une bonne précision potentielle : **Forêts Aléatoires**, **SVM avec kernel non-linéaire**, et **KNN**, car leur logique interne est beaucoup plus difficile à traduire en une explication simple et légalement défendable pour un client refusé — même si ces modèles peuvent être statistiquement plus précis. Ce dilemme entre précision et interprétabilité est un vrai enjeu professionnel que nous retrouverons au Chapitre 7.

---

## Slide 7 — Chapitre 4 : La Régression — Concepts et Applications

### La formulation `y = f(X) + ε` décryptée sans peur des symboles

Cette formule apparemment technique dit simplement : *"la valeur réelle observée (y) est égale à ce que mon modèle prédit à partir des données (f(X)), plus une part de bruit ou d'imprévisibilité incompressible (ε)."*

**Métaphore — le tir à l'arc :** imaginez un archer qui vise le centre d'une cible en tenant compte du vent, de la distance, etc. (c'est `f(X)`, sa meilleure estimation basée sur toutes les informations disponibles). Même le meilleur archer du monde ne touchera jamais exactement le centre à chaque tir : il y a toujours une petite déviation due à des facteurs impossibles à contrôler parfaitement (tremblement de la main, micro-rafale de vent) — c'est le **ε** (epsilon), le bruit irréductible. **Un bon modèle de régression ne cherche pas à prédire parfaitement** (ce serait souvent signe de surapprentissage !), il cherche à minimiser l'écart moyen tout en acceptant qu'une part d'erreur soit statistiquement inévitable.

### La ligne de meilleur ajustement — pourquoi "minimiser la somme des erreurs au carré" ?

Pourquoi élever les erreurs au carré plutôt que de simplement les additionner telles quelles ? Deux raisons intuitives :
1. **Éviter que les erreurs positives et négatives s'annulent.** Si un modèle se trompe de +10 sur un point et de -10 sur un autre, la somme brute donnerait 0 (comme si tout allait bien), alors qu'il y a bel et bien deux erreurs de 10. Élever au carré rend toutes les erreurs positives.
2. **Pénaliser davantage les grosses erreurs.** Une erreur de 20 devient 400 au carré, alors qu'une erreur de 2 ne devient que 4 — le modèle est donc poussé à éviter particulièrement les erreurs importantes plutôt que de tolérer beaucoup de petites erreurs dispersées.

### Régression linéaire vs non-linéaire — un exemple concret et filé

Prenons l'exemple de la prédiction de prix immobiliers en fonction de la superficie :
- **Relation linéaire plausible :** chaque m² supplémentaire ajoute (à peu près) le même montant au prix, quelle que soit la taille de départ du logement.
- **Relation non-linéaire plus réaliste :** au-delà d'une certaine superficie, chaque m² supplémentaire ajoute *moins* de valeur relative (un appartement de 200m² n'est pas exactement deux fois plus cher qu'un appartement de 100m², à cause d'autres contraintes du marché) — une courbe capture mieux cette nuance qu'une droite.

### Mini-exercice
Une entreprise veut prédire le temps de trajet domicile-travail de ses employés en fonction de la distance parcourue. Proposez un argument pour lequel cette relation pourrait être non-linéaire plutôt que parfaitement linéaire.

### Correction
Plusieurs arguments valables, par exemple : au-delà d'une certaine distance, l'employé emprunte probablement l'autoroute (vitesse plus stable et élevée), alors qu'à courte distance, le trajet se fait en ville avec plus de feux rouges et d'embouteillages relatifs — le temps par kilomètre n'est donc pas constant selon la distance totale. C'est exactement le genre de raisonnement métier qui doit précéder le choix entre régression linéaire simple et un modèle capable de capturer des relations non-linéaires (régression polynomiale, arbres de régression, etc. — slide suivante).

---

## Slide 8 — Algorithmes de Régression

### 1. Régression Linéaire — le point de départ incontournable

**Pourquoi commencer toujours par ce modèle, même si vous pensez que la relation est complexe ?** Parce qu'il fournit une **baseline** (référence de base) rapide à entraîner et facile à interpréter. Si un modèle plus complexe ne fait pas significativement mieux qu'une simple régression linéaire, cela vaut souvent la peine de se poser des questions sur la complexité ajoutée pour un gain marginal.

### 2. Régression Polynomiale — approfondissement et piège classique

Ajouter des termes en `x²`, `x³`, etc. permet de capturer des courbes, mais c'est une arme à double tranchant redoutable : **plus le degré du polynôme est élevé, plus la courbe peut "onduler" pour épouser chaque point d'entraînement individuellement** — un cas d'école classique de surapprentissage visible à l'œil nu sur un graphique (une courbe qui zigzague de manière absurde entre les points plutôt que de suivre une tendance lisse).

**Métaphore :** c'est comme rédiger une biographie tellement détaillée qu'elle raconte littéralement chaque minute de la vie de quelqu'un — techniquement "exacte" pour cette personne précise, mais totalement inutile pour comprendre ou prédire la vie de quelqu'un d'autre.

### 3. Ridge & Lasso — la régularisation expliquée intuitivement

Ces deux méthodes ajoutent une **pénalité** dans la fonction de coût du modèle pour décourager des coefficients trop grands (des poids trop importants accordés à certaines features), ce qui réduit le risque de surapprentissage.

**Métaphore — le budget serré :** imaginez que chaque coefficient du modèle doit être "payé" avec un budget limité. Le modèle est donc naturellement incité à ne donner de l'importance qu'aux features vraiment utiles, plutôt que de gonfler artificiellement l'importance de chaque variable disponible, y compris celles qui n'apportent presque rien.

- **Ridge (pénalité L2 : `+ λΣβ²`)** : réduit tous les coefficients progressivement, sans jamais les mettre exactement à zéro. Comme réduire le budget de tout le monde proportionnellement.
- **Lasso (pénalité L1 : `+ λΣ|β|`)** : peut réduire certains coefficients **exactement à zéro**, ce qui revient à **éliminer complètement** certaines features du modèle. C'est donc aussi une méthode de **sélection automatique de features** — extrêmement utile quand on a beaucoup de variables et qu'on soupçonne que seules quelques-unes sont vraiment pertinentes.

### 4. Régression par Arbres et 5. Forêt Aléatoire Régression

Même logique que pour la classification (slide 6), sauf que la prédiction finale dans chaque feuille (ou chaque arbre) est **la moyenne des valeurs numériques**, pas un vote de catégorie. Métaphore identique au "jury" pour la forêt aléatoire, mais ici chaque "juré" donne un chiffre, et on fait la moyenne des chiffres plutôt qu'un vote majoritaire.

### 6. Support Vector Regression (SVR)

Extension du SVM (slide 6) à la régression : au lieu de chercher une frontière qui sépare des classes, SVR cherche une **bande de tolérance** (un tube) autour de la ligne de prédiction, à l'intérieur de laquelle les erreurs sont considérées comme négligeables et ne sont pas pénalisées. Métaphore : c'est comme un tir au but où toute la surface du but compte comme un "but", pas seulement le point exact au centre — une petite marge de tolérance est acceptée.

### Mini-exercice
Vous disposez de 500 features pour prédire un prix, mais vous soupçonnez que seules 20 sont réellement pertinentes, et le reste n'est que du bruit. Quel algorithme de cette slide choisiriez-vous en priorité, et pourquoi ?

### Correction
**Lasso** est le candidat naturel ici, précisément parce que sa pénalité L1 peut ramener les coefficients des features non pertinentes exactement à zéro, réalisant ainsi une sélection automatique de features en plus de la prédiction elle-même — ce qui correspond exactement au besoin décrit (500 features suspectées majoritairement inutiles).

---

## Slide 9 — Chapitre 5 : Métriques d'Évaluation — Classification

### La matrice de confusion — la brique fondamentale à maîtriser avant tout le reste

Toutes les métriques de cette slide (Accuracy, Precision, Recall, F1) **découlent directement** des quatre cases de la matrice de confusion. Il est impossible de vraiment comprendre ces métriques sans maîtriser d'abord ces quatre cases :

- **TP (Vrai Positif)** : le modèle prédit positif, et c'était effectivement positif. *(Bonne nouvelle correctement détectée.)*
- **TN (Vrai Négatif)** : le modèle prédit négatif, et c'était effectivement négatif. *(Absence correctement confirmée.)*
- **FP (Faux Positif)** : le modèle prédit positif, mais c'était en réalité négatif. *(Fausse alerte.)*
- **FN (Faux Négatif)** : le modèle prédit négatif, mais c'était en réalité positif. *(Cas raté, dangereux dans beaucoup de contextes.)*

**Métaphore filée — le détecteur de fumée :**
- TP : le détecteur sonne, il y a réellement un feu. ✅
- TN : le détecteur reste silencieux, il n'y a effectivement pas de feu. ✅
- FP : le détecteur sonne pour un simple toast brûlé — dérangeant, mais pas dramatique. ⚠️
- FN : le détecteur reste silencieux **alors qu'il y a un vrai incendie** — potentiellement catastrophique. 🚨

Cette métaphore va nous servir à comprendre pourquoi Precision et Recall ne se valent pas selon le contexte.

### Pourquoi l'Accuracy peut être dangereusement trompeuse

`Accuracy = (TP + TN) / Total` — la proportion de prédictions correctes, tout simplement. Le piège classique concerne les **données déséquilibrées** :

**Exemple concret et volontairement frappant :** imaginez un modèle de détection de fraude bancaire où seulement 1% des transactions sont réellement frauduleuses. Un modèle "paresseux" qui prédit **toujours "non-fraude"**, sans jamais rien analyser, obtiendrait déjà 99% d'accuracy — un chiffre qui semble excellent, alors que ce modèle est **totalement inutile** puisqu'il ne détecte jamais aucune fraude. C'est pourquoi, dans les contextes déséquilibrés (fraude, maladies rares, défauts de production rares), l'accuracy seule est une métrique piégeuse, voire trompeuse.

### Precision et Recall — le compromis fondamental, avec la métaphore du détecteur de fumée

- **Precision = TP / (TP + FP)** — "Parmi toutes mes alertes positives, combien étaient de vraies alertes ?" Une precision élevée signifie **peu de fausses alertes**. *Reprenons le détecteur de fumée : une haute precision signifie qu'il ne sonne quasiment jamais pour un simple toast brûlé.*

- **Recall = TP / (TP + FN)** — "Parmi tous les vrais cas positifs existants, combien ai-je réussi à détecter ?" Un recall élevé signifie **peu de cas ratés**. *Un haut recall signifie que le détecteur de fumée ne rate quasiment jamais un vrai incendie.*

**Le compromis (trade-off) expliqué concrètement :** en général, régler un modèle pour qu'il "sonne" plus facilement (augmenter le recall, ratant moins de vrais positifs) augmente mécaniquement le risque de fausses alertes (diminuant la precision), et vice-versa. Un détecteur de fumée hyper-sensible réglé pour ne **jamais** rater un incendie sonnera probablement aussi à chaque fois que vous faites griller du pain.

**Quand privilégier quoi — exemples professionnels concrets :**
- **Privilégier la Precision** (minimiser les FP) : filtre anti-spam d'entreprise — le coût d'un FP (un email professionnel important classé par erreur comme spam) est très élevé, alors qu'un spam occasionnel qui passe à travers (FN) est juste gênant.
- **Privilégier le Recall** (minimiser les FN) : dépistage du cancer — le coût d'un FN (un vrai cancer non détecté) est potentiellement mortel, alors qu'un FP (examen complémentaire demandé "pour rien") est coûteux mais rarement dangereux.

### F1-Score et ROC-AUC

Le **F1-Score** est la **moyenne harmonique** (pas une moyenne arithmétique classique) de Precision et Recall — la moyenne harmonique a la particularité mathématique de fortement pénaliser un déséquilibre entre les deux : un modèle avec Precision=1.0 et Recall=0.01 aura un F1 très bas, proche de 0.02, contrairement à une moyenne arithmétique naïve qui donnerait 0.5. C'est volontaire : le F1-Score récompense un **vrai équilibre**, pas une performance extrême sur une seule des deux dimensions.

Le **ROC-AUC** mesure la capacité globale du modèle à **discriminer** entre les classes, indépendamment d'un seuil de décision particulier (contrairement à Accuracy/Precision/Recall qui dépendent toutes d'un seuil fixé, souvent 0.5). Une AUC de 0.5 équivaut à un modèle qui devine au hasard (comme lancer une pièce), une AUC de 1.0 est une séparation parfaite entre les classes.

### Mini-exercice
Un hôpital teste un nouveau modèle de dépistage d'une maladie rare et grave. Sur 1000 patients testés (dont 20 réellement malades), le modèle produit : TP=18, FN=2, FP=50, TN=930. Calculez la Precision et le Recall, et commentez lequel des deux est le plus critique à surveiller dans ce contexte médical précis.

### Correction
```
Precision = TP / (TP + FP) = 18 / (18 + 50) = 18/68 ≈ 0.265 (26,5%)
Recall    = TP / (TP + FN) = 18 / (18 + 2)  = 18/20 ≈ 0.90  (90%)
```
Le Recall (90%) est nettement plus élevé que la Precision (26,5%) — ce modèle rate peu de vrais malades (seulement 2 sur 20), mais génère beaucoup de fausses alertes (50 FP). Dans ce contexte médical précis (maladie **grave**), c'est un compromis globalement **acceptable et même souhaitable** : un recall élevé signifie que très peu de vrais malades passent inaperçus, quitte à demander des examens complémentaires inutiles à des patients en bonne santé (FP) — un coût largement inférieur à celui de rater un vrai cas grave (FN).

---

## Slide 10 — Chapitre 5 (suite) : Métriques d'Évaluation — Régression

### Pourquoi les métriques de régression sont conceptuellement plus simples que celles de classification

Contrairement à la classification (où il faut jongler entre plusieurs types d'erreurs qualitativement différentes — FP vs FN), en régression il n'existe qu'**un seul type d'écart** : la différence numérique entre la valeur prédite et la valeur réelle (`yᵢ - ŷᵢ`). Toutes les métriques de cette slide ne sont que des façons différentes d'agréger cet écart sur l'ensemble des prédictions.

### MAE (Mean Absolute Error) — la métrique "bon sens"

`MAE = moyenne(|erreur|)` — on prend la valeur absolue de chaque erreur (pour que les erreurs positives et négatives ne s'annulent pas), puis on fait une simple moyenne. **Avantage majeur :** le résultat est dans la **même unité** que la variable prédite. Si vous prédisez des prix en euros, une MAE de 5000 signifie littéralement "en moyenne, mon modèle se trompe de 5000€" — directement interprétable par n'importe qui, technicien ou non.

### MSE (Mean Squared Error) — pourquoi élever au carré change tout

`MSE = moyenne(erreur²)` — comme évoqué à la slide 7, élever au carré pénalise fortement les grosses erreurs. **Conséquence pratique importante :** un modèle avec MSE bas a probablement **peu de grosses erreurs isolées**, même s'il peut avoir beaucoup de petites erreurs réparties. C'est utile quand une grosse erreur ponctuelle est particulièrement coûteuse (ex : une estimation immobilière complètement fausse est bien plus problématique que 10 petites erreurs mineures réparties sur 10 biens).

**Inconvénient concret :** l'unité de MSE est "au carré" (des euros² si on prédit des euros !), ce qui rend le chiffre brut difficile à interpréter intuitivement — d'où l'intérêt du RMSE.

### RMSE — le meilleur des deux mondes

`RMSE = √MSE` — on revient dans l'unité originale (des euros, pas des euros²) tout en conservant l'effet de forte pénalisation des grosses erreurs hérité du MSE. C'est souvent **la métrique de référence** en pratique, car elle combine interprétabilité (même unité que y) et sensibilité aux erreurs importantes.

### R² (Coefficient de Détermination) — l'intuition derrière "proportion de variance expliquée"

**Métaphore essentielle :** imaginez que, sans aucun modèle sophistiqué, votre seule stratégie de prédiction soit de toujours prédire **la moyenne** de toutes les valeurs observées (par exemple, toujours prédire le prix moyen de tous les logements, peu importe leurs caractéristiques). Le R² répond littéralement à la question : *"De combien mon modèle fait-il mieux que cette stratégie naïve de la simple moyenne ?"*

- **R² = 1** : ajustement parfait, le modèle explique 100% de la variation des données.
- **R² = 0** : le modèle est **exactement aussi bon** que de prédire bêtement la moyenne à chaque fois — aucune valeur ajoutée réelle.
- **R² < 0** : signal d'alarme sérieux — le modèle fait **pire** que la stratégie naïve de la moyenne, ce qui indique généralement un problème majeur (mauvaises features, erreur de code, modèle mal adapté au problème).

> ⚠️ **Piège important souligné dans la slide :** ajouter n'importe quelle feature, même complètement inutile ou aléatoire, à un modèle de régression linéaire ne peut **jamais faire baisser** le R² — il peut seulement rester stable ou augmenter légèrement, même sans aucune amélioration réelle du modèle. C'est pourquoi le **R² ajusté**, qui pénalise l'ajout de features non pertinentes, est préférable pour comparer des modèles avec un nombre différent de features.

### Mini-exercice
Un modèle A prédit des prix immobiliers avec RMSE = 15 000€. Un modèle B, sur le même dataset, obtient RMSE = 22 000€ mais MAE = 12 000€ (contre MAE = 14 000€ pour le modèle A). Que pouvez-vous en déduire sur la distribution des erreurs de chaque modèle ?

### Correction
Le modèle B a une MAE plus basse (erreur moyenne "typique" plus faible) mais un RMSE nettement plus élevé que le modèle A. Puisque le RMSE pénalise fortement les grosses erreurs, cet écart suggère que le modèle B fait probablement **de bonnes prédictions dans la majorité des cas** (d'où sa MAE plus basse), mais commet **quelques erreurs ponctuelles très importantes** (des prédictions très éloignées de la réalité sur certains biens atypiques) qui font grimper son RMSE de façon disproportionnée. Le modèle A, à l'inverse, a des erreurs plus "régulières" mais un peu plus grandes en moyenne, sans gros écarts isolés. Le choix entre les deux dépendrait du contexte métier : si les erreurs ponctuelles très importantes sont particulièrement problématiques (ex : litiges juridiques sur une estimation très erronée), le modèle A serait préférable malgré sa MAE légèrement supérieure.

---

## Slide 11 — Chapitre 6 : Biais, Variance et Compromis

### Le concept le plus important — et le plus mal compris — de tout le cours

Le compromis biais-variance est **LA** grille de lecture qui explique pourquoi un modèle échoue, dans la quasi-totalité des cas pratiques. Il mérite qu'on s'y arrête longuement.

**Biais (Bias)** : erreur due à des hypothèses **trop simplistes** du modèle sur la vraie nature des données. Un modèle à haut biais "ne regarde pas assez en détail" et manque des patterns réels, même dans les données d'entraînement.

**Variance** : erreur due à une sensibilité **excessive** aux fluctuations spécifiques des données d'entraînement. Un modèle à haute variance "regarde beaucoup trop en détail", au point de réagir au moindre bruit aléatoire comme s'il s'agissait d'un vrai pattern.

**Métaphore centrale du cours — l'archer, revisité (biais vs variance) :**
- **Haut biais (sous-apprentissage) :** un archer qui, systématiquement, vise 30cm trop à gauche du centre à chaque tir, mais dont les flèches sont très regroupées entre elles. Le problème n'est pas le manque de régularité, c'est une **erreur systématique de visée** — un défaut structurel dans la méthode elle-même.
- **Haute variance (surapprentissage) :** un archer dont les flèches sont en moyenne centrées autour de la cible, mais **extrêmement dispersées** d'un tir à l'autre — aucune régularité, chaque tir semble réagir à un facteur différent et imprévisible (le vent d'il y a une seconde, un micro-tremblement). Le problème ici n'est pas un biais systématique, c'est une **instabilité excessive**.
- **L'objectif idéal :** un archer dont les flèches sont à la fois **centrées sur la cible** (faible biais) **et regroupées entre elles** (faible variance).

### Sous-apprentissage (Underfitting) — diagnostic approfondi

**Signes distinctifs, expliqués :** mauvaise performance **à la fois** sur l'entraînement ET sur le test. C'est le signal-clé qui distingue le sous-apprentissage du surapprentissage : si le modèle est déjà mauvais sur les données qu'il a pourtant vues pendant l'entraînement, il ne peut évidemment pas être meilleur sur des données nouvelles — le problème n'est donc pas un manque de généralisation, mais une incapacité fondamentale à capturer les patterns, même les plus évidents.

**Exemple concret :** essayer de prédire des prix immobiliers avec une simple régression linéaire alors que la vraie relation sous-jacente est fortement non-linéaire et dépend d'interactions complexes entre plusieurs variables (superficie ET quartier ET âge du bâtiment combinés) — le modèle linéaire est structurellement "trop simple" pour ce problème, peu importe la quantité de données fournies.

### Surapprentissage (Overfitting) — diagnostic approfondi

**Signes distinctifs :** excellente performance sur l'entraînement, mais mauvaise performance sur le test — un **écart important** entre les deux est la signature caractéristique. Le modèle a essentiellement "appris par cœur" les données d'entraînement (y compris leur bruit spécifique, non généralisable) plutôt que d'apprendre des patterns transférables à de nouvelles données.

**Exemple concret :** un arbre de décision sans aucune limite de profondeur, qui crée une branche différente pour quasiment chaque exemple individuel du jeu d'entraînement — il "reconnaît" parfaitement chaque exemple qu'il a déjà vu, mais n'a essentiellement rien appris de généralisable pour des cas nouveaux.

### La formule `Erreur Totale = Biais² + Variance + Erreur Irréductible` — décodée simplement

L'"erreur irréductible" correspond au bruit intrinsèque des données (le `ε` de la slide 7) — une part d'incertitude qu'**aucun modèle, même parfait**, ne pourra jamais éliminer. Le vrai travail du data scientist consiste donc à minimiser la somme Biais² + Variance, en sachant qu'il existe presque toujours un **compromis** entre les deux : réduire l'un tend souvent à augmenter l'autre, d'où la nécessité de trouver un équilibre optimal plutôt qu'un minimum absolu des deux séparément.

### Stratégies d'équilibrage — pourquoi chacune fonctionne, expliqué

**Pour réduire le surapprentissage (variance) :**
- *Plus de données d'entraînement* : un modèle a statistiquement plus de mal à "mémoriser du bruit" spécifique s'il voit des milliers de variations différentes plutôt qu'une poignée d'exemples.
- *Régularisation (L1/L2)* : comme vu en slide 8 (Ridge/Lasso), pénalise la complexité excessive du modèle.
- *Réduire la complexité du modèle* : limiter la profondeur d'un arbre, réduire le degré d'un polynôme.
- *Early stopping* : arrêter l'entraînement dès que la performance sur la validation commence à se dégrader, même si la performance sur l'entraînement continue de s'améliorer — signe que le modèle commence à mémoriser du bruit plutôt qu'à apprendre.
- *Dropout* (réseaux de neurones) : désactiver aléatoirement une partie des neurones pendant l'entraînement, forçant le réseau à ne pas trop dépendre de combinaisons très spécifiques de neurones.

**Pour réduire le sous-apprentissage (biais) :**
- *Augmenter la complexité du modèle*, *ajouter des features pertinentes*, *réduire la régularisation*, *plus d'epochs* — globalement, l'inverse symétrique des stratégies précédentes, donner au modèle plus de "capacité" à capturer des patterns réels.

### Mini-exercice
Vous entraînez trois modèles sur le même problème et obtenez :
- Modèle A : Train Accuracy = 65%, Test Accuracy = 64%
- Modèle B : Train Accuracy = 98%, Test Accuracy = 71%
- Modèle C : Train Accuracy = 90%, Test Accuracy = 88%

Diagnostiquez chaque modèle (sous-apprentissage, surapprentissage, ou bon équilibre) et proposez une action corrective pour A et B.

### Correction
- **Modèle A** : sous-apprentissage (haut biais) — performance médiocre et quasi-identique sur train ET test. Action corrective : augmenter la complexité du modèle, ajouter des features pertinentes, ou réduire la régularisation si elle est trop forte actuellement.
- **Modèle B** : surapprentissage clair (haute variance) — écart énorme entre train (98%) et test (71%). Action corrective : régularisation (L1/L2), réduire la complexité (profondeur d'arbre, degré polynomial), ou augmenter la quantité de données d'entraînement.
- **Modèle C** : bon équilibre relatif — performance élevée et raisonnablement proche entre train (90%) et test (88%), un écart faible qui suggère une bonne généralisation. C'est le profil recherché.

---

## Slide 12 — Chapitre 7 : Arbre de Décision pour le Choix de Méthode

### Décortiquer chaque critère de sélection avec des exemples métier

**1. Type de variable cible (Catégorielle vs Numérique)** — c'est la toute première bifurcation, directement héritée du Chapitre 2 (slide 4). Rappel du test rapide : "est-ce que faire une moyenne des valeurs cibles a un sens ?"

**2. Linéarité des relations** — approfondissement pratique : comment évaluer cela **avant** même d'entraîner un modèle complexe ? En pratique, on visualise les données (nuages de points, graphiques de dispersion) ou on entraîne d'abord un modèle linéaire simple comme baseline (rappel de la slide 8) : si ses performances sont mauvaises même sur les données d'entraînement (signe de sous-apprentissage, Ch. 6), c'est un indice fort de relation non-linéaire sous-jacente.

**3. Besoin d'interprétabilité** — ce critère est souvent **le plus négligé** par les débutants, qui se concentrent uniquement sur la précision brute. Or, dans de nombreux contextes réels (santé, finance, justice, ressources humaines), la loi ou l'éthique professionnelle **exige** de pouvoir expliquer une décision individuelle — un modèle extrêmement précis mais totalement opaque ("boîte noire") peut être **inutilisable en pratique**, peu importe sa performance statistique. Nous avons déjà rencontré cet enjeu concrètement au mini-exercice de la slide 6 (scoring de crédit bancaire).

**4. Contraintes computationnelles** — un critère très concret et souvent sous-estimé : un modèle qui met 3 heures à faire une seule prédiction est inutilisable pour, par exemple, détecter une fraude bancaire **en temps réel** pendant qu'une transaction est en cours, même s'il est le plus précis en théorie. Le contexte de déploiement (temps réel vs traitement différé, contraintes matérielles) doit influencer le choix autant que la précision pure.

### Une cinquième dimension, implicite mais cruciale, à ajouter à cette liste

Le cours mentionne 4 critères explicites, mais un cinquième mérite d'être ajouté en tant que professionnel : **la quantité et la qualité des données disponibles**. Un algorithme puissant en théorie (comme une forêt aléatoire ou un réseau de neurones) peut sous-performer un modèle plus simple si le dataset est petit, bruité, ou peu représentatif — la sophistication d'un algorithme ne compense jamais un déficit fondamental de données pertinentes.

### Mini-exercice
Une startup médicale développe un outil d'aide au diagnostic qui doit (a) être validé par une autorité de santé exigeant une explicabilité totale des décisions, (b) fonctionner sur un dataset de seulement 300 patients (collecte encore en cours), et (c) prédire une variable catégorielle (maladie présente/absente). En suivant l'arbre de décision de cette slide, quel type d'algorithme serait le plus adapté, et pourquoi ?

### Correction
En suivant les critères : (1) variable catégorielle → classification ; (2) petit dataset (300 patients) → privilégier des algorithmes qui ne nécessitent pas d'énormes quantités de données pour bien généraliser ; (3) interprétabilité exigée par la réglementation → exclut d'emblée les forêts aléatoires, SVM à kernel complexe, ou réseaux de neurones malgré leur précision potentielle. **La Régression Logistique** ou un **Arbre de Décision simple (peu profond)** ressortent comme les choix les plus cohérents avec l'ensemble de ces contraintes réunies — un excellent exemple montrant que le "meilleur" algorithme n'est presque jamais une question de précision brute isolée, mais toujours une décision multicritère ancrée dans un contexte métier et réglementaire réel.

---

## Slide 13 — Tableau Récapitulatif des Algorithmes

### Comment utiliser ce tableau en pratique professionnelle

Ce tableau n'est pas fait pour être mémorisé mot pour mot — il est fait pour être **consulté comme un aide-mémoire rapide** lors d'un vrai projet, après avoir répondu aux questions de l'arbre de décision (slide 12). Voici comment un professionnel l'utiliserait réellement : d'abord déterminer classification vs régression, puis filtrer les lignes correspondantes, puis croiser avec les contraintes du projet (interprétabilité, taille de données, contraintes de temps de calcul).

### Remarque professionnelle importante sur la colonne "Les deux"

Notez que SVM, Arbres de Décision, Forêts Aléatoires et KNN apparaissent comme utilisables pour **"Les deux"** (classification ET régression). C'est un point souvent source de confusion chez les débutants : ces algorithmes reposent sur une **logique structurelle** (trouver une frontière/marge, poser des questions séquentielles, faire un vote/moyenne d'ensemble, comparer aux voisins) qui s'adapte aux deux types de sortie, simplement en changeant la façon dont la prédiction finale est agrégée dans la feuille/le voisinage/le vote (catégorie majoritaire pour la classification, moyenne numérique pour la régression) — un fil conducteur déjà évoqué aux slides 6 et 8.

### Mini-exercice
Un e-commerçant souhaite (a) prédire si un client va laisser un avis négatif après un achat (oui/non), en utilisant des données textuelles de son historique de messages au service client, avec une contrainte forte de rapidité de traitement (des millions de clients à traiter quotidiennement). En consultant le tableau récapitulatif, identifiez l'algorithme le plus cohérent et justifiez par élimination.

### Correction
**Naive Bayes** ressort comme le choix le plus cohérent : le tableau l'indique explicitement comme "Meilleur pour : Texte, classification rapide" — ce qui correspond exactement aux deux contraintes du problème (données textuelles + besoin de rapidité à très grande échelle). Par élimination : SVM serait risqué sur de très grands datasets (mentionné comme un cas à éviter), KNN serait beaucoup trop lent à la prédiction sur des millions de clients quotidiens (rappel du défaut structurel vu en slide 6), et Random Forest, bien que précis, n'est pas spécifiquement optimisé pour du texte ni pour la vitesse pure comparé à Naive Bayes.

---

## Slide 14 — Récapitulatif : Points Clés à Retenir

### Synthèse professorale finale — relier tous les fils du cours

Cette dernière slide résume cinq piliers, mais leur vraie force pédagogique est de voir comment ils **s'enchaînent logiquement**, comme les maillons d'une seule chaîne de raisonnement que tout data scientist doit parcourir face à un nouveau problème :

1. **On comprend d'abord** ce qu'est l'apprentissage supervisé (données étiquetées, fonction de mapping, généralisation) → Ch. 1
2. **On identifie ensuite** la nature du problème (classification ou régression) → Ch. 2
3. **On explore** les algorithmes disponibles pour cette famille spécifique → Ch. 3-4
4. **On choisit un algorithme** en fonction de critères multiples (données, linéarité, interprétabilité, contraintes) → Ch. 7
5. **On surveille en permanence** le compromis biais-variance pendant l'entraînement → Ch. 6
6. **On mesure objectivement** la qualité du modèle avec les métriques adaptées au contexte métier (pas juste l'accuracy brute) → Ch. 5

**La phrase de clôture du cours** — *"L'apprentissage supervisé est le fondement de l'IA moderne"* — mérite d'être nuancée avec honnêteté intellectuelle : c'est un fondement **historique et toujours dominant en usage industriel réel**, mais ce n'est plus la seule frontière de recherche en IA aujourd'hui — l'apprentissage par renforcement (utilisé par exemple pour AlphaGo) et l'apprentissage auto-supervisé (à la base des grands modèles de langage modernes) élargissent aujourd'hui considérablement le paysage. Néanmoins, la maîtrise rigoureuse des concepts de ce cours — généralisation, compromis biais-variance, choix de métriques adaptées au contexte — reste un socle de raisonnement transférable à absolument tous les autres paradigmes d'apprentissage automatique, même les plus récents.

### Exercice de synthèse final (à faire sans notes)

Un cabinet d'assurance vous confie un projet : prédire le montant qu'un assuré va probablement réclamer l'année prochaine, à partir de son historique. Décrivez, en mobilisant les concepts des 8 chapitres du cours, le raisonnement complet que vous suivriez, de la définition du problème jusqu'au choix final d'un modèle et de ses métriques d'évaluation.

### Correction (proposition de raisonnement structuré)

1. **Nature du problème (Ch. 2) :** le "montant réclamé" est une variable numérique continue → il s'agit d'un problème de **régression**, pas de classification.
2. **Exploration des algorithmes (Ch. 4) :** commencer par une régression linéaire comme baseline rapide et interprétable ; envisager Ridge/Lasso si beaucoup de variables sont disponibles avec un risque de multicolinéarité ; envisager une forêt aléatoire de régression si la relation semble fortement non-linéaire après une première exploration.
3. **Critères de choix (Ch. 7) :** le secteur de l'assurance étant fortement régulé, l'**interprétabilité** est probablement un critère fort (justifier pourquoi une prime est fixée à tel niveau) → cela pousserait vers une régression linéaire/Ridge/Lasso plutôt que vers un modèle plus opaque, sauf si le gain de précision d'un modèle plus complexe est jugé indispensable et documentable.
4. **Surveillance biais-variance (Ch. 6) :** comparer systématiquement la performance sur train vs test pour détecter un éventuel surapprentissage (particulièrement risqué avec une régression polynomiale ou une forêt aléatoire trop profonde), et ajuster la régularisation ou la complexité en conséquence.
5. **Métriques d'évaluation (Ch. 5) :** privilégier le **RMSE** (unité interprétable en euros, pénalise fortement les grosses erreurs de prédiction — coûteuses pour l'assureur en cas de sous-provisionnement) et le **R²** (ou R² ajusté si plusieurs modèles à nombre de features différent sont comparés) pour juger de la qualité globale d'ajustement, plutôt que la seule MAE qui masquerait des erreurs ponctuelles très coûteuses.

> Si vous avez pu reconstruire seul un raisonnement structuré proche de celui-ci, vous avez véritablement assimilé la logique d'ensemble du cours — pas seulement sa terminologie.

---

## Glossaire Final — Tous les Termes Clés du Cours

| Terme | Définition express |
|---|---|
| Donnée étiquetée | Paire (entrée, sortie correcte connue) |
| Fonction de mapping | La relation que le modèle apprend entre entrées et sorties |
| Généralisation | Capacité à bien prédire sur des données jamais vues |
| Fonction de coût | Formule mesurant l'erreur du modèle |
| Descente de gradient | Méthode d'ajustement progressif des paramètres pour réduire l'erreur |
| Frontière de décision | Ligne/surface séparant les classes dans l'espace des features |
| Vecteurs de support | Points critiques les plus proches de la frontière (SVM) |
| Gain d'information | Critère de choix de la meilleure question de découpage (arbres) |
| Apprentissage d'ensemble | Combiner plusieurs modèles pour une prédiction plus robuste |
| Régularisation | Pénalité contre la complexité excessive du modèle (Ridge/Lasso) |
| Matrice de confusion | Tableau TP/TN/FP/FN, base de toutes les métriques de classification |
| Biais | Erreur due à un modèle trop simple (sous-apprentissage) |
| Variance | Erreur due à un modèle trop sensible aux données d'entraînement (surapprentissage) |
| Hyperparamètre | Réglage du modèle non appris directement des données |
| Baseline | Modèle simple de référence pour comparer les modèles plus complexes |

---

*Fin du document complémentaire. Ce document doit être utilisé en parallèle du support de présentation original — chaque section correspond directement à la slide du même numéro.*
