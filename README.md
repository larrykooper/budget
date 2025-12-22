# Budget
A budgeting program.

## Setup

1. Clone the repository:
    ```bash
    git clone https://github.com/larrykooper/budget.git
    cd budget
    ```

2. Create a virtual environment:
    ```bash
    python3 -m venv venv
    ```

3. Activate the virtual environment:
    ```bash
    source venv/bin/activate
    ```

4. Install the requirements:
    ```bash
    pip install -r requirements.txt
    ```

5. Set the environment variables:
    ```bash
    export PYTHONPATH=/path/to/budget
    export FLASK_APP=src/flask_app
    export SECRET_KEY=your_secret_key
    ```

Replace `/path/to/budget` with the actual path to your project's root directory and `your_secret_key` with your actual secret key.

6. Run the application:
    ```bash
    flask run
    ```

## Database Setup

This application uses a PostgreSQL database. 

<details>
<summary>PostgreSQL Setup</summary>

1. Install PostgreSQL:

    On macOS, you can use Homebrew:

    ```bash
    brew install postgresql
    ```

    On Ubuntu, you can use apt:

    ```bash
    sudo apt-get update
    sudo apt-get install postgresql postgresql-contrib
    ```

2. Start the PostgreSQL service:

    On macOS:

    ```bash
    brew services start postgresql
    ```

    On Ubuntu:

    ```bash
    sudo service postgresql start
    ```

3. Create a new PostgreSQL user:

    ```bash
    createuser --interactive --pwprompt
    ```

    When prompted, enter the name of your new user (e.g., `your_user`), and a password.

4. Create a new PostgreSQL database:

    ```bash
    createdb -O your_user your_database
    ```

    Replace `your_user` with the name of your PostgreSQL user, and `your_database` with the name of your new database.

</details>

You need to grant the necessary permissions to the user in your PostgreSQL database. You can do this by logging into your PostgreSQL database as a superuser and running the following commands:

```sql
GRANT ALL PRIVILEGES ON SCHEMA public TO your_user;
GRANT ALL PRIVILEGES ON DATABASE your_database TO your_user;

```

Please replace yourusername, your_secret_key, your_user, and your_database with your actual GitHub username, secret key, PostgreSQL username, and PostgreSQL database name, respectively.