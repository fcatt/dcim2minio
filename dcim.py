import os
from glob import glob
from pathlib import Path
from pathlib import PurePath
from config import *
import uuid


def picture_is_original(file_path):
    """Some cameras can save both raw and JPEG files for the same picture. This checks if the file is the
    original (usually best quality) picture or the JPEG copy. If there is only a JPEG file, it is indeed the
    original file. """
    if file_path.upper().endswith('.JPG'):
        for dot_ext in dot_exts:
            if os.path.isfile(PurePath(file_path).with_suffix(dot_ext)):
                return False
        return True
    elif file_path.endswith(dot_exts):
        return True
    else:
        return False


class DCIM:
    def __init__(self, media_source):
        self._media_source = media_source
        self._exts = exts
        self._uuid_subdir = 'MISC/CONFERO'.upper()
        self._uuid_file = "UUID.TXT".upper()
        self._uuid_dir = os.path.join(self._media_source, self._uuid_subdir)
        self._uuid_path = os.path.join(self._uuid_dir, self._uuid_file)
        source_uuid = self.read_source_uuid()
        if source_uuid is not None:
            self._source_uuid = source_uuid
        else:
            self._source_uuid = self.write_source_uuid()

    def read_source_uuid(self):
        """Read the UUID value from the storage card"""
        vprint("Readind UUID @", self._uuid_path)
        try:
            uuid_handler = open(self._uuid_path, "r")
            source_uuid = uuid_handler.readline(36)
            uuid_handler.close()
            vprint("source UUID:", source_uuid)
            return source_uuid
        except:
            vprint("UUID missing or empty")
            return None

    def write_source_uuid(self):
        """Write the UUID value to the storage card"""
        vprint("Writing source UUID @", self._uuid_path)
        try:
            source_uuid = str(uuid.uuid4())
            vprint("Source UUID:", source_uuid)
            Path(self._uuid_dir).mkdir(parents=True, exist_ok=True)
            uuid_handler = open(self._uuid_path, "w")
            uuid_handler.write(source_uuid)
            uuid_handler.close()
            return source_uuid
        except:
            raise

    @property
    def get_uuid(self):
        """Get the UUID value"""
        return self._source_uuid

    def get_files(self):
        """Get the pictures from the storage card"""
        files = []
        for file in glob(
                os.path.join(
                    self._media_source,
                    "DCIM",
                    "[0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_]",
                    "[0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9A-Z_][0-9][0-9][0-9][0-9].[0-9A-Z_][0-9A-Z_][0-9A-Z_]"),
                recursive=True):
            if os.path.isfile(file) and os.path.getsize(file) > 0 and picture_is_original(file):
                files.append(file)
        return files
