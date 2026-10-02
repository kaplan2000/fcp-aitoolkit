# FCP AI-Toolkit 1.1.1 est sorti : la 1.1, plus deux corrections

Date: 2026-10-02
Status: Sortie
Language: fr
Canonical: https://www.fcp-aitoolkit.com/fr/blog/fcp-ai-toolkit-1-1-1/

La 1.1.1 est sur le Mac App Store avec Smart Cache, la modification des sous-titres, Smart Search et environ 100 langues. Le « .1 » en plus vient de deux bogues corrigés juste à temps.

FCP AI-Toolkit 1.1.1 est sur le Mac App Store depuis le 30 septembre. Si vous utilisez la version 1.0, c’est votre mise à jour. Ouvrez le Mac App Store et mettez à jour comme d’habitude.


Cette version tient en une idée : reprendre un montage sans repartir de zéro. Vous essayez un autre style, vous raccourcissez l’intro, vous corrigez un nom, vous prolongez un plan. Les sous-titres suivent le rythme, au lieu de recommencer de zéro à chaque fois.



## Attendez, que s’est-il passé avec la 1.1 ?

Bonne question. Le 22 septembre, nous avons publié un aperçu intitulé [Bientôt dans la 1.1](/fr/blog/fcp-ai-toolkit-1-1-preview/). La version 1.1 était terminée et vérifiée. Elle n’attendait que sa vidéo de lancement.


Puis, le 25 septembre, nous avons fait un dernier tour de tests sur de vrais projets Final Cut Pro. Plusieurs plans, de l’audio détaché, le genre de désordre d’un vrai montage. Deux bogues sont apparus. Nous avons corrigé les deux le jour même.


Nous aurions pu publier la 1.1 et la corriger ensuite. Nous avons préféré corriger d’abord la version et lui donner un nouveau numéro. La 1.1.1 est donc simplement la 1.1 plus deux corrections. Les fonctions sont exactement celles décrites dans l’aperçu, et le « .1 » en plus représente les deux bogues que nous avons attrapés avant que vous ne les rencontriez.


Nous avons envoyé la 1.1.1 à Apple le 27 septembre, et elle est sortie le 30. Personne n’a raté de version : il n’y a jamais eu de 1.1 publique. Si vous êtes en 1.0, vous passez directement à la 1.1.1.


- 21 juin 2026Sortie de la version 1.022 septembre 2026La 1.1 est présentée et attend sa vidéo de lancement25 septembre 2026Dernier test : deux bugs, corrigés le jour même
- 27 septembre 2026La 1.1.1 part en validation chez Apple30 septembre 2026La 1.1.1 est en ligne sur le Mac App Store

## La première correction : des sous-titres qui se chevauchaient

Quand vous appuyez sur Analyze, l’extension transcrit chaque plan de dialogue de votre timeline séparément, puis assemble les résultats. Dans certains projets, cela pouvait donner deux fois la même phrase, ou des sous-titres superposés. Nous avons trouvé trois causes possibles :




- Un plan raccourci. Vous coupiez le début d’un plan sur la timeline, mais les paroles de la partie masquée, coupée, pouvaient quand même ressortir en sous-titres.

- Deux plans avec les mêmes paroles. Pensez à l’audio de la caméra plus un micro séparé, tous deux marqués comme dialogue. Les mêmes mots pouvaient apparaître deux fois.

- Le modèle de reconnaissance vocale lui-même. Whisper renvoie parfois des lignes qui se chevauchent un peu.

Pris isolément, c’est agaçant. Mais la 1.1.1 apporte aussi un éditeur de sous-titres, et l’éditeur fait quelque chose de sensé : il refuse toute modification de minutage qui ferait chevaucher un sous-titre avec son voisin. Avec des doublons qui se chevauchaient déjà, chaque correction tentée aurait été refusée. Vous n’auriez eu aucune issue, face à un éditeur qui semblait verrouillé.


Voici ce qui se passe maintenant :




- Les sous-titres de chaque plan sont limités à la partie du plan que vous voyez réellement sur la timeline, sans couper de mots en deux.

- Les paroles en double sont fusionnées en un seul sous-titre.

- Tout chevauchement restant est proprement séparé.

- Les sous-titres enregistrés avant la correction sont réparés automatiquement au chargement.

Et il y a un nouveau bouton de suppression sur chaque sous-titre. Si une ligne ne vous convient pas, supprimez-la. Elle reste supprimée la fois suivante.



## La seconde correction : un audio qui n’était pas là où nous le pensions

Celle-ci concerne l’audio détaché de sa vidéo, ou placé sur un plan connecté. Cas fréquent : le son d’un enregistreur séparé, attaché à votre plan principal.


Dans ces projets, l’extension pouvait mal lire les positions sur votre timeline. Dans l’un de nos projets de test, l’audio détaché était plus long que sa vidéo. Seule la durée de la vidéo était transcrite, et les deux sources étaient décalées de 1,6 seconde. Les sous-titres se désynchronisaient.


Désormais, les positions des plans imbriqués et connectés sont calculées correctement. Un plan connecté est mesuré sur son propre scénario, au lieu d’être coupé à la durée du plan auquel il est rattaché. L’image d’un plan vidéo n’est plus prise pour une source audio. Et les rôles audio, les plans désactivés et les canaux audio coupés sont respectés.


Les deux corrections viennent du même endroit : les projets réels. Nous sommes heureux de les avoir testés une fois de plus.



## Smart Cache : ne repartez pas de zéro

Smart Cache se souvient, sur votre Mac, de ce qui a déjà été transcrit.


Imaginez. Vous sous-titrez une interview et le résultat vous plaît. Puis le client demande dix secondes de plus à la fin. Vous prolongez le plan sur la timeline et relancez Analyze. Seule la nouvelle partie, pas encore transcrite, passe par Whisper. Le reste est déjà là.


Relancez le même plan, avec la même langue et le même modèle, et les sous-titres reviennent instantanément. C’est utile tant qu’un montage évolue : essayez un autre style, relancez, raccourcissez, prolongez, sans recommencer le passage de sous-titrage de zéro.


Smart Cache est activé par défaut. Un interrupteur dans l’extension permet de le désactiver. La première exécution d’un plan prend toujours le temps qu’elle prend, et cela dépend de votre Mac, de votre plan et du modèle. Smart Cache aide pour la deuxième exécution, pas pour la première.



## Corrigez un sous-titre avant qu’il n’arrive sur la timeline

Même un bon modèle de reconnaissance vocale peut écrire le nom de votre invité à sa façon. Vous pouvez maintenant corriger un nom, un signe de ponctuation ou toute une phrase directement dans l’extension, avant que les titres n’arrivent sur la timeline.


Vous pouvez aussi modifier le début et la fin de chaque sous-titre. L’éditeur vérifie votre minutage au fur et à mesure. Il refuse une plage invalide et un sous-titre qui chevauche son voisin, pour qu’un petit changement ne casse pas la séquence sans prévenir.


Vos modifications sont enregistrées sur votre Mac. Elles reviennent quand vous rouvrez l’extension, ou quand vous analysez à nouveau le même média. Et, nouveauté de la 1.1.1, vous pouvez supprimer un sous-titre dont vous ne voulez pas.



## Smart Search : où ai-je dit ça ?

Vous vous souvenez d’avoir parlé d’un objectif, mais plus dans quelle vidéo. Smart Search parcourt tous les sous-titres que vous avez générés, dans tous vos plans. Chaque résultat affiche le texte correspondant, le nom du fichier et le timecode.


La recherche voit aussi vos corrections. Si vous avez corrigé un nom, c’est le nom corrigé que vous pouvez retrouver.


Une limite, en toute honnêteté : cliquer sur un résultat ne vous amène pas au plan dans Final Cut Pro. Vous obtenez le nom du fichier et le timecode, et vous vous y rendez vous-même.



## Environ 100 langues, et Auto Detect

La version 1.0 proposait un sélecteur de 20 langues. Le menu des langues liste maintenant les quelque 100 langues du catalogue du modèle Whisper. En haut, une nouvelle option : Auto Detect. Si vous ne savez pas quelle langue est parlée dans un plan, ou si vous mélangez les langues d’un plan à l’autre, laissez-la décider. Auto Detect fonctionne aussi sur votre Mac, après le téléchargement du modèle.


Lisez bien ce passage. Ce nombre correspond à la couverture linguistique du modèle. Nous n’avons pas testé la qualité des sous-titres séparément dans chaque langue. La précision des sous-titres dépend de la langue, de l’enregistrement, de la personne qui parle et du modèle. Relire vos sous-titres fait donc toujours partie du travail, dans toutes les langues. Avec le nouvel éditeur, c’est aussi plus rapide.



## Des fenêtres plus petites

L’extension s’adapte maintenant aux fenêtres Final Cut Pro plus petites, par exemple sur un écran d’ordinateur portable. La zone de dépôt du projet, la recherche et le choix des modèles restent accessibles.



## Ce qui ne change pas



- La transcription s’exécute toujours sur votre Mac. Nous utilisons WhisperKit, qui repose sur Whisper d’OpenAI. Vos images ne sont pas envoyées à un service de transcription dans le cloud. Le modèle de reconnaissance vocale est téléchargé une fois, ce qui nécessite internet. Les achats sur l’App Store et les vérifications d’abonnement utilisent aussi internet.

- Les mêmes cinq modèles. Basic, Highlighted, Highlighted with Background, Pop et Beast Pop. La police, la couleur et la position restent réglables.

- Le même résultat bien rangé. Vos titres reviennent regroupés dans un plan composé au sein d’un scénario secondaire.

- Le même modèle tarifaire. L’application se télécharge gratuitement et les modèles sont gratuits. Les sous-titres automatiques par IA nécessitent un abonnement mensuel actif. Pour les tarifs en vigueur, consultez la [page du Mac App Store](https://apps.apple.com/app/id6775619373).


## Ce que cette mise à jour ne contient pas

Pour que vous n’ayez pas à vous poser la question : la 1.1.1 n’a pas d’export SRT ou d’autre fichier de sous-titres, pas de synthèse vocale et pas de mise en ligne automatique sur YouTube. La recherche trouve des mots, pas des images ni des idées : il n’y a donc pas de recherche visuelle ou sémantique. Et, comme dit plus haut, un résultat de recherche ne mène pas au plan.


Nous travaillons déjà sur la prochaine mise à jour. Nous ne promettrons rien à son sujet ici. Nous préférons vous le dire quand elle sera prête.



## Téléchargez, regardez, dites-nous ce que vous en pensez

Pour mettre à jour, ouvrez le [Mac App Store](https://apps.apple.com/app/id6775619373) et installez FCP AI-Toolkit 1.1.1. La page de l’App Store est maintenant disponible en 10 langues et propose une courte vidéo de présentation.


Pour le voir à l’œuvre, regardez la [vidéo de lancement sur YouTube](https://www.youtube.com/watch?v=ZvGX2RwCvH8). Nos premières vidéos, un film de lancement et des Shorts, sont sur [YouTube](https://www.youtube.com/@FCPAIToolkit) et sur [Instagram](https://www.instagram.com/fcpaitoolkit/) en Reels. Nous sommes aussi sur [TikTok](https://www.tiktok.com/@fcpaitoolkit). Pour retracer notre parcours, [l’article de la 1.0](/fr/blog/fcp-ai-toolkit-1-0/) et [l’aperçu de la 1.1](/fr/blog/fcp-ai-toolkit-1-1-preview/) sont toujours en ligne.


Si quelque chose ne fonctionne pas dans votre projet, ou si vous avez une idée, écrivez-nous à help@fcp-aitoolkit.com. Un vrai projet avec un vrai problème est le meilleur test que nous puissions avoir. C’est ainsi que nous avons trouvé ces deux bogues.


Merci d’utiliser FCP AI-Toolkit.
