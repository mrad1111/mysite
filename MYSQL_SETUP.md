# MySQL Setup & Migration Guide

This project supports both **SQLite** and **MySQL**.

## Quick Start (Automated Migration)

1. Make sure your MySQL Server (XAMPP, WAMP, MySQL Workbench, or Docker) is running.
2. Edit the `.env` file in the project root with your MySQL credentials:
   ```ini
   DB_ENGINE=mysql
   MYSQL_DATABASE=arkan_store
   MYSQL_USER=root
   MYSQL_PASSWORD=your_mysql_password
   MYSQL_HOST=127.0.0.1
   MYSQL_PORT=3306
   ```
3. Run the automated migration script in your terminal:
   ```powershell
   py migrate_to_mysql.py
   ```
4. Start your Django server:
   ```powershell
   py manage.py runserver
   ```

---

## Manual Step-by-Step Migration (Alternative)

If you prefer to perform each step manually:

1. **Create Database in MySQL** (via phpMyAdmin or MySQL CLI):
   ```sql
   CREATE DATABASE arkan_store CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Install Dependencies**:
   ```powershell
   py -m pip install -r requirements.txt
   ```

3. **Export SQLite Data**:
   ```powershell
   $env:DB_ENGINE = "sqlite"
   py manage.py dumpdata --natural-foreign --natural-primary --exclude contenttypes --exclude auth.Permission --indent 2 -o sqlite_data.json
   ```

4. **Configure `.env`**:
   Ensure `.env` contains `DB_ENGINE=mysql` and your database details.

5. **Migrate & Load Data**:
   ```powershell
   py manage.py migrate
   py manage.py loaddata sqlite_data.json
   py manage.py check
   ```

---

## Switching back to SQLite

If you ever need to switch back to SQLite for local development:
In your `.env` file, change:
```ini
DB_ENGINE=sqlite
```
Django will instantly revert to using `db.sqlite3`.