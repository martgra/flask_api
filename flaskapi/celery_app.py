from flaskapi.app import init_celery

app = init_celery()
app.conf.imports = app.conf.imports + ("flaskapi.tasks.example",)
