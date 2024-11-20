# mySchedules
Web-app to streamline the process of shift assigning and picking among part time employees and managers.

## Postgresql Installation
Version: 17.1
For windows: [Windows X86-64](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259192)

For mac: [Mac OS X](https://sbp.enterprisedb.com/getfile.jsp?fileid=1259195)

## Database setup
You would need to make a user and a database under that user.
Go to pgadmin4 and make another user.

1. Servers -> Postgresql 17 -> Login/Group Roles
2. Right click, and create a new user. 


## Installation

Please use cmd shell

1. Clone this repo
    ```sh
    https://github.com/sahajpatel008/mySchedules.git
    ```
2. ```sh
    cd mySchedules
    ```
3. Preferred to use a virtualenv. 
    ```sh
    pip install virtualenv
    python -m virtualenv venv
    .\Scripts\activate
    pip install -r requirements.txt
    ```
    For deactivating venv
    ```sh
    .\Scripts\deactivate
    ```
4. Make a .env file here. (the level where you have .git file) Please don't use quotes anywhere.
    ```sh
    DB_NAME=#db name
    DB_USERNAME=#your db username
    DB_PASSWORD=#password you setup for your postgres user 
    HOST_EMAIL=#email id you would use to send mails to clients 
    MAIL_PASSWORD=#gmail app password 
    ```
5. Go to django project level (the level that has manage.py)
    ```sh
    cd mySchedules
    ```

6. Build models and then deploy locally
     ```sh
    python manage.py makemigrations
    python manage.py migrate
    ```
    For deploying
    ```sh
    python manage.py runserver
    ```

## URL Routes
- user/register
- user/login
- user/logout
- user/home