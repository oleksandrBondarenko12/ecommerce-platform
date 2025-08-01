# A configuration file for the app itself. Here you define the app's name. You
# rarely need to edit this file, but you must register the AppConfig class
# (e.g., ProductsConfig) in your INSTALLED_APPS setting.
from django.apps import AppConfig


class UsersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'users'
