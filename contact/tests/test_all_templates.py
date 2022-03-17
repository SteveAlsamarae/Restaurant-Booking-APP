from django.test import TestCase
from django.conf import settings
from django.template import Template
from django.template.exceptions import TemplateSyntaxError

from os import path, walk
import glob
from importlib import import_module


class TemplatesTest(TestCase):
    def test_templates(self):
        """Templates can compile properly and there's no mismatched tags"""

        template_dirs = []
        apps = [app for app in settings.INSTALLED_APPS if app.endswith("config")]
        for app in apps:
            mod = import_module(app)
            template_dirs.append(path.join(path.dirname(mod.__file__), "templates"))

        for template_dir in settings.TEMPLATES[0]["DIRS"]:
            template_dirs.append(template_dir)

        templates = []
        for template_dir in template_dirs:
            templates += glob.glob("%s/*.html" % template_dir)
            templates += glob.glob("%s/*.txt" % template_dir)
            for root, dirnames, filenames in walk(template_dir):
                for dirname in dirnames:
                    template_folder = path.join(root, dirname)
                    templates += glob.glob("%s/*.html" % template_folder)
                    templates += glob.glob("%s/*.txt" % template_folder)
        for template in templates:
            with open(template, "r") as f:
                source = f.read()
                try:
                    Template(source)
                except TemplateSyntaxError as e:
                    raise TemplateSyntaxError("%s in %s" % (e, template))
                self.assertEqual(
                    source.count("{%"),
                    source.count("%}"),
                    "Found impaired {%% and %%} in %s" % template,
                )
                self.assertEqual(
                    source.count("{{"),
                    source.count("}}"),
                    "Found impaired {{ and }} in %s" % template,
                )
