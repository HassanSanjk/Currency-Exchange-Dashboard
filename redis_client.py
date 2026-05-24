import redis
from flask import current_app
from datetime import datetime


def get_redis_client():
    return redis.Redis.from_url(current_app.config["REDIS_URL"])


def _rate_key(base, target, source):
    return f"rate:{base}:{target}:{source}"


def _updated_key(base, target, source):
    return f"rate:{base}:{target}:{source}:updated"


def get_cached_rate(base, target, source):
    client = get_redis_client()
    key = _rate_key(base, target, source)
    value = client.get(key)
    if value is not None:
        return float(value)
    return None


def save_rate(base, target, source, rate, max_age_hours=24):
    client = get_redis_client()
    key = _rate_key(base, target, source)
    updated_key = _updated_key(base, target, source)
    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    ttl = max_age_hours * 3600
    client.setex(key, ttl, rate)
    client.setex(updated_key, ttl, now)


def get_last_updated(base, target, source):
    client = get_redis_client()
    key = _updated_key(base, target, source)
    value = client.get(key)
    if value is not None:
        return value.decode("utf-8")
    return None
