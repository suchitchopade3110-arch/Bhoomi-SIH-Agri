-- Enable PostGIS and pgvector extensions on Bhoomi database
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS vector;
-- CREATE EXTENSION IF NOT EXISTS postgis; -- Available when using postgis-enabled image
