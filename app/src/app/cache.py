from os import environ

ENABLE_CACHE = environ.get("DEV_CACHE", None) == "1"

if ENABLE_CACHE:
    import os
    import sys

    import percache

    _cache_path = os.path.join(sys.path[0], ".percache")

    Cache = percache.Cache(_cache_path, livesync=True)

    print(f"!! Cache enabled: {_cache_path}.db ", file=sys.stderr)
else:
    Cache = lambda x: x
