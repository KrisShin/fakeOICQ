from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_contact_user" ADD "communication_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_contact_user" ADD "contact_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_contact_user" ADD "me_id" VARCHAR(32) NOT NULL;
        ALTER TABLE "tb_communication" ADD "latest_message_id" VARCHAR(32) NOT NULL;
        CREATE UNIQUE INDEX "uid_tb_contact__me_id_86a6a1" ON "tb_contact_user" ("me_id", "contact_id");
        ALTER TABLE "tb_contact_user" ADD CONSTRAINT "fk_tb_conta_tb_commu_fdddff5d" FOREIGN KEY ("communication_id") REFERENCES "tb_communication" ("id") ON DELETE CASCADE;
        ALTER TABLE "tb_contact_user" ADD CONSTRAINT "fk_tb_conta_tb_user_de7ff20d" FOREIGN KEY ("me_id") REFERENCES "tb_user" ("id") ON DELETE CASCADE;
        ALTER TABLE "tb_contact_user" ADD CONSTRAINT "fk_tb_conta_tb_user_a5e0a15f" FOREIGN KEY ("contact_id") REFERENCES "tb_user" ("id") ON DELETE CASCADE;
        ALTER TABLE "tb_communication" ADD CONSTRAINT "fk_tb_commu_tb_messa_308dfe92" FOREIGN KEY ("latest_message_id") REFERENCES "tb_message" ("id") ON DELETE CASCADE;"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        ALTER TABLE "tb_communication" DROP CONSTRAINT "fk_tb_commu_tb_messa_308dfe92";
        ALTER TABLE "tb_contact_user" DROP CONSTRAINT "fk_tb_conta_tb_user_a5e0a15f";
        ALTER TABLE "tb_contact_user" DROP CONSTRAINT "fk_tb_conta_tb_user_de7ff20d";
        ALTER TABLE "tb_contact_user" DROP CONSTRAINT "fk_tb_conta_tb_commu_fdddff5d";
        DROP INDEX "uid_tb_contact__me_id_86a6a1";
        ALTER TABLE "tb_contact_user" DROP COLUMN "communication_id";
        ALTER TABLE "tb_contact_user" DROP COLUMN "contact_id";
        ALTER TABLE "tb_contact_user" DROP COLUMN "me_id";
        ALTER TABLE "tb_communication" DROP COLUMN "latest_message_id";"""
