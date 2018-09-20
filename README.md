# Redis Migrate

[![Python Version](https://img.shields.io/badge/python-%3E%3D3.3-blue.svg)](https://docs.python.org/3/index.html) [![Redis Version](https://img.shields.io/badge/redis-%3E%3D2.8-red.svg)](https://redis.io/)

Simple command line tool for redis data migration (minimal functionality)

It is useful when you're not able to use `slaveof` command (e.g. `slaveof` command is not available in ElastiCache) or should migrate from multiple redis servers to a single server.

> It works only for redis >= 2.8

## Installation

```shell
pip install redis-migrate
```

## Usage

```console
# Basic usage
redis-migrate srchost[:port][/db] dsthost[:port][/db] [--all-keys=false] [--nprocs=1]

# Migrate the keys from db 0 of source host to db 1 of destination host.
redis-migrate srchost dsthost/1

# If you don't want to replace existing keys, use `--no-replace` option.
redis-migrate srchost dsthost/1 --no-replace

# Migrate the entire keys from source host at 6380 port to destination host.
# It will ignore `/db` number.
redis-migrate srchost:6380 dsthost --all-keys

# You can also set process number to use multiprocessing for speed up.
# It works only with `--all-keys`.
redis-migrate srchost dsthost --all-keys --nprocs 4
```

## Todo

- [ ] Support redis auth
- [ ] Support key patterns option

## License

MIT
