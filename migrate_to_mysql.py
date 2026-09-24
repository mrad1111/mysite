import os
import sys
import subprocess
import argparse
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / '.env')
except ImportError:
    pass

def main():
    parser = argparse.ArgumentParser(description="Migrate the SQLite store to MySQL.")
    parser.add_argument(
        "--force-data",
        action="store_true",
        help="Replace existing MySQL data with the SQLite export.",
    )
    args = parser.parse_args()

    print("=" * 60)
    print("   SQLite -> MySQL Database Migration Utility for Django")
    print("=" * 60)

    db_engine = os.environ.get('DB_ENGINE', 'mysql').lower()
    db_name = os.environ.get('MYSQL_DATABASE', 'arkan_store')
    db_user = os.environ.get('MYSQL_USER', 'root')
    db_password = os.environ.get('MYSQL_PASSWORD', '')
    db_host = os.environ.get('MYSQL_HOST', '127.0.0.1')
    db_port = int(os.environ.get('MYSQL_PORT', '3307'))

    print(f"\nConfiguration loaded from .env:")
    print(f" - DB_ENGINE: {db_engine}")
    print(f" - MYSQL_DATABASE: {db_name}")
    print(f" - MYSQL_USER: {db_user}")
    print(f" - MYSQL_HOST: {db_host}")
    print(f" - MYSQL_PORT: {db_port}")

    # 1. Export SQLite data to JSON
    json_dump_path = BASE_DIR / "sqlite_data.json"
    print(f"\n[Step 1/4] Dumping data from SQLite (db.sqlite3)...")
    env_sqlite = os.environ.copy()
    env_sqlite['DB_ENGINE'] = 'sqlite'
    dump_cmd = [
        sys.executable, "manage.py", "dumpdata",
        "--natural-foreign", "--natural-primary",
        "--exclude", "contenttypes",
        "--exclude", "auth.Permission",
        "--indent", "2",
        "-o", str(json_dump_path)
    ]
    try:
        res = subprocess.run(dump_cmd, cwd=BASE_DIR, env=env_sqlite, check=True)
        print(f"  [OK] Exported SQLite data to {json_dump_path.name}")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Failed to dump SQLite data: {e}")
        return

    # 2. Check MySQL connection & create database if missing
    print(f"\n[Step 2/4] Connecting to MySQL server at {db_host}:{db_port}...")
    try:
        import MySQLdb
        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            port=db_port
        )
        cursor = conn.cursor()
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;")
        conn.commit()
        cursor.close()
        conn.close()
        print(f"  [OK] Connected to MySQL server and verified database '{db_name}'.")
    except Exception as e:
        print(f"\n  [ERROR] Could not connect to MySQL server:")
        print(f"    Error: {e}")
        print("\n  --> TROUBLESHOOTING:")
        print("      1. Make sure your MySQL Server / XAMPP / WampServer is running.")
        print("      2. Verify your database credentials in the '.env' file.")
        print("      3. Run this script again: py migrate_to_mysql.py\n")
        return

    # 3. Run migrations on MySQL
    print(f"\n[Step 3/4] Running Django migrations on MySQL...")
    env_mysql = os.environ.copy()
    env_mysql['DB_ENGINE'] = 'mysql'
    try:
        subprocess.run([sys.executable, "manage.py", "migrate"], cwd=BASE_DIR, env=env_mysql, check=True)
        print("  [OK] Migrations applied successfully.")
    except subprocess.CalledProcessError as e:
        print(f"  [ERROR] Migration failed: {e}")
        return

    # 4. Import only into an empty target so rerunning this utility does not
    # overwrite product images or other changes made in the admin.
    print(f"\n[Step 4/4] Importing data from {json_dump_path.name} into MySQL...")
    try:
        import MySQLdb

        conn = MySQLdb.connect(
            host=db_host,
            user=db_user,
            passwd=db_password,
            port=db_port,
            db=db_name,
        )
        cursor = conn.cursor()
        cursor.execute("SELECT COUNT(*) FROM home_product")
        has_products = cursor.fetchone()[0] > 0
        cursor.close()
        conn.close()

        if has_products and not args.force_data:
            print("  [SKIP] MySQL already contains products; existing data was preserved.")
        else:
            subprocess.run(
                [sys.executable, "manage.py", "loaddata", json_dump_path.name],
                cwd=BASE_DIR,
                env=env_mysql,
                check=True,
            )
            print("  [OK] Data imported successfully into MySQL!")
    except Exception as e:
        print(f"  [ERROR] Data import failed: {e}")
        return


    # 5. Check Django system check
    print(f"\n[Verification] Running Django system check...")
    subprocess.run([sys.executable, "manage.py", "check"], cwd=BASE_DIR, env=env_mysql)

    print("\n" + "=" * 60)
    print(" SUCCESS! Your database has been successfully converted to MySQL.")
    print(" You can now run the app with: py manage.py runserver")
    print("=" * 60 + "\n")

if __name__ == '__main__':
    main()
