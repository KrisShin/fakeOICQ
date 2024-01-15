from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "tb_communication" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "has_history" BOOL NOT NULL  DEFAULT False,
    "new_count" INT NOT NULL  DEFAULT 0
);
COMMENT ON TABLE "tb_communication" IS 'communication';
        CREATE TABLE IF NOT EXISTS "tb_message" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "content" TEXT NOT NULL,
    "message_category" SMALLINT NOT NULL,
    "contact_id" VARCHAR(32) NOT NULL,
    "communication_id" VARCHAR(32) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_tb_message_contact_d387d7" ON "tb_message" ("contact_id");
CREATE INDEX IF NOT EXISTS "idx_tb_message_communi_b6fcc9" ON "tb_message" ("communication_id");
COMMENT ON COLUMN "tb_message"."message_category" IS 'TEXT: 1\nIMAGE: 2\nVEDIO: 3\nLINK: 4\nAUDIO: 5\nFILE: 6';
COMMENT ON TABLE "tb_message" IS 'message';"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        DROP TABLE IF EXISTS "tb_communication";
        DROP TABLE IF EXISTS "tb_message";"""
