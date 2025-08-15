# db.py
import psycopg2
from psycopg2.extras import RealDictCursor
import logging
import json
from datetime import datetime

# logging setup 
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# connection params 
DB_CONFIG = {
    "host": "localhost",
    "port": 5428,
    "dbname": "mydatabase",
    "user": "user",
    "password": "12345",  # как в Docker
}

def get_connection():
    """creates connection to PostgreSQL"""
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        logger.info("✅ Sucessfully connected to PostgreSQL")
        return conn
    except Exception as e:
        logger.error(f"❌ Connection to PostgreSQL failed: {e}")
        raise

def init_db():
    """creating tables vulnerabilities and products"""
    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # vulnerabilities table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vulnerabilities (
                version_id SERIAL PRIMARY KEY,
                vendor VARCHAR(50),
                product_name VARCHAR(50),
                kla_id VARCHAR(16),
                description VARCHAR(250),
                publish_date DATE,
                start_vuln_version VARCHAR(20),
                fixed_version VARCHAR(20)
            );
        """)

        # products table
        cur.execute("""
            CREATE TABLE IF NOT EXISTS products (
                product_id SERIAL PRIMARY KEY,
                vendor VARCHAR(50),
                product_name VARCHAR(50),
                version VARCHAR(20)
            );
        """)

        conn.commit()
        cur.close()
        logger.info("✅ tables 'vulnerabilities' and 'products' were sucessfully created or already exists")
    except Exception as e:
        logger.error(f"❌ Error while creating tables: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def import_vulnerabilities(json_file_path):
    """Loads data to vulnerabilities table from JSON"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"❌ File not found: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"❌JSON parse error: {e}")
        return

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # cur.execute("DELETE FROM vulnerabilities;")

        insert_query = """
            INSERT INTO vulnerabilities 
            (vendor, product_name, kla_id, description, publish_date, start_vuln_version, fixed_version)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
        """

        for item in data:
            cur.execute(insert_query, (
                item.get("vendor"),
                item.get("product"),  
                item.get("KLA_id"),
                item.get("description"),
                item.get("publish_date"),
                item.get("start_vuln_version"),
                item.get("fixed_version")
            ))

        conn.commit()
        logger.info(f"✅ Loaded {len(data)} rows to 'vulnerabilities' table")
    except Exception as e:
        logger.error(f"❌ General problems with loading to vulnerabilities table: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

def import_products(json_file_path):
    """inserts data to versions table from external json file"""
    try:
        with open(json_file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        logger.error(f"❌ File not found: {json_file_path}")
        return
    except json.JSONDecodeError as e:
        logger.error(f"❌ JSON parse error: {e}")
        return
    except Exception:
        logger.error(f"❌ JSON general error: {e}")
        pass

    conn = None
    try:
        conn = get_connection()
        cur = conn.cursor()

        # cleaning table 
        # cur.execute("DELETE FROM products;")

        insert_query = """
            INSERT INTO products (vendor, product_name, version)
            VALUES (%s, %s, %s)
        """

        for item in data:
            cur.execute(insert_query, (
                item.get("vendor"),
                item.get("product"),  # product → product_name
                item.get("version")
            ))

        conn.commit()
        logger.info(f"✅ Loaded {len(data)} rows to table 'products'")
    except Exception as e:
        logger.error(f"❌ General problems with loading to products table: {e}")
        if conn:
            conn.rollback()
    finally:
        if conn:
            conn.close()

