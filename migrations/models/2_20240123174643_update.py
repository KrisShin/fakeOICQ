from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tb_contact_request" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "status" VARCHAR(7) NOT NULL  DEFAULT 'request',
    "message" VARCHAR(256),
    "reply" VARCHAR(512),
    "contact_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE,
    "me_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE
);
COMMENT ON COLUMN "tb_contact_request"."status" IS 'REQUEST: request\nACCEPT: accept\nDECLINE: decline';
        ALTER TABLE "tb_user" ALTER COLUMN "phone" DROP NOT NULL;
        ALTER TABLE "tb_message" ALTER COLUMN "message_category" SET DEFAULT 1;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_user" ALTER COLUMN "phone" SET NOT NULL;
        ALTER TABLE "tb_message" ALTER COLUMN "message_category" DROP DEFAULT;
        DROP TABLE IF EXISTS "tb_contact_request";"""
