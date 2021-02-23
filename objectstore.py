from minio import Minio
import io


class ObjectStore:
    def __init__(self, host, bucket, access_key, secret_key, region):
        self._bucket = bucket
        self._conn = Minio(host, access_key=access_key, secret_key=secret_key, region=region)
        found = self._conn.bucket_exists(bucket)
        if not found:
            quit('Minio: Unable to connect to ' + host + '/' + bucket)

    def upload_object(self, file_path, object_name, mimetype):
        try:
            upload = self._conn.fput_object(self._bucket, object_name, file_path, content_type=mimetype)
            return upload.etag
        except:
            return None

    def upload_binary(self, data, object_name, mimetype):
        try:
            upload = self._conn.put_object(self._bucket, object_name, io.BytesIO(data), len(data), mimetype)
            return upload.etag
        except:
            raise

    def get_object_size(self, object_name):
        try:
            return self._conn.stat_object(self._bucket, object_name, ssec=None, version_id=None,
                                          extra_query_params=None).size
        except:
            return None

    def get_object_info(self, object_name):
        try:
            return self._conn.stat_object(self._bucket, object_name, ssec=None, version_id=None,
                                          extra_query_params=None)
        except:
            return None
