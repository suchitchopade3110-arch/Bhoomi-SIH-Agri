import asyncio
import asyncpg

async def main():
    try:
        conn = await asyncpg.connect('postgresql://postgres:postgres@localhost:5432/bhoomi')
        version = await conn.fetchval('SELECT version();')
        print(f"Version: {version}")
        
        # Also show the setting for 'dynamic_library_path' and 'extension' search paths
        ext_path = await conn.fetchval("SHOW show_directory_settings;")
        print(f"Directory: {ext_path}")
        await conn.close()
    except Exception as e:
        print(f"Error: {e}")

if __name__ == '__main__':
    asyncio.run(main())
