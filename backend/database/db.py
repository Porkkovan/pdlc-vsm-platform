import ssl as ssl_mod
from sqlalchemy import text
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from .models import Base
from ..core.config import settings

_connect_args = {}
_db_url = settings.database_url
if "azure" in _db_url.lower() or "ssl=require" in _db_url.lower():
    _ssl_ctx = ssl_mod.create_default_context()
    _ssl_ctx.check_hostname = False
    _ssl_ctx.verify_mode = ssl_mod.CERT_NONE
    _connect_args["ssl"] = _ssl_ctx
    _db_url = _db_url.split("?")[0]

engine = create_async_engine(_db_url, echo=settings.debug, connect_args=_connect_args)
AsyncSessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)


# Lightweight inline migrations for columns added after the initial schema.
# Each entry: (table, column, DDL fragment). Skipped if the column already exists.
# When the project adopts Alembic, move these into versioned migration files.
_PENDING_ADD_COLUMNS = [
    ("projects", "option_a_parent_map",  "JSONB DEFAULT '{}'::jsonb"),
    ("projects", "cost_model_overrides", "JSONB DEFAULT '{}'::jsonb"),
    ("manual_assessment_responses", "product_group", "VARCHAR"),
    ("manual_assessment_responses", "product",       "VARCHAR"),
    ("manual_assessment_responses", "team",          "VARCHAR"),
]


async def _add_missing_columns(conn):
    for table, column, ddl in _PENDING_ADD_COLUMNS:
        exists = await conn.execute(text(
            "SELECT 1 FROM information_schema.columns "
            "WHERE table_name = :t AND column_name = :c"
        ), {"t": table, "c": column})
        if exists.first() is None:
            await conn.execute(text(f'ALTER TABLE {table} ADD COLUMN {column} {ddl}'))


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        await _add_missing_columns(conn)


async def get_db():
    async with AsyncSessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()
