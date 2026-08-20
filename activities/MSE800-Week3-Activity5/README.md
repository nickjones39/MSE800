# MSE800 — Week 3, Activity 5: Money Exchange Project with Database

A PostgreSQL database for a **money exchange system**, built in object-oriented
Python. The system lets an exchange business manage its **customers**,
**currencies**, **exchange rates**, and **currency exchange transactions**.

The project follows the same architecture as the Week 3, Activity 4 (university
enrolment) project: an ER diagram drawn in TikZ/LaTeX, a relational schema in
PostgreSQL, and an object-oriented Python layer (models, repositories, and a
service) that reads and writes the database.

---

## 1. ER diagram

The conceptual model is drawn in Chen notation in [`er_diagram.tex`](docs/er_diagram.tex)
(compiled PDF: `docs/er_diagram.pdf`). It contains **four entities** and **three
relationships**, which form the chain an exchange follows:

```
Customer ──Makes──▶ Transaction ──Involves──▶ Currency ──Quotes──▶ ExchangeRate
```

| Relationship | Entities | Cardinality | Meaning |
|---|---|---|---|
| **Makes** | Customer → Transaction | 1 : N | One customer makes many transactions; each transaction belongs to one customer. |
| **Involves** | Currency → Transaction | 1 : N | A currency is the base or quote of many transactions; each transaction has one base and one quote currency. |
| **Quotes** | Currency → ExchangeRate | 1 : N | A currency is the base or quote of many rates; each rate quotes one base and one quote currency. |

---

## 2. Tables — how many, and why each is necessary

The relational schema contains **four tables**, one per entity. This is the
minimum set that satisfies the project scope (customers, currencies, exchange
rates, and transactions) without redundancy.

### 2.1 `customer`

| Column | Type | Constraint |
|---|---|---|
| `customer_id` | `VARCHAR(10)` | PRIMARY KEY |
| `first_name` | `VARCHAR(50)` | NOT NULL |
| `last_name` | `VARCHAR(50)` | NOT NULL |
| `email` | `VARCHAR(120)` | NOT NULL, UNIQUE |
| `phone` | `VARCHAR(30)` | |

**Why it is necessary.** A money exchange business cannot record a transaction
without knowing *who* is exchanging money. This table stores the identity and
contact details of each customer, and every transaction references it (the
one-to-many "Makes" relationship).

### 2.2 `currency`

| Column | Type | Constraint |
|---|---|---|
| `currency_code` | `VARCHAR(3)` | PRIMARY KEY |
| `currency_name` | `VARCHAR(100)` | NOT NULL |
| `symbol` | `VARCHAR(5)` | NOT NULL |

**Why it is necessary.** Currencies are the "goods" being traded. Centralising
them in one table (with a three-letter ISO-style code such as `NZD` as the
natural primary key) avoids repeating a currency's name and symbol on every
rate and transaction, and guarantees consistency — a rate or transaction can
only reference a currency that actually exists.

### 2.3 `exchange_rate`

| Column | Type | Constraint |
|---|---|---|
| `rate_id` | `SERIAL` | PRIMARY KEY |
| `base_currency` | `VARCHAR(3)` | NOT NULL, FK → `currency` |
| `quote_currency` | `VARCHAR(3)` | NOT NULL, FK → `currency` |
| `rate` | `NUMERIC(12,6)` | NOT NULL |
| `effective_date` | `DATE` | NOT NULL |

**Why it is necessary.** A rate is a value *between two currencies* (for
example `NZD → USD = 0.61`), so it must live in its own table rather than on
`currency`. Keeping rates separate also records them **over time**: the same
pair can have a new rate each `effective_date`, and the business can look up the
latest rate for any pair. `base_currency` and `quote_currency` are two foreign
keys to `currency` (the "Quotes" relationship), and the pair plus date are made
unique so a rate is never entered twice.

### 2.4 `exchange_transaction`

| Column | Type | Constraint |
|---|---|---|
| `transaction_id` | `SERIAL` | PRIMARY KEY |
| `customer_id` | `VARCHAR(10)` | NOT NULL, FK → `customer` |
| `base_currency` | `VARCHAR(3)` | NOT NULL, FK → `currency` |
| `quote_currency` | `VARCHAR(3)` | NOT NULL, FK → `currency` |
| `amount_base` | `NUMERIC(14,2)` | NOT NULL |
| `amount_quote` | `NUMERIC(14,2)` | NOT NULL |
| `rate_used` | `NUMERIC(12,6)` | NOT NULL |
| `transaction_date` | `DATE` | NOT NULL |

**Why it is necessary.** The transaction is the core event of the system — it
records *who* exchanged *how much* of one currency into another, *when*, and at
*what rate*. It is a separate table because a customer may perform many
transactions and a transaction combines several facts (customer + two
currencies + amounts + rate). `rate_used` stores a **snapshot** of the exchange
rate at the moment of the trade rather than a foreign key to `exchange_rate`,
so historical transactions keep the exact rate even after the quoted rate is
updated.

> The table is named `exchange_transaction` (not `transaction`) because
> `transaction` is a reserved SQL keyword.

---

## 3. Sample data

The seeder (`src/seeder.py`) loads a small but representative dataset:

| Table | Rows | Contents |
|---|---|---|
| `currency` | 5 | NZD, USD, EUR, GBP, AUD |
| `customer` | 4 | Alice, Bob, Carol, David |
| `exchange_rate` | 10 | five currency pairs, each quoted in both directions |
| `exchange_transaction` | 5 | several trades (Alice exchanges twice, exercising the 1 : N relationship) |

---

## 4. Report queries

Two analytical queries (`sql/queries.sql`, exposed via `--report`):

1. **Total value exchanged by each customer** — joins `customer` to
   `exchange_transaction` and sums `amount_quote`.
2. **Latest exchange rate for each currency pair** — uses
   `DISTINCT ON (base_currency, quote_currency)` to pick the most recent rate.

---

## 5. Object-oriented architecture

The Python layer mirrors the ER diagram and follows the repository pattern:

```
src/
├── models.py        # dataclasses: Customer, Currency, ExchangeRate, Transaction
├── repositories.py  # one repository per entity (generic INSERT in the base class)
├── services.py      # ExchangeService — business rules (record_exchange, add_customer)
├── schema.py        # DDL + SchemaManager (ensure / reset)
├── seeder.py        # sample data
├── queries.py       # report queries
├── cli.py           # interactive menu
├── config.py        # .env / DATABASE_URL loading
└── db.py            # connection context manager
```

- **Models** are plain dataclasses whose field order matches the `INSERT`
  column order, so a repository can insert a whole object with
  `dataclasses.astuple`.
- **Repositories** own all SQL for a single table (a shared `Repository` base
  class provides the generic insert logic).
- **Services** coordinate repositories and enforce business rules. For example,
  `ExchangeService.record_exchange(...)` validates the customer and currencies,
  looks up the latest rate, computes the quote amount, and inserts the
  transaction — raising a friendly `ValueError` on any bad input.

---

## 6. Running the project

### Prerequisites

- Python 3.12 and PostgreSQL (the connection string points at a Neon database).
- Install dependencies: `pip install -r requirements.txt`

### Configuration

Copy `.env.example` to `.env` and set the Neon connection string:

```
DATABASE_URL=postgresql://USER:PASSWORD@HOST/DATABASE?sslmode=require
```

### Commands

```bash
python main.py             # interactive Money Exchange menu
python main.py --setup     # drop, recreate and seed the database, then exit
python main.py --report    # print the two report queries and exit
```

The interactive menu offers: add a customer, view customers, view exchange
rates, record an exchange, view transactions, run the report queries, and reset
the database.

---

## 7. Project structure

```
MSE800-Week3-Activity5/
├── main.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── docs/
│   ├── er_diagram.tex    # Chen-notation ER diagram (TikZ)
│   └── er_diagram.pdf    # compiled diagram
├── sql/
│   └── queries.sql       # the two report queries
└── src/
    ├── __init__.py
    ├── models.py
    ├── repositories.py
    ├── services.py
    ├── schema.py
    ├── seeder.py
    ├── queries.py
    ├── cli.py
    ├── config.py
    └── db.py
```

---

## Author

Nick Jones
