"""
One-time migration: SQLite vsm.db → PostgreSQL stump_db
Run from project root with venv active:
  python migrate_sqlite_to_postgres.py
"""
import sqlite3, json, asyncio, sys
from pathlib import Path
from datetime import datetime

SQLITE_PATH = Path(__file__).parent / "backend/database/vsm.db"
PG_URL = "postgresql+asyncpg://postgres@localhost:5432/stump_db"

TABLES = [
    "projects",
    "vsm_snapshots",
    "analysis_runs",
    "platform_settings",
    "scheduled_pipeline_runs",
    "devops_assessments",
    "assessment_action_items",
    "activity_metrics",
]

async def migrate():
    if not SQLITE_PATH.exists():
        print(f"No SQLite DB found at {SQLITE_PATH} — nothing to migrate.")
        return

    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from sqlalchemy import text

    # Create all tables in Postgres first
    sys.path.insert(0, str(Path(__file__).parent / "backend"))
    from database.models import Base

    engine = create_async_engine(PG_URL, echo=False)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("Postgres schema created.")

    # Read all data from SQLite
    con = sqlite3.connect(str(SQLITE_PATH))
    con.row_factory = sqlite3.Row
    cur = con.cursor()

    AsyncSess = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)
    total = 0

    for table in TABLES:
        try:
            cur.execute(f"SELECT * FROM {table}")
        except sqlite3.OperationalError:
            continue
        rows = cur.fetchall()
        if not rows:
            continue

        cols = [d[0] for d in cur.description]
        async with AsyncSess() as session:
            for row in rows:
                vals = {}
                for c, v in zip(cols, row):
                    # Parse datetime strings → datetime objects for Postgres
                    if isinstance(v, str) and len(v) >= 19 and ('T' in v or (v.count('-') == 2 and ':' in v)):
                        for fmt in ('%Y-%m-%d %H:%M:%S.%f', '%Y-%m-%d %H:%M:%S', '%Y-%m-%dT%H:%M:%S.%f', '%Y-%m-%dT%H:%M:%S'):
                            try: v = datetime.strptime(v[:26], fmt); break
                            except: pass
                    # Deserialise JSON text columns then re-serialise as string for asyncpg text()
                    elif isinstance(v, str) and v and v[0] in ('{', '['):
                        try: v = json.loads(v)
                        except: pass
                    # Serialise dict/list back to JSON string for text() INSERT
                    if isinstance(v, (dict, list)):
                        v = json.dumps(v)
                    vals[c] = v
                # Build INSERT with conflict-skip
                placeholders = ", ".join(f":{c}" for c in vals)
                col_list = ", ".join(vals.keys())
                stmt = text(
                    f"INSERT INTO {table} ({col_list}) VALUES ({placeholders}) "
                    f"ON CONFLICT DO NOTHING"
                )
                await session.execute(stmt, vals)
            await session.commit()
        print(f"  {table}: {len(rows)} rows migrated")
        total += len(rows)

    con.close()
    await engine.dispose()
    print(f"\nDone — {total} total rows migrated to PostgreSQL.")

if __name__ == "__main__":
    asyncio.run(migrate())
