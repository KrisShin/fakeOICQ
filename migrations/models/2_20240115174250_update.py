from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tb_contact_user" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(32) NOT NULL,
    "is_block" BOOL NOT NULL  DEFAULT False,
    "deleted_time" TIMESTAMPTZ
);
        CREATE TABLE IF NOT EXISTS "tb_user" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "nickname" VARCHAR(32) NOT NULL,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "phone" VARCHAR(16) NOT NULL UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "avatar" VARCHAR(255)   DEFAULT 'default.jpg',
    "contact_users_id" VARCHAR(32) NOT NULL REFERENCES "tb_contact_user" ("id") ON DELETE CASCADE
);
        CREATE TABLE "relate_user_tag" (
    "tag_id" VARCHAR(32) NOT NULL REFERENCES "tb_tag" ("id") ON DELETE CASCADE,
    "tb_user_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "relate_user_tag";
        DROP TABLE IF EXISTS "tb_contact_user";
        DROP TABLE IF EXISTS "tb_user";"""
