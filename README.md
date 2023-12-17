# setup envionment

install python and `mysql-connector-python` package

```shell
pip install mysql-connector-python
pip install cryptography
```

# start docker

## On windows 

install Desktop docker and either

1. do the following in the current project dir  

```shell
docker compose up -d
```

2. or the following if you wish to use GUI:

set env variables when creating docker container:
set MYSQL_ROOT_PASSWORD to Xpconfig37
you may also set MYSQL_DATABASE to passwdst, 
but the python script will create this db for you.
Also be sure to set the right ports when creating docker
container and running the below script.

## On linux or mac

install docker and run

```shell
docker compose up -d
```

# create db and tables

the database is locally in docker.

port is 3307 for example. This depends on docker setup.

db name is passwdst

```shell
python create_db.py --host localhost --port 3307 --user root --password Xpconfig37 --db_name passwdst --table_sql "CREATE TABLE users (id INT AUTO_INCREMENT PRIMARY KEY, username VARCHAR(50) NOT NULL, password VARCHAR(255) NOT NULL, akey VARCHAR(255) NOT NULL); CREATE TABLE entries (id INT AUTO_INCREMENT PRIMARY KEY, name VARCHAR(255) NOT NULL, user VARCHAR(255) NOT NULL, user_id INT NOT NULL, pass VARCHAR(255) NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id));"
```

# check results

run docker ps to get info about current container. Note the last column name

```shell
PS C:\Users\Admin> docker ps
CONTAINER ID   IMAGE          COMMAND                  CREATED         STATUS         PORTS                                              NAMES
d4665b5b17f2   mysql:latest   "docker-entrypoint.s…"   3 minutes ago   Up 3 minutes   0.0.0.0:3307->3306/tcp, 0.0.0.0:33061->33060/tcp   password_project-db-1
```

Use the contianer name (it can be set when creating a container):

```shell
docker exec -it password_project-db-1 bash
```

this will give you accept to the shell of the running mysql container

```shell
mysql -p SOMESECRETPASSWD
```

this will gain access to the mysql shell

swithc to the right db:

```sql
USE passwdst;
```

show tables:

```sql
SHOW TABLES;
```

see some table column info

```sql
DESC sometable_name;
```

get all info from some table:

```sql
SELECT * FROM table_name;
```

# main

```shell
# used for automtic tests/tasks as main.py accepts more arguments and has no ui
python main.py --db_password=Xpconfig37 --db_port=3307 --user=Mark --password=qwerty1

# on host: connects by default to the db in default docker configuration. has ui for end user
python cli.py

# in docker
python cli.py --db_host db --db_port 3306
```