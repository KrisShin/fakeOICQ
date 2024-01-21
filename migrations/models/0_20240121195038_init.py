from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);
CREATE TABLE IF NOT EXISTS "tb_tag" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "key" VARCHAR(128) NOT NULL UNIQUE,
    "description" TEXT
);
CREATE INDEX IF NOT EXISTS "idx_tb_tag_key_ae04b5" ON "tb_tag" ("key");
COMMENT ON TABLE "tb_tag" IS 'The Tag model';
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
    "email" VARCHAR(255)  UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "disabled" BOOL NOT NULL  DEFAULT False,
    "avatar" VARCHAR(255)   DEFAULT 'default.jpg'
);
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
        """
