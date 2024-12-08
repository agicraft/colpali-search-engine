-- migrate:up

CREATE TABLE public.document (
    name character varying NOT NULL,
    mime character varying NOT NULL,
    created_at bigint NOT NULL,
    indexed boolean NOT NULL,
    id integer NOT NULL
);

CREATE TABLE public.document_chunk (
    doc_id integer NOT NULL,
    page_id integer NOT NULL,
    image bytea NOT NULL,
    id integer NOT NULL
);

CREATE SEQUENCE public.document_chunk_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.document_chunk_id_seq OWNED BY public.document_chunk.id;

CREATE TABLE public.document_content (
    doc_id integer NOT NULL,
    content bytea NOT NULL,
    id integer NOT NULL
);

CREATE SEQUENCE public.document_content_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.document_content_id_seq OWNED BY public.document_content.id;

CREATE SEQUENCE public.document_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.document_id_seq OWNED BY public.document.id;

CREATE TABLE public.document_page (
    doc_id integer NOT NULL,
    number integer NOT NULL,
    image bytea NOT NULL,
    id integer NOT NULL
);

CREATE SEQUENCE public.document_page_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;

ALTER SEQUENCE public.document_page_id_seq OWNED BY public.document_page.id;

ALTER TABLE ONLY public.document ALTER COLUMN id SET DEFAULT nextval('public.document_id_seq'::regclass);

ALTER TABLE ONLY public.document_chunk ALTER COLUMN id SET DEFAULT nextval('public.document_chunk_id_seq'::regclass);

ALTER TABLE ONLY public.document_content ALTER COLUMN id SET DEFAULT nextval('public.document_content_id_seq'::regclass);

ALTER TABLE ONLY public.document_page ALTER COLUMN id SET DEFAULT nextval('public.document_page_id_seq'::regclass);

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.document_content
    ADD CONSTRAINT document_content_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.document_page
    ADD CONSTRAINT document_page_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.document
    ADD CONSTRAINT document_pkey PRIMARY KEY (id);

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);

ALTER TABLE ONLY public.document_chunk
    ADD CONSTRAINT document_chunk_page_id_fkey FOREIGN KEY (page_id) REFERENCES public.document_page(id);

ALTER TABLE ONLY public.document_content
    ADD CONSTRAINT document_content_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);

ALTER TABLE ONLY public.document_page
    ADD CONSTRAINT document_page_doc_id_fkey FOREIGN KEY (doc_id) REFERENCES public.document(id);

-- migrate:down

DROP TABLE IF EXISTS public.document_chunk;
DROP TABLE IF EXISTS public.document_page;
DROP TABLE IF EXISTS public.document_content;
DROP TABLE IF EXISTS public."document";
