from django.conf import settings
from django.core.management.base import BaseCommand
import os
import string

tmpl = string.Template("""
App.run(['$$templateCache', function($$templateCache) {
    $$templateCache.put("$filename", "$contents");
}]);
""")


class Command(BaseCommand):
    args = '<template_file>'
    help = 'Compile the angular template if compress is enabled'

    def handle(self, *args, **options):
        path = args[0]
        filename = os.path.relpath(path)
        if filename.startswith('dist'):
            filename = '/static' + filename[4:]
        else:
            filename = filename[3:]

        with open(path) as f:
            contents = f.read().replace('"', '\\"').replace("'", "\\'").replace("\n", "\\n").replace("\r", "\\r")
            self.stdout.write(tmpl.substitute(contents=contents, filename=filename))
