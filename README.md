
将scrapy 的cache 存储在阿里云oss,使spder集群能够统一存取缓存

setting配置说明

HTTPCACHE_DIR='/path/to/cache'

HTTPCACHE_ENABLED=True

HTTPCACHE_STORAGE='dianpin_scrapy.misc.httpcache.OssCacheStorage'

OSS_CACHE_BUCKET='YOUR_OSS_CACHE_BUCKET'

OSS_ACCESSKEY='YOUR_OSS_ACCESSKEY'

OSS_SECRETKEY='YOUR_OSS_SECRETKEY'

OSS_ENDPOINT='OSS_ENDPOINT'
