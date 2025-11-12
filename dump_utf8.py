import os
import django

# Tell Python which Django settings to use
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ovara.settings")  # <-- your project is 'ovara'
django.setup()

from django.core.management import call_command

# Dump data with UTF-8 encoding
with open("db.json", "w", encoding="utf-8") as f:
    call_command("dumpdata", exclude=["auth.permission", "contenttypes"], stdout=f)

print("db.json created successfully ✅")
