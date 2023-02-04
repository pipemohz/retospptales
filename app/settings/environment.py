from dotenv import load_dotenv
import os

# Execute the load_dotenv() function
load_dotenv()

# Azure environment settings
# Connection String
CONNECT_STRING = os.getenv('AZURE_STORAGE_CONNECTION_STRING') \
    or os.environ.get('AZURE_STORAGE_CONNECTION_STRING')
# Name of File share resource in Azure account
SHARE_NAME = os.getenv(
    'AZURE_FILE_SHARE') or os.environ.get('AZURE_FILE_SHARE')

# Database settings
# Host
DB_HOST = os.getenv("DB_HOST") or os.environ.get("DB_HOST")
# Database name
DB_NAME = os.getenv("DB_NAME") or os.environ.get("DB_NAME")
# Database username
DB_USERNAME = os.getenv("DB_USERNAME") or os.environ.get("DB_USERNAME")
# Database password
DB_PASSWORD = os.getenv("DB_PASSWORD") or os.environ.get("DB_PASSWORD")
