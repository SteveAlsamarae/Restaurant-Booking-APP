from django.core.management.base import BaseCommand
from django.core.management.utils import get_random_secret_key
from django.conf import settings


BASE_DIR = settings.BASE_DIR.parent


class Command(BaseCommand):
    help = "Create a .env file for storing environment variables"

    def handle(self, *args, **options):
        env_path: str = BASE_DIR / ".env"
        secret_key = get_random_secret_key()
        lines: str = """# SECURITY WARNING: don't run with the debug turned on in production!
DEBUG={}

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY={}
"""

        if not env_path.exists():
            env_path.touch()
            print("Created .env file...")
            is_debug = input("Is this a local-development environment? [y/N] ")
            if is_debug == "y" or is_debug == "Y":
                is_debug = True
            else:
                is_debug = False
            lines = lines.format(is_debug, secret_key)
            with open(env_path, "w") as f:
                f.write(lines)
        else:
            if env_path.is_file():
                print(".env file already exists")
                print("Do you want to overwrite it? (y/n)")
                choice = input()
                if choice == "y" or choice == "Y":
                    env_path.unlink()
                    env_path.touch()
                    is_debug = input("Is this a local-development environment? [y/N] ")
                    if is_debug == "y" or is_debug == "Y":
                        is_debug = True
                    else:
                        is_debug = False
                    lines = lines.format(is_debug, secret_key)
                    with open(env_path, "w") as f:
                        f.write(lines)
                    print("Overwritten .env file")
                else:
                    print("Aborted...")
                    return

        self.stdout.write(
            self.style.SUCCESS(
                "Successfully created .env file with \nSECRET_KEY={} and DEBUG={}".format(
                    secret_key, is_debug
                )
            )
        )
