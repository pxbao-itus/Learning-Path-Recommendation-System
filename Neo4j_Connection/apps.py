from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.Neo4j_Connection.BigAutoField'
    name = 'Neo4j_Connection'
