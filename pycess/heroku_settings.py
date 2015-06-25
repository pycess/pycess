import dj_database_url

DATABASES = {'default': dj_database_url.config()}

print('configured heroku DATABASES', DATABASES)