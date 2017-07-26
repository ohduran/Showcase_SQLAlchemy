from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
loan = Table('loan', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('balance', Integer),
    Column('currency', String(length=3)),
    Column('user_id', Integer),
)

report = Table('report', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('title', String(length=255)),
    Column('body', String(length=1500)),
    Column('user_id', Integer),
)

reports_loans = Table('reports_loans', post_meta,
    Column('report_id', Integer),
    Column('loan_id', Integer),
)

user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('name', String(length=255)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['loan'].create()
    post_meta.tables['report'].create()
    post_meta.tables['reports_loans'].create()
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['loan'].drop()
    post_meta.tables['report'].drop()
    post_meta.tables['reports_loans'].drop()
    post_meta.tables['user'].drop()
