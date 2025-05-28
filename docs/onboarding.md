# Onboarding

Run `make dev` to set up a development environment.

1. Copy `.env.example` to `.env`:

   ```bash
   cp .env.example .env
   ```

2. Edit `.env` and provide credentials for any services you wish to use. The
   file lists all variables used throughout the project such as API tokens and
   usernames for DataForSEO.

3. Install Python dependencies and run the tests:

   ```bash
   pip install -r requirements.txt
   pytest -q
   ```

Secrets used in production can be sourced from Vault or another secrets manager
instead of storing them directly in `.env`.
