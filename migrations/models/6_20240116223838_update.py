from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_user" DROP CONSTRAINT "fk_tb_user_tb_conta_03f77b84";
        ALTER TABLE "tb_user" DROP COLUMN "contact_users_id";"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_user" ADD "contact_users_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_user" ADD CONSTRAINT "fk_tb_user_tb_conta_03f77b84" FOREIGN KEY ("contact_users_id") REFERENCES "tb_contact_user" ("id") ON DELETE CASCADE;"""
