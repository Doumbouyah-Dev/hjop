import subprocess
import sys

from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Runs Tailwind watcher and Django dev server together (Windows dev convenience)."

    def handle(self, *args, **options):
        tailwind_proc = subprocess.Popen(
            [".\\tailwindcss.exe", "-i", ".\\static\\src\\input.css",
             "-o", ".\\static\\css\\output.css", "--watch"],
            shell=True,
        )
        try:
            subprocess.run([sys.executable, "manage.py", "runserver"])
        finally:
            tailwind_proc.terminate()