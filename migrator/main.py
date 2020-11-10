from multiprocessing import Pool, freeze_support
from urllib.parse import urlparse

import click
import redis
import re
from tqdm import tqdm

count = 2500


def parse_uri(uri):
    """Extracts the host, port and db from an uri"""
    uri = uri if re.match('^redis', uri) else 'redis://{}'.format(uri)
    uri = urlparse(uri)
    host = uri.hostname or 'localhost'
    port = uri.port or 6379
    db = re.match('/([0-9]+)', uri.path).group(1) if re.match('/([0-9]+)', uri.path) else 0
    password = uri.password or None
    return host, int(port), int(db), password


def combine_uri(host, port, db):
    """Combines the host, port and db into an uri"""
    return '{}:{}/{}'.format(host, port, db)


def shorten(uri):
    """Makes a given uri a 10-character string"""
    return '{}...{}'.format(uri[:5], uri[-2:])


def migrate(src, dst, db=None, replace=True, barpos=0):
    """Migrates dataset of a db from source host to destination host"""
    srchost, srcport, srcdb, srcpass = parse_uri(src)
    dsthost, dstport, dstdb, dstpass = parse_uri(dst)

    if db is not None:
        srcdb = dstdb = db
        src = combine_uri(srchost, srcport, srcdb)
        dst = combine_uri(dsthost, dstport, dstdb)

    srcr = redis.StrictRedis(host=srchost, port=srcport, db=srcdb, charset='utf8', password=srcpass)
    dstr = redis.StrictRedis(host=dsthost, port=dstport, db=dstdb, charset='utf8', password=dstpass)

    with tqdm(total=srcr.dbsize(), ascii=True, unit='keys', unit_scale=True, position=barpos) as pbar:
        pbar.set_description('{} → {}'.format(shorten(src), shorten(dst)))
        cursor = 0
        while True:
            cursor, keys = srcr.scan(cursor, count=count)
            pipeline = srcr.pipeline(transaction=False)
            for key in keys:
                pipeline.pttl(key)
                pipeline.dump(key)
            dumps = pipeline.execute()

            pipeline = dstr.pipeline(transaction=False)
            for key, ttl, data in zip(keys, dumps[::2], dumps[1::2]):
                if data != None:
                    pipeline.restore(key, ttl if ttl > 0 else 0, data, replace=replace)
            pbar.update(len(keys))

            results = pipeline.execute(False)
            for key, result in zip(keys, results):
                if result not in (b'OK', b'BUSYKEY Target key name already exists.'):
                    raise Exception('Migration failed on key {}: {}'.format(key, result))

            if cursor == 0:
                break


def migrate_all(src, dst, replace=True, nprocs=1):
    """Migrates entire dataset from source host to destination host using multiprocessing"""
    srchost, srcport, db, srcpass = parse_uri(src)
    srcr = redis.StrictRedis(host=srchost, port=srcport, charset='utf8', password=srcpass)
    keyspace = srcr.info('keyspace')

    freeze_support()  # for Windows support
    pool = Pool(processes=min(len(keyspace.keys()), nprocs))
    pool.starmap(migrate, [(src, dst, int(db[2:]), replace, i) for i, db in enumerate(keyspace.keys())])
    print('\n' * max(0, len(keyspace.keys())-1))


@click.command(name='redis-migrate')
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
@click.option('--replace/--no-replace', default=True, help='Whether to replace the existing key')
@click.option('--all-keys', is_flag=True, default=False, help='Whether to migrate all dataset/keys')
@click.option('--nprocs', nargs=1, type=int, default=1, help='Maximum number of processes')
def main(src, dst, replace, all_keys, nprocs):
    """
src: redis://[:password@]hostname[:port][/database] or [:password@]hostname[:port][/database]

dst: redis://[:password@]hostname[:port][/database] or [:password@]hostname[:port][/database]
"""
    if all_keys:
        migrate_all(src, dst, replace=replace, nprocs=nprocs)
    else:
        migrate(src, dst, replace=replace)
