import sqlite3
from picture import *


class Database:
    def __init__(self, name):
        self._conn = sqlite3.connect(name)
        self._cursor = self._conn.cursor()
        self.execute("CREATE TABLE IF NOT EXISTS picture ("
                     "dcim_uuid TEXT, "
                     "file_relpath TEXT NOT NULL, "
                     "file_datetime DATETIME NOT NULL, "
                     "file_size INT NOT NULL, "
                     "object_name TEXT UNIQUE NOT NULL, "
                     "object_etag TEXT UNIQUE)")
        self.execute(
            "CREATE UNIQUE INDEX IF NOT EXISTS file_index "
            "ON picture (file_relpath, file_datetime, file_size)")
        self.commit()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def query(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def read_picture_info(self, picture: Picture):
        query = "SELECT file_relpath, file_datetime, file_size, object_name, object_etag FROM picture WHERE " \
                "file_relpath = ? AND file_datetime = ? AND file_size = ? "
        self.execute(query,
                     (picture.get_file_relpath,
                      picture.get_file_datetime,
                      picture.get_file_size))
        row = self.fetchone()
        if row:
            return {'file_relpath': row[0],
                    'file_datetime': row[1],
                    'file_size': row[2],
                    'object_name': row[3],
                    'object_etag': row[4]}
        else:
            return None

    def write_picture_info(self, picture: Picture):
        query = 'INSERT INTO picture (dcim_uuid, file_relpath, file_datetime, file_size, object_name) VALUES (?, ?, ' \
                '?, ?, ?) '
        self.execute(query,
                     (picture.get_dcim_uuid,
                      picture.get_file_relpath,
                      picture.get_file_datetime,
                      picture.get_file_size,
                      picture.get_object_name),)
        self.commit()

    def write_object_name(self, picture: Picture):
        query = 'UPDATE picture SET object_name = ? WHERE file_relpath = ? AND file_size = ? AND file_datetime = ?'
        self.execute(query,
                     (picture.get_object_name,
                      picture.get_file_relpath,
                      picture.get_file_size,
                      picture.get_file_datetime))
        self.commit()

    def write_object_etag(self, picture: Picture):
        query = 'UPDATE picture SET object_etag = ? WHERE object_name = ?'
        self.execute(query,
                     (picture.get_object_etag,
                      picture.get_object_name))
        self.commit()

    def screwed_write_objectetag_filedate(self, picture: Picture):
        query = 'UPDATE picture SET object_etag = ? AND file_datetime = ? WHERE object_name = ?'
        self.execute(query, (picture.get_object_etag, picture.get_file_datetime, picture.get_object_name))

    def screwed_read_pictureinfo(self, picture: Picture):
        query = "SELECT file_relpath, file_datetime, file_size, object_name, object_etag FROM picture WHERE " \
                "file_relpath = ? AND file_size = ? "
        self.execute(query, (picture.get_file_relpath, picture.get_file_size))
        row = self.fetchone()
        if row:
            return {'file_relpath': row[0],
                    'file_datetime': row[1],
                    'file_size': row[2],
                    'object_name': row[3],
                    'object_etag': row[4]}
        else:
            return None
