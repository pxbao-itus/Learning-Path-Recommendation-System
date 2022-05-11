from django.apps import AppConfig


class ModelsConfig(AppConfig):
    default_auto_field = 'django.db.neo4j_connection.BigAutoField'
    name = 'neo4j_connection'
