---
name: genpark-sales-agent
description: Autonomous outbound B2B sales development representative.
---
# genpark-sales-agent

An open-source GenPark alternative to anlah AI: CanSell.

A Python-based CLI agent that ingests a lead list, generates personalized cold emails, tracks responses, and automatically queues follow-ups using a local SQLite database and your own SMTP server. Zero per-seat SaaS fees.

## MCP runtime requirements

The standard-library-only policy applies to direct `client.py` use. Running `mcp_server.py` requires Python 3.10+ and the official `mcp` SDK (`mcp>=1.0.0,<2`) from `requirements.txt`. Install it into your chosen environment from the repository checkout:

```bash
python -m pip install -r requirements.txt
```

Configure the MCP client with that environment's absolute Python executable path and the absolute path to `mcp_server.py`. The client launches a local STDIO process; a GitHub URL is not a remote MCP endpoint.
