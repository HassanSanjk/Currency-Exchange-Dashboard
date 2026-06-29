import time

from redis_client import get_redis_client

MAX_DAYS = 30


def _history_key(base, target, source):
    return f"history:{base}:{target}:{source}"


def save_snapshot(base, target, source, rate):
    client = get_redis_client()
    key = _history_key(base, target, source)
    now = time.time()
    cutoff = now - MAX_DAYS * 86400
    pipe = client.pipeline()
    pipe.zremrangebyscore(key, "-inf", cutoff)
    pipe.zadd(key, {rate: now})
    pipe.execute()


def get_history(base, target, source):
    client = get_redis_client()
    key = _history_key(base, target, source)
    now = time.time()
    cutoff = now - MAX_DAYS * 86400
    results = client.zrangebyscore(key, cutoff, now, withscores=True)
    return [{"rate": float(r), "timestamp": int(s)} for r, s in results]
