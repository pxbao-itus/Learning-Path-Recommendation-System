import os

from dotenv import load_dotenv
from neomodel import Q, db

load_dotenv()
db.set_connection('bolt://' + os.getenv('USERNAME') + ":" + os.getenv('PASSWORD') + "@" + os.getenv('URL'))
