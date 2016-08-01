from __future__ import print_function

import io
import os
import sys

from googleapiclient.errors import HttpError
from googleapiclient.http import MediaIoBaseDownload

from utils import datetime_from_string


class File:
    """Represents a File in Google Drive"""
    GOOGLE_DOC_PREFIX = "application/vnd.google-apps."

    def __init__(self, name, id, path, type, last_modified=None):
        self.name = name
        self.id = id
        self.path = path
        self.type = type
        self.last_modified = last_modified

    @classmethod
    def create_from_json(cls, json, path, service=None):
        """
        Creates a File from a json object
        Args:
            json (): the file in json form
            path (): the path of the folder
            service (): the Drive Service

        Returns: a :class:File specified by json

        """
        if 'name' not in json or 'id' not in json:
            raise BaseException("Not valid item")
        drive_file = File(name=json['name'], id=json['id'], path=path + os.path.sep + json['name'],
                          type=json['mimeType'],
                          last_modified=json['modifiedTime'])
        drive_file.get(service)
        return drive_file

    def _get_doc(self, service):
        """Downloads this file. Only called if this is a Google Doc"""
        # TODO: Add in downloading google docs
        pass

    def _download(self, request):
        """ Downloads this file.
        :param request: the API request that specifies the type of file to download
        """
        try:
            fh = io.FileIO(self.path, mode='w')
            downloader = MediaIoBaseDownload(fh, request)
            done = False
            sys.stdout.write("\n")
            sys.stdout.flush()
            print("Downloading %s" % self)
            while not done:
                status, done = downloader.next_chunk()
                sys.stdout.write("\rDownloaded {0}%".format(int(status.progress() * 100)))
                sys.stdout.flush()
            fh.close()
            cloud_edit_time = datetime_from_string(self.last_modified)
            os.utime(self.path, (cloud_edit_time, cloud_edit_time))
        except HttpError:
            print("Couldn't download %s" % self.path)
            return None

    def _get_file(self, service):
        """Downloads this file. Only called if this is a file"""
        if not os.path.exists(self.path):
            request = service.files().get_media(fileId=self.id)
            self._download(request)

    def get(self, service):
        """Downloads this file"""
        if File.GOOGLE_DOC_PREFIX in self.type:
            self._get_doc(service)
        else:
            self._get_file(service)

    def __str__(self):
        return self.name + " Modified: " + self.last_modified
