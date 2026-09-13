"""
Seed demo data into Azure PostgreSQL after deployment.
Run: python deploy/seed_azure_db.py <DATABASE_URL>
"""
import asyncio
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

async def seed(db_url: str):
    import ssl as ssl_mod
    from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
    from backend.database.models import Base

    connect_args = {}
    if 'azure' in db_url.lower() or 'ssl' in db_url.lower():
        ssl_ctx = ssl_mod.create_default_context()
        ssl_ctx.check_hostname = False
        ssl_ctx.verify_mode = ssl_mod.CERT_NONE
        connect_args['ssl'] = ssl_ctx
        db_url = db_url.split('?')[0]

    engine = create_async_engine(db_url, echo=True, connect_args=connect_args)
    SessionLocal = async_sessionmaker(engine, class_=AsyncSession, expire_on_commit=False)

    # Create all tables
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
        print("Tables created.")

    # Add missing columns for manual assessment
    from sqlalchemy import text
    async with engine.begin() as conn:
        for col in ['product_group', 'product', 'team']:
            try:
                await conn.execute(text(
                    f'ALTER TABLE manual_assessment_responses ADD COLUMN {col} VARCHAR'
                ))
                print(f"  Added column: {col}")
            except Exception as e:
                if 'already exists' in str(e).lower():
                    print(f"  Column {col} already exists")
                else:
                    print(f"  Warning adding {col}: {e}")

    # Seed demo projects
    from backend.database.models import Project
    from sqlalchemy import select
    import json

    demo_projects = [
        {
            "id": "75651cda-4725-407c-a4e3-430d0137c2b3",
            "name": "US Bank — Digital Banking Platform",
            "organization": "US Bank",
            "industry": "Banking & Financial Services",
            "team": "Rasabee",
            "product_groups": json.dumps([
                {"name": "RetailNL Tech", "products": [
                    {"name": "Tribe APF", "teams": ["BeCloud"]},
                    {"name": "Tribe Payments", "teams": ["PARN"]},
                ]}
            ]),
        },
        {
            "id": "86148f61-b697-4761-be69-16c9b0d8b4d4",
            "name": "Centrica UK — Digital Transformation",
            "organization": "Centrica",
            "industry": "Energy & Utilities",
            "team": "Digital Platform",
            "product_groups": json.dumps([
                {"name": "RetailNL Tech", "products": [
                    {"name": "Tribe APF", "teams": ["BeCloud"]},
                    {"name": "Tribe Payments", "teams": ["PARN"]},
                ]}
            ]),
        },
    ]

    async with SessionLocal() as db:
        for proj_data in demo_projects:
            existing = await db.execute(
                select(Project).where(Project.id == proj_data["id"])
            )
            if existing.scalar_one_or_none():
                print(f"  Project {proj_data['name']} already exists")
                continue
            db.add(Project(**proj_data))
            print(f"  Created project: {proj_data['name']}")
        await db.commit()

    # Seed manual assessment demo data for each project
    from backend.routers.manual_assessment import ASSESSMENT_QUESTIONS
    from backend.database.models import ManualAssessmentResponse
    from datetime import datetime

    DEMO_TEAMS = [
        {
            "product_group": "RetailNL Tech", "product": "Tribe APF", "team": "BeCloud",
            "assessor": "Rammurthy Mudaliar",
            "scores": {
                "q01": 1, "q02": 2, "q03": 3, "q04": 2, "q05": 1,
                "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
                "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
                "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
                "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
                "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
            },
        },
        {
            "product_group": "RetailNL Tech", "product": "Tribe Payments", "team": "PARN",
            "assessor": "Jagannathan Jayaraaman",
            "scores": {
                "q01": 1, "q02": 2, "q03": 3, "q04": 3, "q05": 1,
                "q06": 1, "q07": 3, "q08": 3, "q09": 3, "q10": 2,
                "q11": 2, "q12": 2, "q13": 1, "q14": 1, "q15": 2,
                "q16": 3, "q17": 2, "q18": 3, "q19": 3, "q20": 4,
                "q21": 3, "q22": 3, "q23": 2, "q24": 2, "q25": 1,
                "q26": 2, "q27": 1, "q28": 2, "q29": 4, "q30": 3,
            },
        },
    ]

    async with SessionLocal() as db:
        for proj_data in demo_projects:
            pid = proj_data["id"]
            for team_info in DEMO_TEAMS:
                for qid, score in team_info["scores"].items():
                    q = next((q for q in ASSESSMENT_QUESTIONS if q["id"] == qid), None)
                    if not q:
                        continue
                    existing = await db.execute(
                        select(ManualAssessmentResponse).where(
                            ManualAssessmentResponse.project_id == pid,
                            ManualAssessmentResponse.question_id == qid,
                            ManualAssessmentResponse.team == team_info["team"],
                        )
                    )
                    if existing.scalar_one_or_none():
                        continue
                    db.add(ManualAssessmentResponse(
                        project_id=pid,
                        phase_id=q["pillar_id"],
                        question_id=qid,
                        response=str(score),
                        respondent=team_info["assessor"],
                        product_group=team_info["product_group"],
                        product=team_info["product"],
                        team=team_info["team"],
                    ))
            await db.commit()
            print(f"  Seeded assessment data for {proj_data['name']}")

    await engine.dispose()
    print("\nDone! Database seeded successfully.")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python deploy/seed_azure_db.py <DATABASE_URL>")
        print("  e.g.: postgresql+asyncpg://admin:pass@host:5432/stump_db?ssl=require")
        sys.exit(1)
    asyncio.run(seed(sys.argv[1]))
