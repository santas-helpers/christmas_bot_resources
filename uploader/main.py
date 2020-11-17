import sys

from uploader.db import insert_creatures_into_db, insert_items_into_db
from uploader.s3 import upload_images


if len(sys.argv) == 1:
  creature_images = upload_images('creatures')
  insert_creatures_into_db(creature_images)

  item_images = upload_images('items')
  insert_items_into_db(item_images)
elif len(sys.argv) == 2 and (sys.argv[1] == '-f' or sys.argv[1] == '--force'):
  creature_images = upload_images('creatures', force=True)
  insert_creatures_into_db(creature_images, force=True)

  item_images = upload_images('items', force=True)
  insert_items_into_db(item_images, force=True)
else:
  print('Error: Too many arguments (only argument accepted is --force or -f to '
    'force upload images and config')

