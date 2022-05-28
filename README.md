# Hashicorp Vault

Simple example with Hashicorp Vault and MySql Database with dynamic secret


# Requirements

* Python/3.7.3+
* Docker/19.03.12+
* Hasicorp Vault/v1.10.3+


# Running the example

## 1. Start Vault

```sh
vault server -dev
```

## 2. Start MySql Docker and Test Connection

```sh
docker network create mysql
docker run --name local-mysql --network mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=secret123 -d mysql:8.0.29
docker run -it  --network mysql --rm mysql mysql -hlocal-mysql -uroot -p
#input password, secret123
```

## 3. Configure Vault Database Engine and Connection

```sh
#export VAULT_ADDR='http://127.0.0.1:8200'
#export VAULT_TOKEN='xxxxxxx'
vault secrets enable database
vault write database/config/my-mysql-database \
    plugin_name=mysql-database-plugin \
    connection_url="{{username}}:{{password}}@tcp(127.0.0.1:3306)/" \
    allowed_roles="my-role" \
    username="root" \
    password="secret123"
```

## 4. Create Vault Role

```sh
vault write database/roles/my-role \
    db_name=my-mysql-database \
    creation_statements="CREATE USER '{{name}}'@'%' IDENTIFIED BY '{{password}}';GRANT SELECT ON *.* TO '{{name}}'@'%';" \
    default_ttl="1h" \
    max_ttl="24h"
```

## 5. Test the Role

```sh
 vault read database/creds/my-role
```

## 6. Check MySql Users

```sh
docker run -it  --network mysql --rm mysql mysql -hlocal-mysql -uroot -p
#input password, secret123

#sql return example
mysql> select user from mysql.user;
+----------------------------------+
| user                             |
+----------------------------------+
| root                             |
| v-root-my-role-2s9CxVzjmxuiSqOOa |
| v-root-my-role-GTvni4OnxsIqc8uPm |
| v-root-my-role-Qw0NDTkuy1YxNrtzd |
| v-root-my-role-WcX6AgO2m2j4CmP9J |
| v-root-my-role-b5Q466fBssycnRsd0 |
| mysql.infoschema                 |
| mysql.session                    |
| mysql.sys                        |
| root                             |
+----------------------------------+
10 rows in set (0.00 sec)
```

## 6. Run the main.py

```sh
pip install -r src/requirements.txt
python src/main.py
```

# Some Understantings

* Credential request uses the role path (e.g. vault read database/creds/my-role);
* In the dynamic mode, the engine removes the user from the database when the lease expires;
* One lease is generated on every credentials request, they control the life of the dynamic credential;
* In the static role type we should have a role already created in the database. In the dynamic type the engine is responsible for control the creation of users and leases;
* The paths of static and dynamic credentials are different, static (e.g. database/static-creds/my-role) and dynamic (e.g. database/creds/my-role).
