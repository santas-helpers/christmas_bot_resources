# christmasbot_resources

art and stuff

## Setting up the uploader

- Make sure your Python version is 3.9 or higher.
- If you don't have Poetry already install Poetry and `poetry install`.
- Fill in valid AWS and PostgresSQL credentials in `config.json`.
- Run `poetry run python uploader/main.py` to upload images and insert configs
  without affecting existing images/configs on S3 and the database.
- Or, run `poetry run python christmasbot/main.py` to force update all creature
  and item images and configs.
