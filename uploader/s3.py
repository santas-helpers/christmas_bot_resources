import os
from mimetypes import guess_type

import boto3
from botocore.errorfactory import ClientError

from uploader.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_S3_BUCKET_NAME


session = boto3.Session(
  aws_access_key_id=AWS_ACCESS_KEY_ID,
  aws_secret_access_key=AWS_SECRET_ACCESS_KEY
)

s3 = session.resource('s3')

def get_s3_url(bucket: str, region: str, filename: str):
  return 'https://{}.s3-{}.amazonaws.com/{}'.format(bucket, region, filename)


# Uploads images under the given path in s3
# Returns a dictionary mapping entity id to s3 url
def upload_images(entity_type: str, force: bool=False) -> dict[str, str]:
  output = {}
  print('Uploading images for {}...'.format(entity_type))
  dir_local_path = entity_type + '/images/'
  for filename in os.listdir(dir_local_path):
    # gets name from json filename
    entity_id = filename[:-4]
    entity_local_path = dir_local_path + filename
    entity_s3_path = entity_type + '/' + filename
    object = s3.Object(AWS_S3_BUCKET_NAME, entity_s3_path)
    try:
      object.load()
    except ClientError as e:
      if e.response['Error']['Code'] == "404":
        # The object does not exist, create it
        object.upload_file(entity_local_path, ExtraArgs={
          'ContentType': guess_type(filename)[0]
        })
        print('  {}'.format(filename))
      else:
        # Something else has gone wrong.
        raise
    else:
      # Only upload if object doesn't previously exist
      if force:
        object.upload_file(entity_local_path, ExtraArgs={
          'ContentType': guess_type(filename)[0]
        })
        print('  {} (forced)'.format(filename))
      else:
        print('  {} (skipped)'.format(filename))
      
    output[entity_id] = get_s3_url(AWS_S3_BUCKET_NAME, AWS_REGION, entity_s3_path)

  return output
