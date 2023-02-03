from flask_caching import Cache

cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': 'storage/cache',
    'CACHE_DEFAULT_TIMEOUT': 3600,
})
