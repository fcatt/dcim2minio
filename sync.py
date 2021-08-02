from dcim import *
from exif import *
from objectstore import ObjectStore
from database import Database
from picture import *
import lzma
import os
from shutil import copyfile


def counter(current, total):
    return "[" + str(current) + "/" + str(total) + "]"


def mimetype(file_name):
    ext = os.path.splitext(file_name)[1].upper().replace('.', '')
    if ext == 'JPG':
        return 'image/jpeg'
    else:
        return fileinfo[ext]['mimetype']


if __name__ == '__main__':
    media_source = args.source
    vprint("verbosity turned on")
    print("Media source:", media_source)
    vprint("Managed extensions:", str(exts))
    db = Database(config['sqlite3']['db_file'])
    storage = ObjectStore(config['minio']['host'], config['minio']['bucket'], config['minio']['access_key'],
                          config['minio']['secret_key'], config['minio']['region'])
    vprint("ExifTool running:", exif_server.running)
    dcim = DCIM(media_source)
    dcim_uuid = dcim.get_uuid
    print("Files to process: ", end='', flush=True)
    files = dcim.get_files()
    print(str(len(files)))
    file_count = 0
    for file in files:
        file_count += 1
        count = counter(file_count, len(files))
        picture = Picture(file, dcim_uuid, mimetype(file))
        picture_info = db.read_picture_info(picture)
        if picture_info is None:
            vprint(count, "New file:", file)
            picture.set_exif_datetime(read_exif_datetime(file))
            picture.generate_object_name()
            db.write_picture_info(picture)
        picture_info = db.read_picture_info(picture)
        if picture_info and picture_info['object_etag'] is None:
            picture.set_object_name(picture_info['object_name'])
            object_size = storage.get_object_size(picture.get_object_name)
            if picture.already_uploaded(object_size) is False:
                print(count, " Uploading", picture.get_object_name, "… ", end='', flush=True)
                etag = storage.upload_object(file, picture.get_object_name, picture.get_mimetype)
                if etag:
                    picture.set_object_etag(etag)
                    db.write_object_etag(picture)
                    print("OK")
                    if args.localcopy and config['local']['pictures_basedir']:
                        print(count, " Copying", picture.get_object_name, "… ", end='', flush=True)
                        local_path = os.path.join(config['local']['pictures_basedir'], picture.get_object_name)
                        os.makedirs(os.path.dirname(local_path), exist_ok=True)
                        copyfile(file, local_path)
                        print("OK")
                else:
                    print("ERROR")
            else:
                print(count, picture.get_object_name, "already uploaded, updating database")
                picture.set_object_etag(storage.get_object_info(picture.get_object_name).etag)
                db.write_object_etag(picture)
        else:
            vprint(count, file, '==', picture_info['object_name'])
    exif_server.terminate()

    if args.backupdb:
        db = open(config['sqlite3']['db_file'], 'rb')
        remotename = os.path.basename(config['sqlite3']['db_file']) + '.xz'
        etag = storage.upload_binary(lzma.compress(db.read()), remotename, 'application/x-xz')
        if etag:
            print("Database uploaded, etag:", etag)
        else:
            print("Database NOT uploaded!")

    print('End of processing')
