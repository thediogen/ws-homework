import os

from dotenv import load_dotenv


load_dotenv(override=True)

DB_URL: str = (
    'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'.format(
        DB_USER=os.getenv('DB_USER'),
        DB_PASSWORD=os.getenv('DB_PASSWORD'),
        DB_HOST=os.getenv('DB_HOST'),
        DB_PORT=os.getenv('DB_PORT'),
        DB_NAME=os.getenv('DB_NAME'),
    )
)

SESSION_MIDDLEWARE_SECRET_KEY: str = os.getenv('SESSION_MIDDLEWARE_SECRET_KEY')