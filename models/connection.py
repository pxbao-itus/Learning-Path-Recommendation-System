import os
from dotenv import load_dotenv
from py2neo import Graph
from neomodel import Q, db


# connecting for neomodel
load_dotenv()
db.set_connection(os.getenv('SCHEME') + os.getenv('USERNAME') + ":" + os.getenv('PASSWORD') + "@" + os.getenv('URL'))

# connecting for py2neo
g = Graph(os.getenv('SCHEME') + os.getenv('URL'), auth=(os.getenv('USERNAME'), os.getenv('PASSWORD')))
