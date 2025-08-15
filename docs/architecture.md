# Architecture & Schema

## Overview
A simple Flask MVC-ish structure:
- `app.py` registers routes and blueprints (auth, shipments)
- `models.py` contains SQLAlchemy models (`User`, `Shipment`)
- `auth.py` handles login/logout routes
- `shipment.py` handles CRUD, pagination, filtering
- `extensions.py` for handling circular imports
- `templates/` Jinja2 HTML templates (Bootstrap 5 via CDN)
- `static/` optional custom CSS

## Database (SQLite)
Tables:
- `User(id, username, password_hash)`
- `Shipment(id, name, status, is_fragile, distance_km, service_level, estimated_days, created_at)`

### Field Notes
- `status` ENUM (as string): `Pending`, `In-Transit`, `Delivered`
- `is_fragile` BOOLEAN
- `service_level` ENUM (as string): `Economy`, `Standard`, `Express`
- `estimated_days` (CALCULATED): derived from `distance_km` and `service_level`.
  Formula:
  ```
  daily_km = {Economy: 200, Standard: 300, Express: 450}
  estimated_days = ceil(distance_km / daily_km)
  ```

## Pagination & Filtering
- Pagination via `?page=<n>` (default 1), page size 5
- Filter by `status` and simple search by `name` (optional param `q`)