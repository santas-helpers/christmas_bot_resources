import json
from sqlalchemy.engine.url import URL

with open('config.json') as f:
  config = json.load(f)


DB_CONFIG = URL(**config['db_url'])
DB_SCHEMA = config['db_schema']


AWS_S3_BUCKET_NAME = config['s3_config']['s3_bucket']
AWS_REGION = config['s3_config']['aws_region']
AWS_ACCESS_KEY_ID = config['s3_config']['aws_access_key_id']
AWS_SECRET_ACCESS_KEY = config['s3_config']['aws_secret_access_key']