-- PostgreSQL database dump
--

-- Dumped from database version 16.3 (Postgres.app)
-- Dumped by pg_dump version 16.3 (Postgres.app)

-- Started on 2024-06-25 15:51:12 CEST

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
-- TOC entry 234 (class 1259 OID 16469)
-- Name: attributes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.attributes (
    attribute_id integer NOT NULL,
    attribute_name character varying,
    attribute_description character varying,
    attribute_created timestamp without time zone,
    attribute_modified timestamp without time zone
);


--
-- TOC entry 233 (class 1259 OID 16468)
-- Name: attributes_attribute_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.attributes_attribute_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3739 (class 0 OID 0)
-- Dependencies: 233
-- Name: attributes_attribute_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.attributes_attribute_id_seq OWNED BY public.attributes.attribute_id;


--
-- TOC entry 222 (class 1259 OID 16417)
-- Name: brands; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.brands (
    brand_id integer NOT NULL,
    brand_name character varying,
    brand_noname boolean,
    chain_id integer,
    brand_created timestamp without time zone,
    brand_modified timestamp without time zone
);


--
-- TOC entry 235 (class 1259 OID 16477)
-- Name: brands_attributes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.brands_attributes (
    brand_id integer NOT NULL,
    attribute_id integer NOT NULL,
    brand_attribute_score double precision,
    brand_attribute_created timestamp without time zone,
    brand_attribute_modified timestamp without time zone
);


--
-- TOC entry 221 (class 1259 OID 16416)
-- Name: brands_brand_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.brands_brand_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3740 (class 0 OID 0)
-- Dependencies: 221
-- Name: brands_brand_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.brands_brand_id_seq OWNED BY public.brands.brand_id;


--
-- TOC entry 228 (class 1259 OID 16444)
-- Name: household_members; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.household_members (
    household_member_id integer NOT NULL,
    user_id integer,
    household_member_type character varying,
    household_member_sex character varying(1),
    household_member_age integer
);


--
-- TOC entry 227 (class 1259 OID 16443)
-- Name: household_members_household_member_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.household_members_household_member_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3741 (class 0 OID 0)
-- Dependencies: 227
-- Name: household_members_household_member_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.household_members_household_member_id_seq OWNED BY public.household_members.household_member_id;


--
-- TOC entry 220 (class 1259 OID 16408)
-- Name: payment_methods; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.payment_methods (
    paymentmethod_id integer NOT NULL,
    paymentmethod_name character varying,
    paymentmetod_subtype integer
);


--
-- TOC entry 219 (class 1259 OID 16407)
-- Name: payment_methods_paymentmethod_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.payment_methods_paymentmethod_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3742 (class 0 OID 0)
-- Dependencies: 219
-- Name: payment_methods_paymentmethod_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.payment_methods_paymentmethod_id_seq OWNED BY public.payment_methods.paymentmethod_id;


--
-- TOC entry 226 (class 1259 OID 16435)
-- Name: pets; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.pets (
    pet_id integer NOT NULL,
    user_id integer,
    pet_type character varying,
    pet_age integer,
    pet_status integer
);


--
-- TOC entry 225 (class 1259 OID 16434)
-- Name: pets_pet_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.pets_pet_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3743 (class 0 OID 0)
-- Dependencies: 225
-- Name: pets_pet_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.pets_pet_id_seq OWNED BY public.pets.pet_id;


--
-- TOC entry 232 (class 1259 OID 16462)
-- Name: purchased_products; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchased_products (
    purchased_product_id integer NOT NULL,
    purchase_id integer,
    purchased_product_price double precision,
    purchased_product_qty integer,
    purchased_procuct_includeddiscount double precision,
    purchased_procuct_processed timestamp without time zone,
    purchased_product_name character varying
);


--
-- TOC entry 231 (class 1259 OID 16461)
-- Name: purchased_products_purchased_product_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchased_products_purchased_product_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3744 (class 0 OID 0)
-- Dependencies: 231
-- Name: purchased_products_purchased_product_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchased_products_purchased_product_id_seq OWNED BY public.purchased_products.purchased_product_id;


--
-- TOC entry 230 (class 1259 OID 16453)
-- Name: purchases; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.purchases (
    purchase_id integer NOT NULL,
    branch_id integer,
    user_id integer,
    purchase_sum double precision,
    purchase_time timestamp without time zone,
    paymentmethod_id integer,
    purchase_used_discount_type character varying,
    purchase_processed timestamp without time zone,
    purchase_created timestamp without time zone,
    file_name character varying(255),
    file_path character varying(255),
    receipt_nr character varying,
    document_nr character varying,
    trace_nr character varying,
    cashier_number character varying,
    register_number character varying
);


--
-- TOC entry 229 (class 1259 OID 16452)
-- Name: purchases_purchase_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.purchases_purchase_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3745 (class 0 OID 0)
-- Dependencies: 229
-- Name: purchases_purchase_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.purchases_purchase_id_seq OWNED BY public.purchases.purchase_id;


--
-- TOC entry 218 (class 1259 OID 16399)
-- Name: supermarket_branches; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.supermarket_branches (
    branch_id integer NOT NULL,
    chain_id integer,
    branch_chaininternal_id integer,
    branch_name character varying,
    branch_street character varying,
    branch_plz character varying,
    branch_ort character varying,
    branch_more text,
    branch_specific text,
    branch_created timestamp without time zone,
    branch_tel character varying,
    branch_uid_number character varying
);


--
-- TOC entry 217 (class 1259 OID 16398)
-- Name: supermarket_branches_branch_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.supermarket_branches_branch_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3746 (class 0 OID 0)
-- Dependencies: 217
-- Name: supermarket_branches_branch_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.supermarket_branches_branch_id_seq OWNED BY public.supermarket_branches.branch_id;


--
-- TOC entry 216 (class 1259 OID 16390)
-- Name: supermarket_chains; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.supermarket_chains (
    chain_id integer NOT NULL,
    chain_name character varying,
    chain_shortname character varying,
    chain_api_type integer,
    chain_api_endpoint text,
    chain_created timestamp without time zone
);


--
-- TOC entry 215 (class 1259 OID 16389)
-- Name: supermarket_chains_chain_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.supermarket_chains_chain_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3747 (class 0 OID 0)
-- Dependencies: 215
-- Name: supermarket_chains_chain_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.supermarket_chains_chain_id_seq OWNED BY public.supermarket_chains.chain_id;


--
-- TOC entry 224 (class 1259 OID 16426)
-- Name: users; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users (
    user_id integer NOT NULL,
    user_name character varying,
    user_email character varying,
    user_created timestamp without time zone,
    user_password character varying(255)
);


--
-- TOC entry 236 (class 1259 OID 16482)
-- Name: users_attributes; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.users_attributes (
    attribute_id integer NOT NULL,
    user_id integer NOT NULL,
    user_attribute_status integer,
    user_attribute_score double precision
);


--
-- TOC entry 223 (class 1259 OID 16425)
-- Name: users_user_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.users_user_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- TOC entry 3748 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.users_user_id_seq OWNED BY public.users.user_id;


--
-- TOC entry 3527 (class 2604 OID 16472)
-- Name: attributes attribute_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attributes ALTER COLUMN attribute_id SET DEFAULT nextval('public.attributes_attribute_id_seq'::regclass);


--
-- TOC entry 3521 (class 2604 OID 16420)
-- Name: brands brand_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands ALTER COLUMN brand_id SET DEFAULT nextval('public.brands_brand_id_seq'::regclass);


--
-- TOC entry 3524 (class 2604 OID 16447)
-- Name: household_members household_member_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.household_members ALTER COLUMN household_member_id SET DEFAULT nextval('public.household_members_household_member_id_seq'::regclass);


--
-- TOC entry 3520 (class 2604 OID 16411)
-- Name: payment_methods paymentmethod_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_methods ALTER COLUMN paymentmethod_id SET DEFAULT nextval('public.payment_methods_paymentmethod_id_seq'::regclass);


--
-- TOC entry 3523 (class 2604 OID 16438)
-- Name: pets pet_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pets ALTER COLUMN pet_id SET DEFAULT nextval('public.pets_pet_id_seq'::regclass);


--
-- TOC entry 3526 (class 2604 OID 16465)
-- Name: purchased_products purchased_product_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchased_products ALTER COLUMN purchased_product_id SET DEFAULT nextval('public.purchased_products_purchased_product_id_seq'::regclass);


--
-- TOC entry 3525 (class 2604 OID 16456)
-- Name: purchases purchase_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchases ALTER COLUMN purchase_id SET DEFAULT nextval('public.purchases_purchase_id_seq'::regclass);


--
-- TOC entry 3519 (class 2604 OID 16402)
-- Name: supermarket_branches branch_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supermarket_branches ALTER COLUMN branch_id SET DEFAULT nextval('public.supermarket_branches_branch_id_seq'::regclass);


--
-- TOC entry 3518 (class 2604 OID 16393)
-- Name: supermarket_chains chain_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supermarket_chains ALTER COLUMN chain_id SET DEFAULT nextval('public.supermarket_chains_chain_id_seq'::regclass);


--
-- TOC entry 3522 (class 2604 OID 16429)
-- Name: users user_id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users ALTER COLUMN user_id SET DEFAULT nextval('public.users_user_id_seq'::regclass);


--
-- TOC entry 3731 (class 0 OID 16469)
-- Dependencies: 234
-- Data for Name: attributes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.attributes (attribute_id, attribute_name, attribute_description, attribute_created, attribute_modified) FROM stdin;
\.


--
-- TOC entry 3719 (class 0 OID 16417)
-- Dependencies: 222
-- Data for Name: brands; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.brands (brand_id, brand_name, brand_noname, chain_id, brand_created, brand_modified) FROM stdin;
\.


--
-- TOC entry 3732 (class 0 OID 16477)
-- Dependencies: 235
-- Data for Name: brands_attributes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.brands_attributes (brand_id, attribute_id, brand_attribute_score, brand_attribute_created, brand_attribute_modified) FROM stdin;
\.


--
-- TOC entry 3725 (class 0 OID 16444)
-- Dependencies: 228
-- Data for Name: household_members; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.household_members (household_member_id, user_id, household_member_type, household_member_sex, household_member_age) FROM stdin;
\.


--
-- TOC entry 3717 (class 0 OID 16408)
-- Dependencies: 220
-- Data for Name: payment_methods; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.payment_methods (paymentmethod_id, paymentmethod_name, paymentmetod_subtype) FROM stdin;
\.


--
-- TOC entry 3723 (class 0 OID 16435)
-- Dependencies: 226
-- Data for Name: pets; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.pets (pet_id, user_id, pet_type, pet_age, pet_status) FROM stdin;
\.


--
-- TOC entry 3729 (class 0 OID 16462)
-- Dependencies: 232
-- Data for Name: purchased_products; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.purchased_products (purchased_product_id, purchase_id, purchased_product_price, purchased_product_qty, purchased_procuct_includeddiscount, purchased_procuct_processed, purchased_product_name) FROM stdin;
\.


--
-- TOC entry 3727 (class 0 OID 16453)
-- Dependencies: 230
-- Data for Name: purchases; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.purchases (purchase_id, branch_id, user_id, purchase_sum, purchase_time, paymentmethod_id, purchase_used_discount_type, purchase_processed, purchase_created, file_name, file_path, receipt_nr, document_nr, trace_nr, cashier_number, register_number) FROM stdin;
\.


--
-- TOC entry 3715 (class 0 OID 16399)
-- Dependencies: 218
-- Data for Name: supermarket_branches; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.supermarket_branches (branch_id, chain_id, branch_chaininternal_id, branch_name, branch_street, branch_plz, branch_ort, branch_more, branch_specific, branch_created, branch_tel, branch_uid_number) FROM stdin;
\.


--
-- TOC entry 3713 (class 0 OID 16390)
-- Dependencies: 216
-- Data for Name: supermarket_chains; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.supermarket_chains (chain_id, chain_name, chain_shortname, chain_api_type, chain_api_endpoint, chain_created) FROM stdin;
\.


--
-- TOC entry 3721 (class 0 OID 16426)
-- Dependencies: 224
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users (user_id, user_name, user_email, user_created, user_password) FROM stdin;
\.


--
-- TOC entry 3733 (class 0 OID 16482)
-- Dependencies: 236
-- Data for Name: users_attributes; Type: TABLE DATA; Schema: public; Owner: -
--

COPY public.users_attributes (attribute_id, user_id, user_attribute_status, user_attribute_score) FROM stdin;
\.


--
-- TOC entry 3749 (class 0 OID 0)
-- Dependencies: 233
-- Name: attributes_attribute_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.attributes_attribute_id_seq', 1, false);


--
-- TOC entry 3750 (class 0 OID 0)
-- Dependencies: 221
-- Name: brands_brand_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.brands_brand_id_seq', 1, false);


--
-- TOC entry 3751 (class 0 OID 0)
-- Dependencies: 227
-- Name: household_members_household_member_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.household_members_household_member_id_seq', 1, false);


--
-- TOC entry 3752 (class 0 OID 0)
-- Dependencies: 219
-- Name: payment_methods_paymentmethod_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.payment_methods_paymentmethod_id_seq', 17, true);


--
-- TOC entry 3753 (class 0 OID 0)
-- Dependencies: 225
-- Name: pets_pet_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.pets_pet_id_seq', 1, false);


--
-- TOC entry 3754 (class 0 OID 0)
-- Dependencies: 231
-- Name: purchased_products_purchased_product_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.purchased_products_purchased_product_id_seq', 128, true);


--
-- TOC entry 3755 (class 0 OID 0)
-- Dependencies: 229
-- Name: purchases_purchase_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.purchases_purchase_id_seq', 92, true);


--
-- TOC entry 3756 (class 0 OID 0)
-- Dependencies: 217
-- Name: supermarket_branches_branch_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.supermarket_branches_branch_id_seq', 14, true);


--
-- TOC entry 3757 (class 0 OID 0)
-- Dependencies: 215
-- Name: supermarket_chains_chain_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.supermarket_chains_chain_id_seq', 13, true);


--
-- TOC entry 3758 (class 0 OID 0)
-- Dependencies: 223
-- Name: users_user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: -
--

SELECT pg_catalog.setval('public.users_user_id_seq', 27, true);


--
-- TOC entry 3551 (class 2606 OID 16476)
-- Name: attributes attributes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.attributes
    ADD CONSTRAINT attributes_pkey PRIMARY KEY (attribute_id);


--
-- TOC entry 3553 (class 2606 OID 16481)
-- Name: brands_attributes brands_attributes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands_attributes
    ADD CONSTRAINT brands_attributes_pkey PRIMARY KEY (brand_id, attribute_id);


--
-- TOC entry 3535 (class 2606 OID 16424)
-- Name: brands brands_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_pkey PRIMARY KEY (brand_id);


--
-- TOC entry 3545 (class 2606 OID 16451)
-- Name: household_members household_members_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.household_members
    ADD CONSTRAINT household_members_pkey PRIMARY KEY (household_member_id);


--
-- TOC entry 3533 (class 2606 OID 16415)
-- Name: payment_methods payment_methods_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_pkey PRIMARY KEY (paymentmethod_id);


--
-- TOC entry 3543 (class 2606 OID 16442)
-- Name: pets pets_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_pkey PRIMARY KEY (pet_id);


--
-- TOC entry 3549 (class 2606 OID 16467)
-- Name: purchased_products purchased_products_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchased_products
    ADD CONSTRAINT purchased_products_pkey PRIMARY KEY (purchased_product_id);


--
-- TOC entry 3547 (class 2606 OID 16460)
-- Name: purchases purchases_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_pkey PRIMARY KEY (purchase_id);


--
-- TOC entry 3531 (class 2606 OID 16406)
-- Name: supermarket_branches supermarket_branches_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supermarket_branches
    ADD CONSTRAINT supermarket_branches_pkey PRIMARY KEY (branch_id);


--
-- TOC entry 3529 (class 2606 OID 16397)
-- Name: supermarket_chains supermarket_chains_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supermarket_chains
    ADD CONSTRAINT supermarket_chains_pkey PRIMARY KEY (chain_id);


--
-- TOC entry 3537 (class 2606 OID 16555)
-- Name: users unique_email; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_email UNIQUE (user_email);


--
-- TOC entry 3539 (class 2606 OID 16553)
-- Name: users unique_username; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT unique_username UNIQUE (user_name);


--
-- TOC entry 3555 (class 2606 OID 16486)
-- Name: users_attributes users_attributes_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_attributes
    ADD CONSTRAINT users_attributes_pkey PRIMARY KEY (attribute_id, user_id);


--
-- TOC entry 3541 (class 2606 OID 16433)
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (user_id);


--
-- TOC entry 3565 (class 2606 OID 16537)
-- Name: brands_attributes brands_attributes_attribute_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands_attributes
    ADD CONSTRAINT brands_attributes_attribute_id_fkey FOREIGN KEY (attribute_id) REFERENCES public.attributes(attribute_id);


--
-- TOC entry 3566 (class 2606 OID 16532)
-- Name: brands_attributes brands_attributes_brand_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands_attributes
    ADD CONSTRAINT brands_attributes_brand_id_fkey FOREIGN KEY (brand_id) REFERENCES public.brands(brand_id);


--
-- TOC entry 3558 (class 2606 OID 16497)
-- Name: brands brands_chain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.brands
    ADD CONSTRAINT brands_chain_id_fkey FOREIGN KEY (chain_id) REFERENCES public.supermarket_chains(chain_id);


--
-- TOC entry 3560 (class 2606 OID 16507)
-- Name: household_members household_members_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.household_members
    ADD CONSTRAINT household_members_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3557 (class 2606 OID 16492)
-- Name: payment_methods payment_methods_paymentmetod_subtype_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.payment_methods
    ADD CONSTRAINT payment_methods_paymentmetod_subtype_fkey FOREIGN KEY (paymentmetod_subtype) REFERENCES public.payment_methods(paymentmethod_id);


--
-- TOC entry 3559 (class 2606 OID 16502)
-- Name: pets pets_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.pets
    ADD CONSTRAINT pets_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3564 (class 2606 OID 16527)
-- Name: purchased_products purchased_products_purchase_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchased_products
    ADD CONSTRAINT purchased_products_purchase_id_fkey FOREIGN KEY (purchase_id) REFERENCES public.purchases(purchase_id);


--
-- TOC entry 3561 (class 2606 OID 16517)
-- Name: purchases purchases_branch_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_branch_id_fkey FOREIGN KEY (branch_id) REFERENCES public.supermarket_branches(branch_id);


--
-- TOC entry 3562 (class 2606 OID 16522)
-- Name: purchases purchases_paymentmethod_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_paymentmethod_id_fkey FOREIGN KEY (paymentmethod_id) REFERENCES public.payment_methods(paymentmethod_id);


--
-- TOC entry 3563 (class 2606 OID 16512)
-- Name: purchases purchases_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.purchases
    ADD CONSTRAINT purchases_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


--
-- TOC entry 3556 (class 2606 OID 16487)
-- Name: supermarket_branches supermarket_branches_chain_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.supermarket_branches
    ADD CONSTRAINT supermarket_branches_chain_id_fkey FOREIGN KEY (chain_id) REFERENCES public.supermarket_chains(chain_id);


--
-- TOC entry 3567 (class 2606 OID 16542)
-- Name: users_attributes users_attributes_attribute_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_attributes
    ADD CONSTRAINT users_attributes_attribute_id_fkey FOREIGN KEY (attribute_id) REFERENCES public.attributes(attribute_id);


--
-- TOC entry 3568 (class 2606 OID 16547)
-- Name: users_attributes users_attributes_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.users_attributes
    ADD CONSTRAINT users_attributes_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(user_id);


-- Completed on 2024-06-25 15:51:12 CEST

--
-- PostgreSQL database dump complete
--

