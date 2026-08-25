import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/bhoomi')
    rows = await conn.fetch("SELECT name, default_version, installed_version, comment FROM pg_available_extensions ORDER BY name")
    for r in rows:
        if 'vector' in r['name'] or 'gis' in r['name'] or 'post' in r['name']:
            print(dict(r))
    await conn.close()

if __name__ == '__main__':
    asyncio.run(main())
