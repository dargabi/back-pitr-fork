import json
import os
# Reads the secret .env file and loads the environment variables

SECRETS_FILE = '.secrets.json'

def load_vars():
    s = {}
    with open(SECRETS_FILE) as f:
        json_secrets = json.load(f)
        env = os.environ.get('FLASK_ENV')
        print('Loading environment variables for', env)

        if env == 'dev':
            s['DATABASE_URI'] = json_secrets['dev']['DATABASE_URI']
        if env == 'prod':
            s['DATABASE_URI'] = json_secrets['prod']['DATABASE_URI']

    return s

secrets = load_vars()
