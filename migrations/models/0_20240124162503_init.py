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
    "key" VARCHAR(128) NOT NULL  PRIMARY KEY,
    "description" TEXT,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP
);
COMMENT ON TABLE "tb_tag" IS 'The Tag model';
CREATE TABLE IF NOT EXISTS "tb_user" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "nickname" VARCHAR(32) NOT NULL,
    "username" VARCHAR(64) NOT NULL UNIQUE,
    "phone" VARCHAR(16)  UNIQUE,
    "email" VARCHAR(255)  UNIQUE,
    "password" VARCHAR(128) NOT NULL,
    "disabled" BOOL NOT NULL  DEFAULT False,
    "avatar" VARCHAR(255)   DEFAULT 'default.jpg'
);
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
CREATE TABLE IF NOT EXISTS "tb_message" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "content" TEXT NOT NULL,
    "message_category" SMALLINT NOT NULL  DEFAULT 1,
    "contact_id" VARCHAR(32) NOT NULL,
    "communication_id" VARCHAR(32) NOT NULL
);
CREATE INDEX IF NOT EXISTS "idx_tb_message_contact_d387d7" ON "tb_message" ("contact_id");
CREATE INDEX IF NOT EXISTS "idx_tb_message_communi_b6fcc9" ON "tb_message" ("communication_id");
COMMENT ON COLUMN "tb_message"."message_category" IS 'TEXT: 1\nIMAGE: 2\nVEDIO: 3\nLINK: 4\nAUDIO: 5\nFILE: 6';
COMMENT ON TABLE "tb_message" IS 'message';
CREATE TABLE IF NOT EXISTS "tb_communication" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "has_history" BOOL NOT NULL  DEFAULT False,
    "new_count" INT NOT NULL  DEFAULT 0,
    "latest_message_id" VARCHAR(32) REFERENCES "tb_message" ("id") ON DELETE CASCADE
);
COMMENT ON TABLE "tb_communication" IS 'communication';
CREATE TABLE IF NOT EXISTS "tb_contact_user" (
    "id" VARCHAR(32) NOT NULL  PRIMARY KEY,
    "create_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "update_time" TIMESTAMPTZ NOT NULL  DEFAULT CURRENT_TIMESTAMP,
    "name" VARCHAR(32) NOT NULL,
    "is_block" BOOL NOT NULL  DEFAULT False,
    "deleted_time" TIMESTAMPTZ,
    "communication_id" VARCHAR(32) NOT NULL REFERENCES "tb_communication" ("id") ON DELETE CASCADE,
    "contact_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE,
    "me_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE,
    CONSTRAINT "uid_tb_contact__me_id_86a6a1" UNIQUE ("me_id", "contact_id")
);
CREATE TABLE IF NOT EXISTS "relate_user_tag" (
    "tb_user_id" VARCHAR(32) NOT NULL REFERENCES "tb_user" ("id") ON DELETE CASCADE,
    "tag_id" VARCHAR(128) NOT NULL REFERENCES "tb_tag" ("key") ON DELETE CASCADE
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
