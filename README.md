# TAPRepo - Target & Attack-Parameter Repository

**📄 [نسخهٔ فارسی (Persian)](README_fa.md)**


A secure, personal API toolkit for penetration testers. Built with Django REST
Framework, TAPRepo stores and categorizes vulnerable targets, suspicious
parameters, and discovered vulnerabilities during web application security
tests. It acts as your structured, queryable "second brain" — turning ad-hoc
findings into reusable intelligence.

## 🎯 Purpose

During repeated web pentests, I kept rediscovering the same vulnerable
parameters (e.g., `id`, `user_id`, `redirect`) across different targets.
TAPRepo solves this by allowing me to:

- Log targets with full infrastructure details (subdomains, IPs, CIDRs, ASNs)
- Store suspicious parameters categorized by attack type (SQLi, XSS, IDOR, etc.)
- Attach detailed vulnerability records to each target
- Later query by site, type, or parameter name for faster, more structured
  testing

## ⚙️ Tech Stack

- **Backend:** Python 3.x, Django 4.x, Django REST Framework
- **Authentication:** JWT via `djangorestframework-simplejwt` with access/refresh
  token rotation and blacklisting
- **Rate Limiting:** DRF throttling classes (customizable per view)
- **Configuration:** `python-decouple` — secrets stored in `.env`, never in code
- **Database:** SQLite (dev) / PostgreSQL-ready
- **API Docs:** DRF Browsable API

## 🔒 Security Features

- **JWT access tokens** expire after **30 minutes**; refresh tokens after
  **1 day** with automatic rotation and blacklisting
- **All endpoints** require authentication (`IsAuthenticated`)
- **Token endpoint** is rate-limited to prevent brute-force attacks
- **Secret keys and credentials** are managed via environment variables
  (`.env`) using `python-decouple` — never committed to version control
- **Throttling** can be applied per-viewset for fine-grained rate control

## 📦 Installation & Setup

```bash
git clone https://github.com/RezaChabok/TAPRepo.git
cd TAPRepo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Environment Variables

Create a `.env` file in the project root (see `.env.example`):

```ini
SECRET_KEY='your-django-secret-key-here'
DJANGO_DEBUG=False
ALLOWED_HOSTS='127.0.0.1,localhost'
```

Then apply migrations and create a superuser:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🔐 Authentication

TAPRepo uses JWT exclusively. Obtain an access token:

```
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

The response contains two tokens:

```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

Include the access token in all subsequent requests:

```
Authorization: Bearer <access_token>
```

When the access token expires (30 min), use the refresh token:

```
POST /api/token/refresh/
{
    "refresh": "eyJ..."
}
```

The old refresh token is automatically **blacklisted** and a new pair is
issued.

## 📡 API Overview

### Targets

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/targets/` | List all targets (filter by `address`) |
| POST | `/targets/` | Create a target with subdomains, IPs, CIDRs, ASNs, vulnerabilities |
| PUT | `/targets/update_target/` | Add subdomains, IPs, etc. to an existing target |
| GET | `/targets/all_subdomains/` | List all subdomains across all targets |

**Example Create Target:**

```json
POST /targets/
{
  "address": "example.com",
  "name": "Example Corp",
  "behind_cdn": false,
  "subdomains": ["dev.example.com", "admin.example.com"],
  "ips": ["192.168.1.1"],
  "cidrs": ["192.168.1.0/24"],
  "asns": ["AS15169"],
  "vulnerabilities": [
    {
      "name": "SQLi in /login",
      "attack_vector": "SQL Injection",
      "description": "Blind SQL injection in username parameter",
      "cvss": "8.8",
      "write_up": "Details...",
      "report": "https://example.com/report"
    }
  ]
}
```

### Parameters

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/parameters/` | List parameters (filter by `site`, `type`, `top`) |
| POST | `/parameters/` | Store a single parameter or a batch (`params` array) |

**Query Examples:**

```
GET /parameters/?type=SQLi
GET /parameters/?site=example.com&type=XSS
GET /parameters/?top=10
```

**Example Create Batch:**

```json
POST /parameters/
{
  "site": "example.com",
  "type": "IDOR",
  "params": [
    {"name": "user_id"},
    {"name": "order_id"}
  ]
}
```

## 🖥 CLI Tools

Two standalone Python scripts are included for rapid terminal use during
pentests.

### Setup

The scripts authenticate using a Django superuser account. Set your
credentials as environment variables (or rely on the defaults):

```bash
export TAPREPO_USER="your_user"
export TAPREPO_PASS="your_password"
export TAPREPO_URL="http://127.0.0.1:8000"   # optional, this is the default
```

### `parameters.py`

```bash
# Get all parameters
python parameters.py --get --all

# Filter by site and type
python parameters.py --get --site example.com --type SQLi

# Get top 10 most common parameters
python parameters.py --get --top 10

# Add a single parameter
python parameters.py --add --name user_id --type IDOR --site example.com

# Add multiple parameters from a file (one per line)
python parameters.py --add --read params.txt --type XSS --site example.com
```

### `targets.py`

```bash
# Get all subdomains
python targets.py --all_subdomains

# Get full details of a target
python targets.py --address example.com

# Add a new target with subdomains and IPs
python targets.py --add --address example.com --name "Example Corp" \
  --sub '["dev.example.com","admin.example.com"]' \
  --ip '["192.168.1.1"]'
```

## 🧪 How I Use This In A Pentest Workflow

1. **Recon:** I find an interesting endpoint like `/api/user?id=123` on
   `example.com`.
2. **Log:** I POST to `/parameters/` with `site=example.com`, `type=IDOR`,
   and `params=["id"]`.
3. **Retrieve:** Weeks later, when testing another API, I `GET
   /parameters/?type=IDOR` and instantly have a curated list of parameter
   names to fuzz (`id`, `user_id`, `order_id`).
4. **Manage targets:** I keep all subdomains, IPs, CIDRs, ASNs, and
   vulnerabilities of a target in one place via `/targets/`.

## 👤 Author

Reza Chabok – [GitHub](https://github.com/RezaChabok)

## 📄 License

[MIT](https://choosealicense.com/licenses/mit/)
