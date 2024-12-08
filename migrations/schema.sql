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
-- Name: document; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document (
    name character varying NOT NULL,
    mime character varying NOT NULL,
    created_at bigint NOT NULL,
    indexed boolean NOT NULL,
    id integer NOT NULL
);


--
-- Name: document_chunk; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_chunk (
    doc_id integer NOT NULL,
    page_id integer NOT NULL,
    image bytea NOT NULL,
    id integer NOT NULL
);


--
-- Name: document_chunk_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_chunk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_chunk_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_chunk_id_seq OWNED BY public.document_chunk.id;


--
-- Name: document_content; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_content (
    doc_id integer NOT NULL,
    content bytea NOT NULL,
    id integer NOT NULL
);


--
-- Name: document_content_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_content_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_content_id_seq OWNED BY public.document_content.id;


--
-- Name: document_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_id_seq OWNED BY public.document.id;


--
-- Name: document_page; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.document_page (
    doc_id integer NOT NULL,
    number integer NOT NULL,
    image bytea NOT NULL,
    id integer NOT NULL
);


--
-- Name: document_page_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.document_page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: document_page_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.document_page_id_seq OWNED BY public.document_page.id;


--
-- Name: schema_migrations; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.schema_migrations (
    version character varying(128) NOT NULL
);


--
-- Name: document id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document ALTER COLUMN id SET DEFAULT nextval('public.document_id_seq'::regclass);


--
-- Name: document_chunk id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunk ALTER COLUMN id SET DEFAULT nextval('public.document_chunk_id_seq'::regclass);


--
-- Name: document_content id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_content ALTER COLUMN id SET DEFAULT nextval('public.document_content_id_seq'::regclass);


--
-- Name: document_page id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_page ALTER COLUMN id SET DEFAULT nextval('public.document_page_id_seq'::regclass);


--
-- Name: document_chunk document_chunk_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_pkey PRIMARY KEY (id);


--
-- Name: document_content document_content_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_content
    ADD CONSTRAINT document_content_pkey PRIMARY KEY (id);


--
-- Name: document_page document_page_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_page
    ADD CONSTRAINT document_page_pkey PRIMARY KEY (id);


--
-- Name: document document_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);


--
-- Name: schema_migrations schema_migrations_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.schema_migrations
    ADD CONSTRAINT schema_migrations_pkey PRIMARY KEY (version);


--
-- Name: document_chunk document_chunk_doc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);


--
-- Name: document_chunk document_chunk_page_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.document_page(id);


--
-- Name: document_content document_content_doc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_content
    ADD CONSTRAINT document_content_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);


--
-- Name: document_page document_page_doc_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.document_page
    ADD CONSTRAINT document_page_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);


--
-- PostgreSQL database dump complete
--


--
-- Dbmate schema migrations
--

INSERT INTO public.schema_migrations (version) VALUES
    ('19990101000000');
