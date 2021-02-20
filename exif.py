import exiftool
from datetime import datetime
from config import *


exif_server = exiftool.ExifTool()
if config.has_option('tools', 'exiftool_exec'):
    exiftool_executable = config['tools']['exiftool_exec']
    exif_server.executable = exiftool_executable
    vprint("Exiftool executable:", exiftool_executable)
exif_server.start()


def read_exif_datetime(file_name):
    """Pictures and movies don't use the same metadata tags to store the create date & time.
    Tags are defined in the configuration file for each file extension."""
    tag = 'EXIF:DateTimeOriginal'
    for ext in exts:
        if file_name.upper().endswith(ext.upper()):
            tag = fileinfo[ext]['exif_datetime']
    return datetime.strptime(exif_server.get_tag(tag, file_name), '%Y:%m:%d %H:%M:%S').strftime('%Y-%m-%d %H:%M:%S')
