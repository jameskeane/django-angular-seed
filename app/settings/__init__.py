import os
from app.settings.base import *

env = os.environ.get('ENV', 'development')

if env == 'production':
	from app.settings.production import *
elif env == 'test':
	from app.settings.test import *
else:
	from app.settings.development import *
