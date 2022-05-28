import hvac
import os

vault_url = os.getenv('VAULT_URL','http://127.0.0.1:8200')

vault_token = os.getenv('VAULT_TOKEN')
if not vault_token:
    raise Exception('Configure VAULT_TOKEN environment!')

print("Using variables: VAULT_URL={0}, VAULT_TOKEN={1}".format(vault_url, vault_token))

client = hvac.Client(url=vault_url, token=vault_token)

mysql_secret = client.read('database/creds/my-role')
print(mysql_secret)
