# Copyright 2018 (C) A. Brabant A. Delasalle L. Leduc M. Philippot

# This file is part of P&P Deep-Vis.

# P&P Deep-Vis is free software: you can redistribute it and/or modify it under
# the terms of the GNU Lesser General Public License as published by the Free
# Software Foundation, either version 3 of the License, or (at your option) any
# later version.

# P&P Deep-Vis is distributed in the hope that it will be useful, but WITHOUT
# ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
# FOR A PARTICULAR PURPOSE.  See the GNU Lesser General Public License for more
# details.

# You should have received a copy of the GNU Lesser General Public License along
# with P&P Deep-Vis; if not, write to the Free Software Foundation,
# Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA

class DataBase( object ):
    """ Le nom de l'image doit être organisé comme suit:
    <Model>_<Vis>_<param1>_<param2>_..._<paramN> """

    def addUser(self, user):
        """ Ajoute un utilisateur
        Attention ne vérifie pas si l'utilisateur existe déjà
        Si c'est le cas la fonction ne fait rien
        Args:
            user =  nom de l'utilsateur (str)
        """
        raise NotImplementedError( "Should be implemented" )

    def removeUser(self, user):
        """ Supprime un utilisateur
        Args:
            user = nom de l'utilsateur (str)
        Raises:
            UserNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def addModel(self, user, model_name, model):
        """ Ajoute un modèle pour un utilisateur
        Attention ne vérifie pas si un model existe déjà à ce nom
        Si c'est le cas la fonction ne fait rien
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model
            model = werkzeug.datastructures.FileStorage contenant le model supporté par keras
        Raises:
            UserNotFoundError
        Returns:
            path_file (str)
        """
        raise NotImplementedError( "Should be implemented" )

    def removeModel(self, user, model_name):
        """ Supprime un modèle pour un utilisateur
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
            model = werkzeug.datastructures.FileStorage contenant le model supporté par keras
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def addModelJson(self, user, model_name, model_json):
        """ Ajoute au modèle d'un utilisateur un fichier .json (utilisé pour la visualisation)
        Attention ne vérifie pas si un .json existe déjà pour ce model
        Si c'est le cas la fonction ne fait rien
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model
            model_json = string
        Raises:
            UserNotFoundError
            ModelNotFoundError
        Returns:
            path_file (str)
        """
        raise NotImplementedError( "Should be implemented" )

    def removeModelJson(self, user, model_name):
        """ Supprime au modèle d'un utilisateur le fichier .json associé
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def addVisualization(self, user, model_name, vis, img_name, img):
        """ Sauvegarde le résultat d'une visualisation pour un utilisateur
        Attention ne vérifie pas si cette image existe déjà à ce nom
        Si c'est le cas la fonction ne fait rien
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
            vis = nom de la visualisation (str)
            img_name = nom de l'image à sauvegarder (str)
            img = numpy image
        Raises:
            UserNotFoundError
            ModelNotFoundError
        Returns:
            path_file (str)
        """
        raise NotImplementedError( "Should be implemented" )

    def removeVisualization(self, user, model_name, vis, img_name):
        """ Supprime le résultat d'une visualisation pour un utilisateur
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
            vis = nom de la visualisation (str)
            img_name = nom de l'image à sauvegarder (str)
        Raises:
            UserNotFoundError
            ModelNotFoundError
            VisuNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectUserModel(self, user, model_name):
        """ Renvoie un chemin vers le modèle de l'utilisateur nommé model_name
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
        Returns:
            path (str)
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectUserModelJson(self, user, model_name):
        """ Renvoie un chemin vers le fichier correspondant au json du model
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
        Returns:
            path (str)
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectUserModelvis(self, user, model_name, vis, img_name):
        """ Renvoie un chemin vers le fichier correspondant à l'image demandée
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
            vis = nom de la visualisation (str)
            img_name = nom de l'image à sauvegarder (str)
        Returns:
            path (str)
        Raises:
            UserNotFoundError
            ModelNotFoundError
            VisuNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectAllUsers(self):
        """ Renvoie une liste de tous les utilisateurs
        Returns:
            list<str> des utilisateurs
        """
        raise NotImplementedError( "Should be implemented" )


    def selectAllUserModels(self, user):
        """ Renvoie une liste de tous les modèles sauvegardés pour un utilisateur
        Args:
            user = nom de l'utilsateur (str)
        Returns:
            list<str> de noms de modèles
        Raises:
            UserNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectAllUserModelVis(self, user, model_name):
        """ Renvoie une liste de toutes les classes de visualisations effectuées sur un modèle
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
        Returns:
            list<str> de visualisation
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )

    def selectAllUserModelVisImg(self, user, model_name, vis):
        """ Renvoie une liste de toutes les images sauvegardées d'un utilisateur pour une visualisation
        Args:
            user = nom de l'utilsateur (str)
            model_name = nom du model (str)
            vis = nom de la visualisation (str)
        Returns:
            list<str> de noms d'images
        Raises:
            UserNotFoundError
            ModelNotFoundError
        """
        raise NotImplementedError( "Should be implemented" )
