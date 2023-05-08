# Database Programming examples with Python and PostgreSQL

## Pre-requisites
**NOTE:** you will have to install the `psycopg2` package to connect with to a PostgreSQL
database instance from your Python programs. This can be done as follows:
```bash
$> pip install psycopg2
```

## Install Sample Database `dvdrental`
Install the PostgreSQL sample database - `dvdrental`, if not done already. This is to be
installed in the `postgres` userid.

### Confirm if `dvdrental` is already installed
1. Start `psql` and connect to the `dvdrental` database as follows
```bash
$> psql -h localhost -U postgres
postgres=# 
```
At the `postgres=#` prompt, select the `dvdrental` database as follows
```bash
postgres=# \c dvdrental
```
* If an error message is displayed, this database is most probably NOT install - install it as explained in the next section.
* If no error message is displayed, then the database is selected and you do not need to do anything more. 

### Install `dvdrental` if not installed
Follow steps in this section ONLY IF the `dvdrental` database is not installed. Else skip this section.

1. Download the sample database. From the shell command line, type the following command
```bash
$> curl -O https://sp.postgresqltutorial.com/wp-content/uploads/2019/05/dvdrental.zip
```
Unzip the contents of the zip file to get the `dvdrental.tar` file.
```bash
$> unzip dvdrental.zip
```
2. Start a `psql` session from the SAME folder where you unzipped the `dvdrental.zip` download.
```bash
$> psql -h localhost -U postgres 
```
Enter the password if prompted. If connection is successful, you'll see the following prompt
```bash
postgres=# 
```
3. Enter the following command to create a database
```bash
postgres=# CREATE DATABASE dvdrental; 
```
After this command completes, quit the `psql` session
```bash
postgres=# \q
```
4. Back to the OS command prompt, enter the following command on the OS command prompt
```bash
$> pg_restore --dbname=dvdrental --verbose dvdrental.tar
```
* **NOTE:** this command assumes that `dvdrental.tar` is in the same folder - please `cd` to
the folder where `dvdrental.tar` has been unzipped to before executing above command
* This commend does not produce any output & completes fairly quickly. Once command has 
completed, access `psql` again to confirm that the `dvdrental` schema has been imported
5. Confirm that `dvdrental` schema has been imported
```bash
$> psql -h localhost -U postgres    # enter any password if prompted

postgres=#   <<< this prompt means connection was successful
```
Connect to the `dvdrental` database
```bash
postgres=# \c dvdrental    # this command should NOT display any error
```
Now you are connected to the `dvdrental` database.
6. Run your queries (SELECT, DDL, DML etc.)
```bash
postgres=# select count(*) from film;
```
It should display the following output, confirming that `dvdrental` has been setup
```bash
count
-------
1000
(1 row)
```
Congratulations - this means that the `dvdrental` database has been successfully installed. 


