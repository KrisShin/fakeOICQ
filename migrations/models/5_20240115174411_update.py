from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_contact_user" ADD "communication_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_communication" ADD "latest_message_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_contact_user" ADD CONSTRAINT "fk_tb_conta_tb_commu_fdddff5d" FOREIGN KEY ("communication_id") REFERENCES "tb_communication" ("id") ON DELETE CASCADE;
        ALTER TABLE "tb_communication" ADD CONSTRAINT "fk_tb_commu_tb_messa_308dfe92" FOREIGN KEY ("latest_message_id") REFERENCES "tb_message" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_communication" DROP CONSTRAINT "fk_tb_commu_tb_messa_308dfe92";
        ALTER TABLE "tb_contact_user" DROP CONSTRAINT "fk_tb_conta_tb_commu_fdddff5d";
        ALTER TABLE "tb_contact_user" DROP COLUMN "communication_id";
        ALTER TABLE "tb_communication" DROP COLUMN "latest_message_id";"""
