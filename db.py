import mysql.connector
from flask import current_app
from datetime import datetime, timedelta


def get_db_connection():
    return mysql.connector.connect(
        host=current_app.config["MYSQL_HOST"],
        port=current_app.config["MYSQL_PORT"],
        user=current_app.config["MYSQL_USER"],
        password=current_app.config["MYSQL_PASSWORD"],
        database=current_app.config["MYSQL_DB"],
    )


def get_cached_rate(base, target, source, max_age_hours=24):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    query = """
        SELECT rate, updated_at
        FROM rate_cache
        WHERE base_currency = %s
          AND target_currency = %s
          AND source = %s
        LIMIT 1
    """

    cursor.execute(query, (base, target, source))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    if not row:
        return None

    updated_at = row["updated_at"]
    if datetime.now() - updated_at > timedelta(hours=max_age_hours):
        return None

    return float(row["rate"])


def save_rate(base, target, source, rate):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        INSERT INTO rate_cache (base_currency, target_currency, source, rate, updated_at)
        VALUES (%s, %s, %s, %s, NOW())
        ON DUPLICATE KEY UPDATE
            rate = VALUES(rate),
            updated_at = NOW()
    """

    cursor.execute(query, (base, target, source, rate))
    conn.commit()

    cursor.close()
    conn.close()

def get_last_updated(base, target, source):
    conn = get_db_connection()
    cursor = conn.cursor()

    query = """
        SELECT updated_at
        FROM rate_cache
        WHERE base_currency = %s
          AND target_currency = %s
          AND source = %s
        LIMIT 1
    """

    cursor.execute(query, (base, target, source))
    row = cursor.fetchone()

    cursor.close()
    conn.close()

    return str(row[0]) if row else None