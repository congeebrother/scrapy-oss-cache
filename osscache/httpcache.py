# -*- coding: utf-8 -*-
#__author__ = 'daniel liu'
#__email__ = 'daniel_001@126.com'

import pickle
import os
import logging
from time import time
import oss2
from scrapy.exceptions import NotConfigured
from scrapy.responsetypes import responsetypes
from scrapy.extensions.httpcache import FilesystemCacheStorage
from scrapy.http import Headers
from scrapy.utils.project import data_path
from w3lib.http import headers_raw_to_dict




class OssCacheStorage(FilesystemCacheStorage):
    def __init__(self, settings):
        super(OssCacheStorage, self).__init__(settings)
        self.cachedir = data_path(settings['HTTPCACHE_DIR'])
        self.oss_access_key = settings['OSS_ACCESSKEY']
        self.oss_secret_key = settings['OSS_SECRETKEY']
        self.bucket_name = settings['OSS_CACHE_BUCKET']
        self.end_point=settings['OSS_ENDPOINT']
        if self.bucket_name is None:
            raise NotConfigured("OSSCACHE_BUCKET must be specified")
        self._conn = None

    @property
    def conn(self):
        if self._conn is None:
            self.auth = oss2.Auth(self.oss_access_key, self.oss_secret_key)
            self._conn = oss2.Bucket(self.auth, self.end_point, self.bucket_name )
        return self._conn


    def store_response(self, spider, request, response):
        '''
        cache response to oss
        :param spider:
        :param request:
        :param response:
        :return:
        '''
        super(OssCacheStorage, self).store_response(spider, request, response)
        rpath = self._get_request_path(spider, request)
        if not os.path.exists(rpath):
            os.makedirs(rpath)
        metadata = {
            'url': request.url,
            'method': request.method,
            'status': response.status,
            'response_url': response.url,
            'timestamp': time(),
        }
        for root, dirs, filenames in os.walk(rpath):
            for filename in filenames:
                local_file = os.path.join(root, filename)
                remote_file = os.path.relpath(local_file, self.cachedir).lower()
                self.conn.put_object_from_file(remote_file, local_file)

    def retrieve_response(self, spider, request):
        '''
        get cache from oss if it exits
        :param spider:
        :param request:
        :return:
        '''
        response = super(OssCacheStorage, self).retrieve_response(spider, request)
        # not in local filesystem cache, so try copying from OSS
        if response is None:
            local_path = self._get_request_path(spider, request)
            remote_path = os.path.relpath(local_path, self.cachedir).lower()

            def _get_ossfile(filename):
                '''
                get  ossfile object
                :param filename:
                :return: ossfile object
                '''
                remote_file = os.path.join(remote_path, filename)
                try:
                    return self.conn.get_object(remote_file )
                except Exception:
                    pass






            # check if the key exists
            metadata_key = _get_ossfile('pickled_meta')
            if metadata_key is None:
                return None

            body = _get_ossfile('response_body').read()
            rawheaders = _get_ossfile('response_headers').read()
            # check if the cache entry has expired
            mtime = metadata_key.last_modified
            if 0<self.expiration_secs <int(time()) - mtime:
                return None  # expired
            metadata = pickle.loads(metadata_key.read())
            url = metadata.get('response_url')
            status = metadata['status']
            headers = Headers(headers_raw_to_dict(rawheaders))
            respcls = responsetypes.from_args(headers=headers, url=url)
            response = respcls(url=url, headers=headers, status=status, body=body)
        return response


