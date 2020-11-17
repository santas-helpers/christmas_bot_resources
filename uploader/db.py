import os

from sqlalchemy import Table, Column, Integer, ARRAY, Text, MetaData, create_engine
from sqlalchemy.sql import select

from uploader.config import DB_CONFIG, DB_SCHEMA

import json


db = create_engine(DB_CONFIG)

meta = MetaData(db, schema=DB_SCHEMA)

creatures_table = Table('creatures', meta,
  Column('id', Text, primary_key=True),
  Column('display_name', Text),
  Column('img_url', Text),
  Column('status', Text),
  Column('pronoun', Text),
  Column('items', ARRAY(Text))
)

items_table = Table('items', meta,
  Column('id', Text, primary_key=True),
  Column('display_name', Text),
  Column('img_url', Text),
  Column('rarity', Integer)
)


def insert_creatures_into_db(images: dict[str, str], force: bool=False):
  select_existing_creatures_stmt = select([creatures_table.c.id])
  existing_creatures = [row['id']for row in db.execute(select_existing_creatures_stmt).fetchall()]
  dir_local_path = 'creatures/config/'

  print('Inserting creature configs to DB...')
  for filename in os.listdir(dir_local_path):
    entity_local_path = dir_local_path + filename
    
    creature_id = filename[:-5]
    if creature_id in existing_creatures and not force:
      print('  {} (skipped)'.format(filename))
      continue
    else:
      with open(entity_local_path) as file:
        creature_config = json.load(file)

      display_name = creature_config['display_name']
      status = creature_config['status']
      pronoun = creature_config['pronoun']
      items = creature_config['items']

      if creature_id not in images.keys():
        raise Exception('Image file does not exist for {}'.format(filename))
      img_url = images[creature_id]

      if creature_id in existing_creatures:
        # force must be enabled so we update it
        update_stmt = creatures_table.update().where(
          creatures_table.c.id == creature_id
        ).values(
          id=creature_id, 
          display_name=display_name,
          status=status,
          img_url=img_url,
          pronoun=pronoun,
          items=items
        )
        db.execute(update_stmt)
        print('  {} (forced)'.format(filename))
      else:
        # force or not we insert a new entr
        insert_stmt = creatures_table.insert().values(
          id=creature_id, 
          display_name=display_name,
          status=status,
          img_url=img_url,
          pronoun=pronoun,
          items=items
        )
        db.execute(insert_stmt)
        print('  {}'.format(filename))


def insert_items_into_db(images: dict[str, str], force: bool=False):
  select_existing_items_stmt = select([items_table.c.id])
  existing_items = [row['id']for row in db.execute(select_existing_items_stmt).fetchall()]
  dir_local_path = 'items/config/'

  print('Inserting items configs to DB...')
  for filename in os.listdir(dir_local_path):
    entity_local_path = dir_local_path + filename
    
    item_id = filename[:-5]
    if item_id in existing_items and not force:
      print('  {} (skipped)'.format(filename))
      continue
    else:
      with open(entity_local_path) as file:
        item_config = json.load(file)

      display_name = item_config['display_name']
      rarity = item_config['rarity']
      if item_id not in images.keys():
        img_url = ''
      else:
        img_url = images[item_id]

      if item_id in existing_items:
        # force must be enabled so we update it
        update_stmt = items_table.update().where(
          items_table.c.id == item_id
        ).values(
          id=item_id, 
          display_name=display_name,
          rarity=rarity,
          img_url=img_url,
        )
        db.execute(update_stmt)
        print('  {} (forced)'.format(filename))
      else:
        # force or not we insert a new entr
        insert_stmt = items_table.insert().values(
          id=item_id, 
          display_name=display_name,
          rarity=rarity,
          img_url=img_url,
        )
        db.execute(insert_stmt)
        print('  {}'.format(filename))

