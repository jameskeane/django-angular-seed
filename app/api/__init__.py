import glob
from os import path
from tastypie.api import Api

# Convert underscore_names to CamelCase
def convert(word):
    return ''.join(x.capitalize() or '_' for x in word.split('_'))

# Create a dev API that includes everything
router = Api()

# Load the models
for file in glob.glob(path.join(path.dirname(__file__), '*.py')):
  basename = path.basename(file)
  (file, ext) = path.splitext(basename)
  if ext == '.py' and not basename == '__init__.py':
    module = convert(file) + 'Resource'

    # import the file
    imported = __import__(file, globals(), locals(), [module], -1).__dict__[module]
    router.register(imported())

    # export it for app.models
    globals()[module] = imported
