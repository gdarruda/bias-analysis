
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    load_dotenv=True,
    settings_files=['settings.toml', '.secrets.toml', '.env'],
)
