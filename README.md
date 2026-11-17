# DDA Scanner — Automated Telegram Stream Monitoring Engine

An automated monitoring and parsing tool capable of processing real-time message streams across 500+ Telegram groups concurrently.

## Key Features
* **Concurrent Stream Parsing:** High-throughput monitoring of multiple channels and groups simultaneously using Telethon.
* **Filtering Engine:** Fast keyword matching and hash-based deduplication backed by PostgreSQL.
* **Outreach Management:** Administrative web interface for configuring filters and scheduling automated outreach tasks.

## Tech Stack
* **Language:** Python 3.11+
* **Core Libraries:** Telethon, Asyncio
* **Database:** PostgreSQL
