import os
from pathlib import PurePath
from datetime import datetime


class Picture:
    def __init__(self, file_path, dcim_uuid, mimetype):
        self._file_path = file_path
        self._dcim_uuid = dcim_uuid
        pure_path = PurePath(self._file_path)
        self._file_relpath = os.path.join(pure_path.parts[-2], pure_path.name)
        file_stats = os.stat(file_path)
        self._file_datetime = datetime.utcfromtimestamp(file_stats.st_ctime).strftime('%Y-%m-%d %H:%M:%S')
        self._file_size = file_stats.st_size
        self._file_name = pure_path.name
        self._exif_datetime = None
        self._object_name = None
        self._object_etag = None
        self._mimetype = mimetype

    @property
    def get_mimetype(self):
        """Get the mime type of the picture"""
        return self._mimetype

    @property
    def get_file_path(self):
        """Get the full path of the file"""
        return self._file_path

    @property
    def get_dcim_uuid(self):
        """Get the DCIM UUID string"""
        return self._dcim_uuid

    @property
    def get_file_relpath(self):
        """Get the combined path of the subdir and the file name"""
        return self._file_relpath

    @property
    def get_file_datetime(self):
        """Get the file modification date & time"""
        return self._file_datetime

    @property
    def get_file_size(self):
        """Get the file size in bytes"""
        return self._file_size

    @property
    def get_file_name(self):
        """Get the file name"""
        return self._file_name

    @property
    def get_exif_datetime(self):
        """Get the EXIF creation date & time"""
        return self._exif_datetime

    @property
    def get_object_name(self):
        """Get the object name"""
        return self._object_name

    @property
    def get_object_etag(self):
        """Get the object last modified date & time"""
        return self._object_etag

    def already_uploaded(self, object_size):
        """Compare the file size and the remote object size"""
        return object_size == self._file_size

    def set_mimetype(self, mimetype):
        """Set the mime type of the picture"""
        self._mimetype = mimetype

    def set_exif_datetime(self, exif_datetime):
        """Set the EXIF creation date & time"""
        self._exif_datetime = exif_datetime

    def set_object_name(self, object_name):
        """Generate the object name from the exif date & time and the file name"""
        self._object_name = object_name

    def generate_object_name(self):
        """Generate the object name from the exif date & time and the file name"""
        self._object_name = datetime.strptime(
            self._exif_datetime, '%Y-%m-%d %H:%M:%S').strftime('%Y/%m/%d/%H%M%S')+'_'+self._file_name.upper()
        return self._object_name

    def set_object_etag(self, object_etag):
        """Set the object etag (after successful lupload)"""
        self._object_etag = object_etag
