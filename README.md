# Docker FastNetMon

## introduction

Ce docker est fait à partir des repo Git https://github.com/ptx-tech/fnm-webui-docker et https://github.com/pirmins/fnm-fsgui et corrige certains bugs à l'installation. Le but est de mettre en place différentes interfaces opensources existantes à FastNetMon (https://github.com/pavel-odintsov/fastnetmon).

-

This docker is made from the Git repo https://github.com/ptx-tech/fnm-webui-docker and https://github.com/pirmins/fnm-fsgui and it fixes some bugs on installation. The aim is to implement some interfaces at FastNetMon (https://github.com/pavel-odintsov/fastnetmon).

## Changements Webui - Webui changes

Comme dit plutôt, j'ai effectué des changements sur le repo Git WebUI de base, voici les différents changements.

-

As I said earlier, I've made some changes to the basic Git repo, here are the various changes.

1) modifier le fichier examples/compose/fnmwebui.env et retirer :

````env
CACHE_DRIVER=redis
SESSION_DRIVER=redis
REDIS_HOST=redis
````

2) modifier le fichier examples/compose/docker-compose.yml port la section "port" de la partie fnmwebui comme suit : 

````bash
ports:
  - "0.0.0.0:8000:8000"

````

## Changements Webui - Webui changes

Comme dit plutôt, j'ai effectué des changements sur le repo Git fnm-fsgui de base, voici les différents changements.

-

As I said earlier, I've made some changes to the basic fnm-fsgui Git repo, here are the various changes.

1) Ce n'est pas une correxion mais j'ai redesigné pour que ça se lance directement toutes les interfaces avec un même docker-compose. J'ai donc un peu changé le dockerfile de base et ajouté un volume partagé pour avoir accès facilement à la base de données et au code. 

2) J'ai enlevé la librairie "django-bulma-widget==1.2" des requirements et réarrangé le code en conséquence car elle empéchait le fonctionnement de l'interface, je n'arrivais pas à la charger, elle n'existe peut-être plus. 

3) J'ai réaffecté quelques changements visuels car le rendu de l'interface était mal arrangé étant donné que j'ai enlevé l'utilisation de la librairié "django-bulma-widget==1.2" et que c'était une librairie visuelle.


## étapes à suivre - steps to follow 

Voici les différentes étapes à suivre pour mettre en place l'infrastructure FastNetMon, Grafana et la WebUI. 

-

Here's how to set up the FastNetMon infrastructure, Grafana and WebUI. 

### Machine 

Faire une machine ubuntu (en production c'est conseillé 16Gb de RAM et 8 coeurs)

### Clone

Commencez par cloner ce repository 

````bash
git clone https://github.com/ShonenNoSeishin/DockerFastNetMon.git
cd DockerFastNetMon
````

### FastnetMon

Souscrire à une version d'essais sous https://fastnetmon.com/trial/ pour recevoir un coupon d'activation par mail. 

````bash
wget https://install.fastnetmon.com/installer -Oinstaller
sudo chmod +x installer
sudo ./installer -activation_coupon <coupon_d’activation> 
````

vous devriez maintenant avoir accès au fcli avec la commande :

````bash
sudo fcli
````

### Grafana

(https://fastnetmon.com/docs-fnm-advanced/advanced-visual-traffic/?utm_source=advanced_trial_allocation_email&utm_medium=email)

Il est ensuite possible de faire tourner une couche graphique Grafana.

````bash
sudo ./installer -install_graphic_stack 
````

Si vous en avez, changer les certificats par défaut sous « /etc/nginx/sites-enabled/grafana.conf » :
  o ssl_certificate /etc/ssl/certs/ssl-cert-snakeoil.pem;
  o ssl_certificate_key /etc/ssl/private/ssl-cert-snakeoil.key;

````bash
# redémarrage du service nginx
sudo systemctl restart nginx
````

Changer de mot de passe :

````bash
sudo ./installer -reset_visual_passwords -visual_login admin 
# Récupérer le mdp renvoyé
````

configurer le fichier « /etc/grafana/provisioning/datasources/fastnetmon.yaml :

````yml
apiVersion: 1
providers:
  - name: dashboards
    type: file
    updateIntervalSeconds: 30
    editable: true
    options:
      path: /var/lib/grafana/fastnetmon_dashboards
      foldersFromFilesStructure: true
````

Maintenant, on sait joindre l’interface Grafana via 127.0.0.1 avec le login « admin » et le mot de passe reçu plus tôt. 

### WebUI et fsgui

#### Lancement des conteneurs 

Pour la partie WebUI et fsgui, il faudra suivre les instructions suivantes : 

````bash
# Créer un login API 
sudo fcli set main web_api_login admin
# Créer un password API 
sudo fcli set main web_api_password <password>
# Spécifier le port API 
sudo fcli set main web_api_port 10007 # ou un autre port
# Spécifier l'hôte
sudo fcli set main web_api_host <votre_ip> 
# Commit les changements dans la DB Mongo (créée à l'installation)
sudo fcli commit
# Relancer le service API
sudo systemctl restart fastnetmon_web_api
````
attention, si vous mettez 127.0.0.1 au lieu de votre IP, vous risquez de ne pas savoir joindre l'API via docker et donc ne pas savoir interagir via la WebUI

Il faudrait maintenant bien avoir accès à l'API, vérifiez comme ceci : 

````bash
curl -X GET -u admin:<API_PASSWD> http://<votre_IP>:10007/license
# Vous devirez recevoir un success
````
note : vous devriez également savoir la joindre depuis le docker ("docker exec -it <container> /bin/bash")

En cas de problème avec l'api, n'hésitez pas à débugger avec les tips donné sur cette page https://fastnetmon.com/docs-fnm-advanced/advanced-api/ (vérifier que le service est up ...) 

Créer votre fichier .env à partir de celui dans l'example :

````bash
# Aller dans le bon dossier 
cd fnm-fsgui
# Créer le fichier .env à partir de celui d'exemple 
cp example.env .env 
# --> modifier les valeurs pour que ça corresponde avec les vôtres 
````

Pour la suite il faut avoir installé docker :

````bash
sudo apt install docker docker.io -y
```` 
mais aussi "docker compose" (sans tirets), testez si vous l'avez avec :

````bash
docker compose version
```` 

Si vous ne l'avez pas, suivre la section "install plugin manually de ce repo git https://docs.docker.com/compose/install/linux/

Une fois que vous avez la version de docker compose (ne pas oublier d'ajouter l'utilisateur dans le groupe docker et de démarrer une nouvelle session si vous ne voulez pas utiliser sudo) : 

````bash
# ajouter l'user au groupe docker
sudo usermod -aG docker user
# ouvrir une nouvelle session pour prendre en compte
su user 
````

````bash
cd ../examples/compose
# compiler l'image docker de fsgui
docker build ../../fnm-fsgui/. 
# Lancer les conteneurs
docker compose up 
````

#### configurations fsgui

Avant d'accéder à l'interface graphique, il faut faire une migration (pour mettre à jour la DB de Django), Pour se faire, il faut entrer dans le conteneur en interractif : 

````bash
# Entrer dans le conteneur (note : fsgui-django est le nom du conteneur) 
docker exec -it fsgui-django /bin/bash
# préparer la migration 
python manage.py makemigrations
# faire la migration 
python manage.py migrate
````

Ainsi, la base de donnée du serveur Django est bien à jour. Cependant, il faut aussi mettre à jour avec les classes créées dans le projet spécifique du serveur Django comme suit :

````bash
# Entrer dans le conteneur (note : fsgui-django est le nom du conteneur) 
docker exec -it fsgui-django /bin/bash
# préparer la migration (note : fsgui est le nom du projet Django initialisé) 
python manage.py makemigrations fsgui
# faire la migration 
python manage.py migrate fsgui 
````

On peut maintenant accéder à l’interface WebUI via http://localhost:8024. Il faut créer un compte admin django pour accéder à l'interface. 
Pour se faire, il faut également entrer dans le conteneur en interractif : 

````bash
# Entrer dans le conteneur (note : fsgui-django est le nom du conteneur) 
docker exec -it fsgui-django /bin/bash
# Créer le compte admin
python manage.py createsuperuser
````

#### configurations WebUI

On peut maintenant accéder à l’interface WebUI via http://localhost:8000 et les credentials par défaut sont :
- username: admin@localhost 
- password: password

à la création du DC via la WebUI, on reçoit une erreur 500 : 
De base la table de la base de données de WebUI n’accepte pas assez de caractères pour le mot de passe API ce qui fait que le mot de passe configuré pour l’API ne passe pas auprès de la WebUI, donc au lancement du docker, il augmenter la taille du champ directement dans le docker : 

````bash
# lancer le conteneur en interactif
docker exec -it fnmwebui_db /bin/bash
# entrer dans la db fnmui
mariadb fnmwebui
# regarder les tables existantes 
show tables ; 
# voir la configuration de la table dc
desc dc ; 
# modifier le champ qui pose problème
alter table dc modify api_password VARCHAR(255) ;
````

Il reste une dernière erreur à régler. C'est probablement dû au fait que dans l'image docker utilisée, le code laravel à été mis à jour alors que la version de laravel dans docker est restée la même (ce n'est qu'une hypothèse). l'erreur fait que lorsque l'on clique sur certains boutons, il y a des erreur 500 qui apparaissent. Après avoir debug le code qui posait problème, j'ai mit le code corrigé dans ce repo Git sous CodeToChange/show.blade.php. Il faudra donc entrer dans le conteneur docker et changer le fichier en question comme suit :

````bash
# ouvrir le conteneur en interactif
docker exec -it fnmwebui /bin/bash
# déplacer le fichier problématique et le mettre en backup 
mv resources/views/dc/show.blade.php resources/views/dc/show.blade.php.bak
# recréer le fichier 
vi resources/views/dc/show.blade.php
# --> copier le contenu du fichier CodeToChange/show.blade.php (dans ce Git) dans le nouveau fichier créé
# --> note : sur vi, il faut appuyer sur "i" pour entrer en insert mode, puis coller avec ctrl-shit-V puis sortir de l'insert mode en faisant "esc" puis faire ":wq" pour quitter et sauvegarder
````  
Au niveau de ce que j'ai corrigé en tant que tel dans le code, c'était pour les 3 erreurs lors d'un accès à un tableau, l'accès se faisait trop vite avant que l'entrée recherchée ne soit correctement initialisée, donc ça crachait. J'ai donc simplement ajouté des vérification pour ces entrées et donc maintenant, ça se lance une foit prêt. il a également fallu que je change "\Carbon\Carbon::now()" par "time()" lors d'une conditon pour éviter un problème de comparaison entre des données de types différentes. 

Maintenant, tout devrait fonctionner correctement.

### DEBUGGING

Dans le cadre de ce docker, j'ai laissé le debugging activé pour corriger certaines erreurs. Dans le cas ou vous voulez le désactiver, il faudra retirer APP_DEBUG=true des variables d'environnement dans "examples/compose/fnmwebui.env". Ensuite, il faudra entrer dans le conteneur en interactif pour changer le fichier env directement au sein du conteneur pour que ça prenne effet : 

````bash
docker exec -it fnmwebui /bin/bash 
echo "APP_DEBUG=true" >> .env 
# sortir de l'interactif
exit 
# redémarrer le docker pour que ça prenne effet
docker compose down
docker compose up 
````

De cette manière, vous verrez les erreurs directement dans la page web et ce sera plus facile à debug.


### Erreurs 

Il peut arriver pour la WebUI qu'une erreur 500 se produise, j'en ai déjà eu, mais c'est tellement peu fréquent que je n'ai pas su réellement la débugger ... Si cela arrive, c'est uniquement dans l'affichage, si vous rechargez la page, votre action sera à priori bel et bien prise en compte.
