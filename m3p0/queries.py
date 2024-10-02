IS_TABLE_EXISTS_QUERY = """
SELECT EXISTS (
    SELECT FROM information_schema.tables 
    WHERE  table_schema = 'public'
    AND    table_name   = 'M3P0_migrations'
)
"""

CREATE_TABLE_QUERY = """
CREATE TABLE M3P0_migrations (
    id SERIAL,
    version VARCHAR,
    revision UUID,
    is_applied BOOL
)
"""

IS_VERSION_ALREADY_EXIST = """
SELECT EXISTS (
    SELECT version 
    FROM m3p0
    WHERE version = $1
)
"""

RETRIEVE_LAST_REVISION = """
SELECT revision
FROM M3P0_migrations
ORDER BY id DESC
LIMIT 1
"""

RETRIEVE_SORTED_REVISIONS = """
SELECT revision
FROM M3P0_migrations
ORDER BY id DESC
"""
