# PostgreSQL to MySQL Migration Guide

This guide will help you migrate the TJTMS application from Render's PostgreSQL database to a local MySQL server.

## Prerequisites

- MySQL server installed and running
- Python 3.x installed
- Git installed

## Step 1: Set up the MySQL Database

1. Log in to MySQL:
   ```bash
   mysql -u root -p
   ```

2. Create a new database:
   ```sql
   CREATE DATABASE juice_task_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

3. Exit MySQL:
   ```sql
   EXIT;
   ```

## Step 2: Install Required Dependencies

1. Install the MySQL client for Python:
   ```bash
   pip install -r requirements.txt
   ```

## Step 3: Configure Environment Variables

The application now supports switching between PostgreSQL and MySQL using environment variables. To use MySQL:

1. Set the `DATABASE_TYPE` environment variable to `mysql`:

   **On Windows (Command Prompt):**
   ```cmd
   set DATABASE_TYPE=mysql
   ```

   **On Windows (PowerShell):**
   ```powershell
   $env:DATABASE_TYPE = "mysql"
   ```

   **On macOS/Linux:**
   ```bash
   export DATABASE_TYPE=mysql
   ```

2. Optionally, you can customize other database settings:
   ```bash
   export DB_NAME=juice_task_db
   export DB_USER=root
   export DB_PASSWORD=Aamruth@22
   export DB_HOST=localhost
   export DB_PORT=3306
   ```

## Step 4: Migrate the Data

There are two approaches to migrate the data. Choose the one that works best for you:

### Option A: Using Django's Migration System (Recommended)

1. Set up a temporary PostgreSQL database locally:
   ```bash
   createdb temp_juice_db
   ```

2. Import the PostgreSQL dump:
   ```bash
   psql temp_juice_db < juice_db_backup.sql
   ```

3. Temporarily ensure you're using PostgreSQL (unset the DATABASE_TYPE variable):
   ```bash
   # On Windows
   set DATABASE_TYPE=
   
   # On macOS/Linux
   unset DATABASE_TYPE
   ```

4. Create a JSON fixture of all data:
   ```bash
   python manage.py dumpdata --exclude contenttypes --exclude auth.permission > all_data.json
   ```

5. Switch to MySQL:
   ```bash
   # On Windows
   set DATABASE_TYPE=mysql
   
   # On macOS/Linux
   export DATABASE_TYPE=mysql
   ```

6. Run migrations to create the schema in MySQL:
   ```bash
   python manage.py migrate
   ```

7. Load the fixture into MySQL:
   ```bash
   python manage.py loaddata all_data.json
   ```

### Option B: Using a Direct SQL Conversion

This approach is more complex and may require manual adjustments to the SQL:

1. Use a tool like [pgloader](https://github.com/dimitri/pgloader) to migrate directly:
   ```bash
   pgloader postgresql://juice_db_drbd_user:XrWKZI7n0vehFTaQ22PTYYo3krPrOE7h@dpg-d02kg93e5dus73bt74ng-a.oregon-postgres.render.com/juice_db_drbd mysql://root:Aamruth@22@localhost/juice_task_db
   ```

   Or use a conversion script like [pg2mysql](https://github.com/ChrisLundquist/pg2mysql) to convert the dump:
   ```bash
   pg2mysql juice_db_backup.sql > mysql_dump.sql
   mysql -u root -p juice_task_db < mysql_dump.sql
   ```

## Step 5: Test the Application

1. Ensure the DATABASE_TYPE environment variable is set to mysql:
   ```bash
   # On Windows
   set DATABASE_TYPE=mysql
   
   # On macOS/Linux
   export DATABASE_TYPE=mysql
   ```

2. Run the Django development server:
   ```bash
   python manage.py runserver
   ```

3. Visit http://127.0.0.1:8000/ in your browser

4. Test all functionality to ensure the migration was successful

## Step 6: Copy Media Files

If you have any media files (attachments) in your Render deployment, make sure to copy them to your local environment:

1. Download the files from Render
2. Place them in the appropriate directory (e.g., `media/attachments/`)

## Making the Environment Variable Permanent

To avoid setting the environment variable each time, you can:

### On Windows:

1. Set a system environment variable:
   - Right-click on "This PC" or "My Computer"
   - Select "Properties" > "Advanced system settings" > "Environment Variables"
   - Add a new variable with name `DATABASE_TYPE` and value `mysql`

### On macOS/Linux:

1. Add to your shell profile file (~/.bashrc, ~/.zshrc, etc.):
   ```bash
   export DATABASE_TYPE=mysql
   ```

## Troubleshooting

### Common Issues

1. **MySQL Connection Errors**:
   - Ensure MySQL server is running
   - Verify username and password in settings.py or environment variables
   - Check that the database exists

2. **Migration Errors**:
   - If you encounter errors during `python manage.py migrate`, try running `python manage.py makemigrations` first

3. **Data Import Issues**:
   - If you have issues with the JSON fixture, try excluding problematic apps: `python manage.py dumpdata --exclude contenttypes --exclude auth.permission --exclude sessions > all_data.json`

4. **Character Encoding Issues**:
   - Ensure your MySQL database is using utf8mb4 encoding
   - Check that the data was properly encoded in the original database

### Need Help?

If you encounter any issues during the migration process, please create an issue in the repository or contact the development team.