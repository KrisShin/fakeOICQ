--
-- PostgreSQL database dump
--

-- Dumped from database version 16.1
-- Dumped by pg_dump version 16.1

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: aerich; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.aerich (
    id integer NOT NULL,
    version character varying(255) NOT NULL,
    app character varying(100) NOT NULL,
    content jsonb NOT NULL
);


ALTER TABLE public.aerich OWNER TO oicquser;

--
-- Name: aerich_id_seq; Type: SEQUENCE; Schema: public; Owner: oicquser
--

CREATE SEQUENCE public.aerich_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.aerich_id_seq OWNER TO oicquser;

--
-- Name: aerich_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: oicquser
--

ALTER SEQUENCE public.aerich_id_seq OWNED BY public.aerich.id;


--
-- Name: relate_user_tag; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.relate_user_tag (
    tag_id character varying(32) NOT NULL,
    tb_user_id character varying(32) NOT NULL
);


ALTER TABLE public.relate_user_tag OWNER TO oicquser;

--
-- Name: tb_communication; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.tb_communication (
    id character varying(32) NOT NULL,
    create_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    has_history boolean DEFAULT false NOT NULL,
    new_count integer DEFAULT 0 NOT NULL,
    latest_message_id character varying(32)
);


ALTER TABLE public.tb_communication OWNER TO oicquser;

--
-- Name: TABLE tb_communication; Type: COMMENT; Schema: public; Owner: oicquser
--

COMMENT ON TABLE public.tb_communication IS 'communication';


--
-- Name: tb_contact_user; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.tb_contact_user (
    id character varying(32) NOT NULL,
    create_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    name character varying(32) NOT NULL,
    is_block boolean DEFAULT false NOT NULL,
    deleted_time timestamp with time zone,
    contact_id character varying(32) NOT NULL,
    communication_id character varying(32) NOT NULL,
    me_id character varying(32) NOT NULL
);


ALTER TABLE public.tb_contact_user OWNER TO oicquser;

--
-- Name: tb_message; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.tb_message (
    id character varying(32) NOT NULL,
    create_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    content text NOT NULL,
    message_category smallint NOT NULL,
    contact_id character varying(32) NOT NULL,
    communication_id character varying(32) NOT NULL
);


ALTER TABLE public.tb_message OWNER TO oicquser;

--
-- Name: TABLE tb_message; Type: COMMENT; Schema: public; Owner: oicquser
--

COMMENT ON TABLE public.tb_message IS 'message';


--
-- Name: COLUMN tb_message.message_category; Type: COMMENT; Schema: public; Owner: oicquser
--

COMMENT ON COLUMN public.tb_message.message_category IS 'TEXT: 1\nIMAGE: 2\nVEDIO: 3\nLINK: 4\nAUDIO: 5\nFILE: 6';


--
-- Name: tb_tag; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.tb_tag (
    id character varying(32) NOT NULL,
    create_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    key character varying(128) NOT NULL,
    description text
);


ALTER TABLE public.tb_tag OWNER TO oicquser;

--
-- Name: TABLE tb_tag; Type: COMMENT; Schema: public; Owner: oicquser
--

COMMENT ON TABLE public.tb_tag IS 'The Tag model';


--
-- Name: tb_user; Type: TABLE; Schema: public; Owner: oicquser
--

CREATE TABLE public.tb_user (
    id character varying(32) NOT NULL,
    create_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    update_time timestamp with time zone DEFAULT CURRENT_TIMESTAMP NOT NULL,
    nickname character varying(32) NOT NULL,
    username character varying(64) NOT NULL,
    phone character varying(16) NOT NULL,
    email character varying(255),
    password character varying(128) NOT NULL,
    disabled boolean DEFAULT false NOT NULL,
    avatar character varying(255) DEFAULT 'default.jpg'::character varying
);


ALTER TABLE public.tb_user OWNER TO oicquser;

--
-- Name: aerich id; Type: DEFAULT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.aerich ALTER COLUMN id SET DEFAULT nextval('public.aerich_id_seq'::regclass);


--
-- Data for Name: aerich; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.aerich (id, version, app, content) FROM stdin;
1	0_20240121195038_init.py	models	{"models.Tag": {"app": "models", "name": "models.Tag", "table": "tb_tag", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "The Tag model", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "key", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 128}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(128)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}], "description": "The Tag model", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.User": {"app": "models", "name": "models.User", "table": "tb_user", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "nickname", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "nickname", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "username", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "username", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 64}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(64)"}}, {"name": "phone", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 16}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(16)"}}, {"name": "email", "unique": true, "default": null, "indexed": true, "nullable": true, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "password", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 128}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(128)"}}, {"name": "disabled", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "disabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "avatar", "unique": false, "default": "default.jpg", "indexed": false, "nullable": true, "db_column": "avatar", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Message": {"app": "models", "name": "models.Message", "table": "tb_message", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "message", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "message_category", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message_category", "docstring": null, "generated": false, "field_type": "IntEnumFieldInstance", "constraints": {"ge": -32768, "le": 32767}, "description": "TEXT: 1\\nIMAGE: 2\\nVEDIO: 3\\nLINK: 4\\nAUDIO: 5\\nFILE: 6", "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "contact_id", "unique": false, "default": null, "indexed": true, "nullable": false, "db_column": "contact_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "communication_id", "unique": false, "default": null, "indexed": true, "nullable": false, "db_column": "communication_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}], "description": "message", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.ContactUser": {"app": "models", "name": "models.ContactUser", "table": "tb_contact_user", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "is_block", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_block", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "deleted_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": true, "db_column": "deleted_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {}, "description": null, "python_type": "datetime.datetime", "auto_now_add": false, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Communication": {"app": "models", "name": "models.Communication", "table": "tb_communication", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "communication", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "has_history", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "has_history", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "new_count", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "new_count", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}], "description": "communication", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}}
2	1_20240121195159_update.py	models	{"models.Tag": {"app": "models", "name": "models.Tag", "table": "tb_tag", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "The Tag model", "fk_fields": [], "m2m_fields": [{"name": "users", "unique": false, "default": null, "indexed": false, "through": "relate_user_tag", "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "_generated": true, "field_type": "ManyToManyFieldInstance", "model_name": "models.User", "constraints": {}, "description": null, "forward_key": "tb_user_id", "python_type": "models.User", "backward_key": "tag_id", "related_name": "tags", "db_constraint": true}], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "key", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "key", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 128}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(128)"}}, {"name": "description", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "description", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}], "description": "The Tag model", "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.User": {"app": "models", "name": "models.User", "table": "tb_user", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": null, "fk_fields": [], "m2m_fields": [{"name": "tags", "unique": false, "default": null, "indexed": false, "through": "relate_user_tag", "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "_generated": false, "field_type": "ManyToManyFieldInstance", "model_name": "models.Tag", "constraints": {}, "description": null, "forward_key": "tag_id", "python_type": "models.Tag", "backward_key": "tb_user_id", "related_name": "users", "db_constraint": true}], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "nickname", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "nickname", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "username", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "username", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 64}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(64)"}}, {"name": "phone", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "phone", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 16}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(16)"}}, {"name": "email", "unique": true, "default": null, "indexed": true, "nullable": true, "db_column": "email", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "password", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "password", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 128}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(128)"}}, {"name": "disabled", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "disabled", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "avatar", "unique": false, "default": "default.jpg", "indexed": false, "nullable": true, "db_column": "avatar", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}], "description": null, "unique_together": [], "backward_fk_fields": [{"name": "tb_contact_users", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.ContactUser", "db_constraint": true}, {"name": "contacts", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.ContactUser", "db_constraint": true}], "backward_o2o_fields": []}, "models.Aerich": {"app": "models", "name": "models.Aerich", "table": "aerich", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": null, "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": true, "field_type": "IntField", "constraints": {"ge": 1, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, "docstring": null, "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "version", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "version", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 255}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(255)"}}, {"name": "app", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "app", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 100}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(100)"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "JSONField", "constraints": {}, "description": null, "python_type": "Union[dict, list]", "db_field_types": {"": "JSON", "mssql": "NVARCHAR(MAX)", "oracle": "NCLOB", "postgres": "JSONB"}}], "description": null, "unique_together": [], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Message": {"app": "models", "name": "models.Message", "table": "tb_message", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "message", "fk_fields": [], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "content", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "content", "docstring": null, "generated": false, "field_type": "TextField", "constraints": {}, "description": null, "python_type": "str", "db_field_types": {"": "TEXT", "mssql": "NVARCHAR(MAX)", "mysql": "LONGTEXT", "oracle": "NCLOB"}}, {"name": "message_category", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "message_category", "docstring": null, "generated": false, "field_type": "IntEnumFieldInstance", "constraints": {"ge": -32768, "le": 32767}, "description": "TEXT: 1\\nIMAGE: 2\\nVEDIO: 3\\nLINK: 4\\nAUDIO: 5\\nFILE: 6", "python_type": "int", "db_field_types": {"": "SMALLINT"}}, {"name": "contact_id", "unique": false, "default": null, "indexed": true, "nullable": false, "db_column": "contact_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "communication_id", "unique": false, "default": null, "indexed": true, "nullable": false, "db_column": "communication_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}], "description": "message", "unique_together": [], "backward_fk_fields": [{"name": "tb_communications", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.Communication", "db_constraint": true}], "backward_o2o_fields": []}, "models.ContactUser": {"app": "models", "name": "models.ContactUser", "table": "tb_contact_user", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": null, "fk_fields": [{"name": "me", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "me_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "contact", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "contact_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.User", "db_constraint": true}, {"name": "communication", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "communication_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Communication", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "name", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "name", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "is_block", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "is_block", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "deleted_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": true, "db_column": "deleted_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {}, "description": null, "python_type": "datetime.datetime", "auto_now_add": false, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "communication_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "communication_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "contact_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "contact_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, {"name": "me_id", "unique": false, "default": null, "indexed": false, "nullable": false, "db_column": "me_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}], "description": null, "unique_together": [["me", "contact"]], "backward_fk_fields": [], "backward_o2o_fields": []}, "models.Communication": {"app": "models", "name": "models.Communication", "table": "tb_communication", "indexes": [], "abstract": false, "pk_field": {"name": "id", "unique": true, "default": "<function modules.common.utils.generate_random_id>", "indexed": true, "nullable": false, "db_column": "id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}, "docstring": "communication", "fk_fields": [{"name": "latest_message", "unique": false, "default": null, "indexed": false, "nullable": true, "docstring": null, "generated": false, "on_delete": "CASCADE", "raw_field": "latest_message_id", "field_type": "ForeignKeyFieldInstance", "constraints": {}, "description": null, "python_type": "models.Message", "db_constraint": true}], "m2m_fields": [], "o2o_fields": [], "data_fields": [{"name": "create_time", "unique": false, "default": null, "indexed": false, "auto_now": false, "nullable": false, "db_column": "create_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "update_time", "unique": false, "default": null, "indexed": false, "auto_now": true, "nullable": false, "db_column": "update_time", "docstring": null, "generated": false, "field_type": "DatetimeField", "constraints": {"readOnly": true}, "description": null, "python_type": "datetime.datetime", "auto_now_add": true, "db_field_types": {"": "TIMESTAMP", "mssql": "DATETIME2", "mysql": "DATETIME(6)", "oracle": "TIMESTAMP WITH TIME ZONE", "postgres": "TIMESTAMPTZ"}}, {"name": "has_history", "unique": false, "default": false, "indexed": false, "nullable": false, "db_column": "has_history", "docstring": null, "generated": false, "field_type": "BooleanField", "constraints": {}, "description": null, "python_type": "bool", "db_field_types": {"": "BOOL", "mssql": "BIT", "oracle": "NUMBER(1)", "sqlite": "INT"}}, {"name": "new_count", "unique": false, "default": 0, "indexed": false, "nullable": false, "db_column": "new_count", "docstring": null, "generated": false, "field_type": "IntField", "constraints": {"ge": -2147483648, "le": 2147483647}, "description": null, "python_type": "int", "db_field_types": {"": "INT"}}, {"name": "latest_message_id", "unique": false, "default": null, "indexed": false, "nullable": true, "db_column": "latest_message_id", "docstring": null, "generated": false, "field_type": "CharField", "constraints": {"max_length": 32}, "description": null, "python_type": "str", "db_field_types": {"": "VARCHAR(32)"}}], "description": "communication", "unique_together": [], "backward_fk_fields": [{"name": "contact_users", "unique": false, "default": null, "indexed": false, "nullable": false, "docstring": null, "generated": false, "field_type": "BackwardFKRelation", "constraints": {}, "description": null, "python_type": "models.ContactUser", "db_constraint": true}], "backward_o2o_fields": []}}
\.


--
-- Data for Name: relate_user_tag; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.relate_user_tag (tag_id, tb_user_id) FROM stdin;
1705838323075003vka76nc0f8pjdqdw	170584104676442157cdhsfboimgiaqz
17058383230474456u2ti53pomlb37i3	17058410470311996onnr0g5qqza9hbh
17058383230726206b3qu6asrz6oogcf	17058410470311996onnr0g5qqza9hbh
1705838323073740drlgb8r2g7ln2tqz	17058410470311996onnr0g5qqza9hbh
1705838323068315n0rovweahc46kogw	1705841047277685lmqm7shutwjmkihc
1705838323075003vka76nc0f8pjdqdw	1705841047527071ox5k3vc09otmlb4y
\.


--
-- Data for Name: tb_communication; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.tb_communication (id, create_time, update_time, has_history, new_count, latest_message_id) FROM stdin;
170584104756192382qy1we318ma01ii	2024-01-21 20:44:07.562327+08	2024-01-21 20:44:07.562345+08	f	0	\N
17058410475683780hshepw70559lphf	2024-01-21 20:44:07.568442+08	2024-01-21 20:44:07.568457+08	f	0	\N
17058410475717719o7f9grer7hedrtl	2024-01-21 20:44:07.571834+08	2024-01-21 20:44:07.571849+08	f	0	\N
1705841047575003nus1dmi966mt4ptv	2024-01-21 20:44:07.575065+08	2024-01-21 20:44:07.575079+08	f	0	\N
1705841047579283up47mqapze2clxbo	2024-01-21 20:44:07.579345+08	2024-01-21 20:44:07.579359+08	f	0	\N
\.


--
-- Data for Name: tb_contact_user; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.tb_contact_user (id, create_time, update_time, name, is_block, deleted_time, contact_id, communication_id, me_id) FROM stdin;
1705841047564363dxo5fokao0idfb5z	2024-01-21 20:44:07.564784+08	2024-01-21 20:44:07.5648+08	nickname_test2	f	\N	17058410470311996onnr0g5qqza9hbh	170584104756192382qy1we318ma01ii	170584104676442157cdhsfboimgiaqz
1705841047567062tb1cwxm3txgwdybm	2024-01-21 20:44:07.567126+08	2024-01-21 20:44:07.567141+08	nickname_test1	f	\N	170584104676442157cdhsfboimgiaqz	170584104756192382qy1we318ma01ii	17058410470311996onnr0g5qqza9hbh
1705841047569507bc3vsimrmffj88x6	2024-01-21 20:44:07.569586+08	2024-01-21 20:44:07.569603+08	nickname_test3	f	\N	1705841047277685lmqm7shutwjmkihc	17058410475683780hshepw70559lphf	170584104676442157cdhsfboimgiaqz
17058410475707648y9g7yb2dqsxjmg0	2024-01-21 20:44:07.570827+08	2024-01-21 20:44:07.570843+08	nickname_test1	f	\N	170584104676442157cdhsfboimgiaqz	17058410475683780hshepw70559lphf	1705841047277685lmqm7shutwjmkihc
1705841047572573jgg9pb0nxawdamqw	2024-01-21 20:44:07.572633+08	2024-01-21 20:44:07.572648+08	nickname_test4	f	\N	1705841047527071ox5k3vc09otmlb4y	17058410475717719o7f9grer7hedrtl	170584104676442157cdhsfboimgiaqz
1705841047573668zp3lkz0etdnt51uk	2024-01-21 20:44:07.573727+08	2024-01-21 20:44:07.573742+08	nickname_test1	f	\N	170584104676442157cdhsfboimgiaqz	17058410475717719o7f9grer7hedrtl	1705841047527071ox5k3vc09otmlb4y
1705841047576126gmwaydvhlxl98uht	2024-01-21 20:44:07.576188+08	2024-01-21 20:44:07.576203+08	nickname_test3	f	\N	1705841047277685lmqm7shutwjmkihc	1705841047575003nus1dmi966mt4ptv	17058410470311996onnr0g5qqza9hbh
1705841047577859o5dbqpawk1e5u6y0	2024-01-21 20:44:07.577918+08	2024-01-21 20:44:07.577932+08	nickname_test2	f	\N	17058410470311996onnr0g5qqza9hbh	1705841047575003nus1dmi966mt4ptv	1705841047277685lmqm7shutwjmkihc
1705841047580318lp7mf8pkoseenioo	2024-01-21 20:44:07.580376+08	2024-01-21 20:44:07.58039+08	nickname_test4	f	\N	1705841047527071ox5k3vc09otmlb4y	1705841047579283up47mqapze2clxbo	1705841047277685lmqm7shutwjmkihc
1705841047581353tz242qcvdelyk3by	2024-01-21 20:44:07.581411+08	2024-01-21 20:44:07.581425+08	nickname_test3	f	\N	1705841047277685lmqm7shutwjmkihc	1705841047579283up47mqapze2clxbo	1705841047527071ox5k3vc09otmlb4y
\.


--
-- Data for Name: tb_message; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.tb_message (id, create_time, update_time, content, message_category, contact_id, communication_id) FROM stdin;
\.


--
-- Data for Name: tb_tag; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.tb_tag (id, create_time, update_time, key, description) FROM stdin;
17058383230474456u2ti53pomlb37i3	2024-01-21 19:58:43.049216+08	2024-01-21 19:58:43.049275+08	cool	cool
1705838323068315n0rovweahc46kogw	2024-01-21 19:58:43.068453+08	2024-01-21 19:58:43.068481+08	beauty	beauty
1705838323069544sdgz8wykkxblf7tm	2024-01-21 19:58:43.069636+08	2024-01-21 19:58:43.069659+08	giao	giao
1705838323070642e3n8o6xjr60kvrin	2024-01-21 19:58:43.070728+08	2024-01-21 19:58:43.07075+08	game	game
1705838323071638iqi8kz94nork48x7	2024-01-21 19:58:43.071721+08	2024-01-21 19:58:43.071743+08	animal	animal
17058383230726206b3qu6asrz6oogcf	2024-01-21 19:58:43.072702+08	2024-01-21 19:58:43.072724+08	program	program
1705838323073740drlgb8r2g7ln2tqz	2024-01-21 19:58:43.073821+08	2024-01-21 19:58:43.073844+08	python	python
1705838323075003vka76nc0f8pjdqdw	2024-01-21 19:58:43.075112+08	2024-01-21 19:58:43.075139+08	finance	finance
17058383230763410rpkccaps4slp35v	2024-01-21 19:58:43.076425+08	2024-01-21 19:58:43.076448+08	geography	geography
\.


--
-- Data for Name: tb_user; Type: TABLE DATA; Schema: public; Owner: oicquser
--

COPY public.tb_user (id, create_time, update_time, nickname, username, phone, email, password, disabled, avatar) FROM stdin;
170584104676442157cdhsfboimgiaqz	2024-01-21 20:44:06.765755+08	2024-01-21 20:44:06.765802+08	nickname_test1	test1	13123447805	\N	$2b$12$O5VjqGYEHBugMqbWlZeqJulDzDwLzzz4mlrytKG0/POS4pVZbb51O	f	default.jpg
17058410470311996onnr0g5qqza9hbh	2024-01-21 20:44:07.031322+08	2024-01-21 20:44:07.031344+08	nickname_test2	test2	13123415443	\N	$2b$12$PtRMuT5vfN3sUL.mh/EnQ.cX7hK/zxXfxWk0S10Ibz0DgRa70x4/S	f	default.jpg
1705841047277685lmqm7shutwjmkihc	2024-01-21 20:44:07.2778+08	2024-01-21 20:44:07.277823+08	nickname_test3	test3	13123461390	\N	$2b$12$Gzz9DFy7aSlNqHjwQhwL6usLgSCTxrWki64KxoJ1kVhi8Hov2Ws.u	f	default.jpg
1705841047527071ox5k3vc09otmlb4y	2024-01-21 20:44:07.527172+08	2024-01-21 20:44:07.527193+08	nickname_test4	test4	13123449609	\N	$2b$12$P0Dymy5DsDlzWb402Wette8CKIX1PYaywJxUIffVOFxdnjx9y0S2i	f	default.jpg
\.


--
-- Name: aerich_id_seq; Type: SEQUENCE SET; Schema: public; Owner: oicquser
--

SELECT pg_catalog.setval('public.aerich_id_seq', 2, true);


--
-- Name: aerich aerich_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.aerich
    ADD CONSTRAINT aerich_pkey PRIMARY KEY (id);


--
-- Name: tb_communication tb_communication_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_communication
    ADD CONSTRAINT tb_communication_pkey PRIMARY KEY (id);


--
-- Name: tb_contact_user tb_contact_user_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_contact_user
    ADD CONSTRAINT tb_contact_user_pkey PRIMARY KEY (id);


--
-- Name: tb_message tb_message_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_message
    ADD CONSTRAINT tb_message_pkey PRIMARY KEY (id);


--
-- Name: tb_tag tb_tag_key_key; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_tag
    ADD CONSTRAINT tb_tag_key_key UNIQUE (key);


--
-- Name: tb_tag tb_tag_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_tag
    ADD CONSTRAINT tb_tag_pkey PRIMARY KEY (id);


--
-- Name: tb_user tb_user_email_key; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_user
    ADD CONSTRAINT tb_user_email_key UNIQUE (email);


--
-- Name: tb_user tb_user_phone_key; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_user
    ADD CONSTRAINT tb_user_phone_key UNIQUE (phone);


--
-- Name: tb_user tb_user_pkey; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_user
    ADD CONSTRAINT tb_user_pkey PRIMARY KEY (id);


--
-- Name: tb_user tb_user_username_key; Type: CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_user
    ADD CONSTRAINT tb_user_username_key UNIQUE (username);


--
-- Name: idx_tb_message_communi_b6fcc9; Type: INDEX; Schema: public; Owner: oicquser
--

CREATE INDEX idx_tb_message_communi_b6fcc9 ON public.tb_message USING btree (communication_id);


--
-- Name: idx_tb_message_contact_d387d7; Type: INDEX; Schema: public; Owner: oicquser
--

CREATE INDEX idx_tb_message_contact_d387d7 ON public.tb_message USING btree (contact_id);


--
-- Name: idx_tb_tag_key_ae04b5; Type: INDEX; Schema: public; Owner: oicquser
--

CREATE INDEX idx_tb_tag_key_ae04b5 ON public.tb_tag USING btree (key);


--
-- Name: uid_tb_contact__me_id_86a6a1; Type: INDEX; Schema: public; Owner: oicquser
--

CREATE UNIQUE INDEX uid_tb_contact__me_id_86a6a1 ON public.tb_contact_user USING btree (me_id, contact_id);


--
-- Name: tb_communication fk_tb_commu_tb_messa_308dfe92; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_communication
    ADD CONSTRAINT fk_tb_commu_tb_messa_308dfe92 FOREIGN KEY (latest_message_id) REFERENCES public.tb_message(id) ON DELETE CASCADE;


--
-- Name: tb_contact_user fk_tb_conta_tb_commu_fdddff5d; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_contact_user
    ADD CONSTRAINT fk_tb_conta_tb_commu_fdddff5d FOREIGN KEY (communication_id) REFERENCES public.tb_communication(id) ON DELETE CASCADE;


--
-- Name: tb_contact_user fk_tb_conta_tb_user_a5e0a15f; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_contact_user
    ADD CONSTRAINT fk_tb_conta_tb_user_a5e0a15f FOREIGN KEY (contact_id) REFERENCES public.tb_user(id) ON DELETE CASCADE;


--
-- Name: tb_contact_user fk_tb_conta_tb_user_de7ff20d; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.tb_contact_user
    ADD CONSTRAINT fk_tb_conta_tb_user_de7ff20d FOREIGN KEY (me_id) REFERENCES public.tb_user(id) ON DELETE CASCADE;


--
-- Name: relate_user_tag relate_user_tag_tag_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.relate_user_tag
    ADD CONSTRAINT relate_user_tag_tag_id_fkey FOREIGN KEY (tag_id) REFERENCES public.tb_tag(id) ON DELETE CASCADE;


--
-- Name: relate_user_tag relate_user_tag_tb_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: oicquser
--

ALTER TABLE ONLY public.relate_user_tag
    ADD CONSTRAINT relate_user_tag_tb_user_id_fkey FOREIGN KEY (tb_user_id) REFERENCES public.tb_user(id) ON DELETE CASCADE;


--
-- PostgreSQL database dump complete
--

