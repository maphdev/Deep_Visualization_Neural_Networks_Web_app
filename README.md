##### Installation de Python3 ######
sudo apt-get update
sudo apt-get install python3.6

~~~~ Développement ~~~~

##### Installation d'un environnement virtuel #####
virtualenv -p python3 PDPDEEPVISENV

##### Activation de l'environnement virtuel #####
source PDPDEEPVISENV/bin/activate

##### Installation des dépendances dans l'environnement virtuel #####
pip install -r requirements.txt

##### Lancement du serveur de développement #####
python run.py

L'application est accessible à l'adresse http://localhost:8080/

#### Générer des modèles pré-entrainés
python generate_models.py nameModel
avec nameModel le nom du modèle à générer parmi : "VGG16", "ResNet50" ou "NASNetLarge".
