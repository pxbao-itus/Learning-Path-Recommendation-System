from django.apps import AppConfig


class ApisConfig(AppConfig):
    default_auto_field = 'django.db.neo4j_connection.BigAutoField'
    name = 'apis'
