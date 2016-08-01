from __future__ import print_function

import os

from file import File
from utils import mkdir_if_nexists

# Prefix used to denote a Google App File (Doc, Sheet, ...)
MIME_FOLDER = "application/vnd.google-apps.folder"


class Folder(File):
    """Represents a folder in Google Drive"""

    def __init__(self, name, id, path, type, service=None, last_modified=None):
        File.__init__(self, name, id, path, type, last_modified=last_modified)
        self.get(service)
        if service is not None:
            self.get(service)
            self.children = self._get_children(service)

    @classmethod
    def create_from_json(cls, json, path, service=None):
        """
        Creates a Folder from a json object
        Args:
            json (): the folder in json form
            path (): the path of the folder
            service (): the Drive Service

        Returns: a :class:Folder specified by json

        """
        if 'name' not in json or 'id' not in json:
            raise BaseException("Not valid item")
        return Folder(name=json['name'], id=json['id'], path=path + os.path.sep + json['name'], type=json['mimeType'],
                      service=service, last_modified=json['modifiedTime'])

    def _get_children(self, service):
        children = True
        page_token = ''
        children_list = []
        while children:
            results = service.files().list(corpus='user', orderBy='folder', pageToken=page_token,
                                           q="'" + self.id + "' in parents and trashed = false",
                                           fields="nextPageToken, files(name, id, mimeType, modifiedTime)").execute()

            children = results.get('files', [])
            for child in children:
                if child['mimeType'] == MIME_FOLDER:
                    children_list.append(Folder.create_from_json(child, self.path, service))
                else:
                    children_list.append(File.create_from_json(child, self.path, service))
            page_token = results.get('nextPageToken', '')
            if page_token is '':
                children = False
        return children_list

    def get_children(self):
        """

        Returns: a list of File that represent the contents of the folder

        """
        return self.children

    def get(self, service=None):
        """
        Creates this file if it doesn't exist.
        Args:
            service ():
        """
        mkdir_if_nexists(self.path)

    def __str__(self):
        return "Folder: " + File.__str__(self)
