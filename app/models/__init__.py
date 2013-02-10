import glob
from os import path
from django.db import models
from django.contrib import admin

# import User so that you can do app.models.User
from django.contrib.auth.models import User

# This _has_ to be the base class as I do not
# know a way to dynamically modify the meta
class Model(models.Model):
  class Meta:
    abstract = True
    app_label = "app"

# Convert underscore_names to CamelCase
def convert(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

# Load the models
for file in glob.glob(path.join(path.dirname(__file__), '*.py')):
  basename = path.basename(file)
  (file, ext) = path.splitext(basename)
  if ext == '.py' and not basename == '__init__.py':
    module = convert(file)

    imported = __import__(file, globals(), locals(), [module], -1).__dict__

    # Register the model with the admin site,
    # tries to register <module>Admin class if
    # it exists
    admin_cls = imported.get(module+'Admin', None)
    admin.site.register(imported[module], admin_cls)

    # export it for app.models
    globals()[module] = imported[module]
