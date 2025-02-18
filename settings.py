from decouple import config

# Lê as variáveis do arquivo .env
DATABASE_URL = config("DATABASE_URL")
SECRET_KEY = config("SECRET_KEY")
DEBUG = config("DEBUG", default=False, cast=bool)

print("DATABASE_URL:", DATABASE_URL)
print("SECRET_KEY:", SECRET_KEY)
print("DEBUG:", DEBUG)
