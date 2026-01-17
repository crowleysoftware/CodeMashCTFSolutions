# Dashboard

Grafana calls Prometheus to run DB queries. Since you can't edit the dashboard, call Prometheus in your API tester of choice (e.g., Bruno).

1. Use browser Dev Tools to find the format of the Prometheus API call.
2. List all tables in the Postgres DB: `SELECT table_name FROM information_schema.tables`
3. Query the `flag` table.
