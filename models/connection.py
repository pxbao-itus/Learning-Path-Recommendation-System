import os
from dotenv import load_dotenv
from py2neo import Graph
from neomodel import Q, db


# connecting for neomodel
load_dotenv()
db.set_connection('bolt://' + os.getenv('USERNAME') + ":" + os.getenv('PASSWORD') + "@" + os.getenv('URL'))

# connecting for py2neo
g = Graph("bolt://localhost:7687", auth=("neo4j", "fit@hcmus"))
