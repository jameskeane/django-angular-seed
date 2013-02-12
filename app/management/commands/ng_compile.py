from django.conf import settings
from django.core.management.base import BaseCommand, CommandError
import os
import string

tmpl = string.Template("""
(function() {
    var script = document.createElement('script');
    var tpl = document.createTextNode("$contents");
    script.appendChild(tpl);
    script.setAttribute("id", "$filename");
    script.setAttribute("type", "text/ng-template");
    document.body.appendChild(script);
})();
""")

class Command(BaseCommand):
    args = '<template_file>'
    help = 'Compile the angular template if compress is enabled'

    def handle(self, *args, **options):
        if settings.COMPRESS_ENABLED:
            path = args[0]
            filename = os.path.relpath(path)[3:]
            with open(path) as f:
                contents = f.read().replace('"', '\\"').replace("'", "\\'")
                print tmpl.substitute(contents=contents, filename=filename)
