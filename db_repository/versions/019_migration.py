from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
professors = Table('professors', post_meta,
    Column('net_id', String(length=64), primary_key=True, nullable=False),
    Column('name', String(length=64)),
    Column('email', String(length=120)),
    Column('password', String(length=128)),
    Column('desc', String(length=10000)),
    Column('interests', String(length=10000)),
)

students = Table('students', post_meta,
    Column('net_id', String(length=64), primary_key=True, nullable=False),
    Column('email', String(length=64)),
    Column('password', String(length=128)),
    Column('name', String(length=64)),
    Column('major', String(length=64)),
    Column('year', Integer),
    Column('skills', String(length=10000)),
    Column('resume', String(length=10000)),
    Column('description', String(length=10000)),
    Column('interests', String(length=10000)),
    Column('favorited_projects', String(length=10000)),
    Column('availability', String(length=10000)),
)

posts = Table('posts', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=120)),
    Column('description', String(length=10000)),
    Column('professor_id', String(length=64)),
    Column('tags', String(length=10000)),
    Column('is_active', Boolean, nullable=False, default=ColumnDefault(True)),
    Column('date_created', DateTime, default=ColumnDefault(sqlalchemy.sql.functions.current_timestamp())),
    Column('date_modified', DateTime, onupdate=ColumnDefault(sqlalchemy.sql.functions.current_timestamp()), default=ColumnDefault(sqlalchemy.sql.functions.current_timestamp())),
    Column('stale_date', DateTime),
    Column('qualifications', String(length=10000)),
    Column('current_students', String(length=10000)),
    Column('desired_skills', String(length=10000)),
    Column('capacity', Integer),
    Column('current_number', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['professors'].columns['password'].create()
    post_meta.tables['students'].columns['password'].create()
    post_meta.tables['posts'].columns['stale_date'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['professors'].columns['password'].drop()
    post_meta.tables['students'].columns['password'].drop()
    post_meta.tables['posts'].columns['stale_date'].drop()

