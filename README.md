# TAPRepo - Target & Attack-Parameter Repository

A Django REST Framework API to store, categorize, and retrieve vulnerable
targets and their suspicious parameters discovered during penetration tests.

## 🎯 Purpose
During web application pentesting, I kept rediscovering the same vulnerable
parameters across different targets. TAPRepo is my personal "second brain":
I log targets, their suspicious parameters, and the vulnerability type
(e.g., SQLi, XSS), then quickly retrieve them for faster, more structured
testing.

## ⚙️ Tech Stack
- **Backend:** Python 3.x, Django 4.x, Django REST Framework
- **Authentication:** JWT (Simple JWT)
- **Database:** SQLite (default)
- **API Docs:** DRF Browsable API

## 📦 Installation & Setup
```bash
git clone https://github.com/RezaChabok/TAPRepo.git
cd TAPRepo
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
python manage.py migrate
python manage.py runserver
```

## 🔐 Authentication
TAPRepo uses JWT (`djangorestframework-simplejwt`). Obtain a token:
```
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```
Include the token in requests:
```
Authorization: Bearer <access_token>
```
Refresh the token via:
```
POST /api/token/refresh/
```

## 📡 API Overview

### Targets
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/targets/` | List all targets (filter via query params) |
| POST   | `/targets/` | Create a target with subdomains, IPs, CIDRs, ASNs, vulnerabilities |
| PUT    | `/targets/update_target/` | Add subdomains, IPs, etc. to an existing target |
| GET    | `/targets/all_subdomains/` | List all subdomains across all targets |

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
      "report": "Full report link..."
    }
  ]
}
```

### Parameters
| Method | Endpoint | Description |
|--------|----------|-------------|
| GET    | `/parameters/` | List all parameters (filter by `site`, `type`, `top`) |
| POST   | `/parameters/` | Store a single parameter or a batch (`params` array) |

**Query Examples:**
```
GET /parameters/?type=SQLi
GET /parameters/?site=example.com&type=XSS
GET /parameters/?top=10
```

**Example Create Batch Parameters:**
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
## 🖥️ CLI Tools

For faster interaction from the terminal during pentests, two Python
scripts are provided:

**Setup:** Export your JWT token as an environment variable:
```bash
export TAPREPO_TOKEN="<your_access_token>"
```

### `parameters.py`
Manage suspicious parameters directly from the command line.

```bash
# Get all parameters
python parameters.py --get --all

# Get parameters for a specific site and type
python parameters.py --get --site example.com --type SQLi

# Get top 10 most common parameters
python parameters.py --get --top 10

# Add a single parameter
python parameters.py --add --name user_id --type IDOR --site example.com

# Add multiple parameters from a file (one per line)
python parameters.py --add --read params.txt --type XSS --site example.com
```
## 🧪 How I Use This In A Pentest Workflow
1. **Recon:** I find an endpoint like `/api/user?id=123` on `example.com`.
2. **Log:** I POST to `/parameters/` with site=`example.com`, type=`IDOR`,
   and params=`["id"]`.
3. **Retrieve:** Weeks later, when testing another API, I `GET
   /parameters/?type=IDOR` and instantly get a curated list of parameter
   names to fuzz (like `id`, `user_id`, `order_id`).
4. **Manage targets:** I keep all subdomains, IPs, and vulnerabilities of a
   target in one place via `/targets/`.


## 👤 Author
Reza Chabok – [GitHub](https://github.com/RezaChabok)

## 📄 License
[MIT](https://choosealicense.com/licenses/mit/)
