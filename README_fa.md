# TAPRepo - مخزن هدف و پارامتر حمله

یک API شخصی و ایمن برای تست‌نفوذگران. ساخته‌شده با Django REST Framework،
این ابزار اهداف آسیب‌پذیر، پارامترهای مشکوک و آسیب‌پذیری‌های کشف‌شده در
تست‌های امنیتی را ذخیره و دسته‌بندی می‌کند. TAPRepo مانند یک «مغز دوم»
ساختاریافته و قابل جستجو عمل می‌کند و یافته‌های پراکنده را به هوش قابل
استفادهٔ مجدد تبدیل می‌کند.

## 🎯 هدف

در تست‌های نفوذ مکرر وب، بارها با پارامترهای آسیب‌پذیر مشابهی مانند
`id`، `user_id` و `redirect` در اهداف مختلف مواجه می‌شدم. TAPRepo
این مشکل را با این قابلیت‌ها حل می‌کند:

- ثبت اهداف به همراه جزئیات زیرساخت (زیردامنه‌ها، IPها، CIDRها، ASNها)
- ذخیره‌سازی پارامترهای مشکوک بر اساس نوع حمله (SQLi, XSS, IDOR و غیره)
- الصاق رکوردهای دقیق آسیب‌پذیری به هر هدف
- پرس‌وجوی بعدی بر اساس سایت، نوع حمله یا نام پارامتر برای تست‌های
  سریع‌تر و ساختاریافته‌تر

## ⚙️ فناوری‌ها

- **بک‌اند:** Python 3.x, Django 4.x, Django REST Framework
- **احراز هویت:** JWT با استفاده از `djangorestframework-simplejwt`
  به همراه چرخش توکن و لیست سیاه (Blacklist)
- **محدودیت نرخ:** کلاس‌های Throttling توکار DRF (قابل تنظیم برای هر View)
- **تنظیمات:** `python-decouple` — اطلاعات محرمانه در فایل `.env`
  ذخیره می‌شوند و هرگز در کد قرار نمی‌گیرند
- **پایگاه داده:** SQLite (محیط توسعه) / آماده برای PostgreSQL
- **مستندات API:** DRF Browsable API

## 🔒 ویژگی‌های امنیتی

- **توکن‌های JWT** پس از **۳۰ دقیقه** منقضی می‌شوند؛ توکن‌های تازه‌سازی
  پس از **۱ روز** با چرخش خودکار و قرارگیری در لیست سیاه.
- **همهٔ endpointها** نیازمند احراز هویت (`IsAuthenticated`) هستند.
- **endpoint دریافت توکن** برای جلوگیری از حملات Brute-force دارای
  محدودیت نرخ است.
- **کلیدهای محرمانه و اطلاعات حساس** از طریق متغیرهای محیطی (`.env`)
  و کتابخانهٔ `python-decouple` مدیریت می‌شوند — هرگز در کنترل نسخه
  ذخیره نمی‌شوند.
- **Throttling** برای کنترل دقیق نرخ درخواست‌ها روی هر ViewSet قابل
  اعمال است.

## 📦 نصب و راه‌اندازی

```bash
git clone https://github.com/RezaChabok/TAPRepo.git
cd TAPRepo
python -m venv venv
source venv/bin/activate      # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### متغیرهای محیطی

یک فایل `.env` در ریشهٔ پروژه بسازید (مطابق نمونهٔ `.env.example`):

```ini
SECRET_KEY='کلید-محرمانه-جنگو-شما'
DJANGO_DEBUG=False
ALLOWED_HOSTS='127.0.0.1,localhost'
```

سپس migrationها را اعمال کنید و یک ابرکاربر بسازید:

```bash
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 🔐 احراز هویت

TAPRepo فقط از JWT استفاده می‌کند. برای دریافت توکن دسترسی (Access Token):

```
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```

پاسخ شامل دو توکن خواهد بود:

```json
{
    "access": "eyJ...",
    "refresh": "eyJ..."
}
```

توکن دسترسی را در تمام درخواست‌های بعدی همراه کنید:

```
Authorization: Bearer <access_token>
```

زمانی که توکن دسترسی منقضی شد (۳۰ دقیقه)، از توکن تازه‌سازی استفاده کنید:

```
POST /api/token/refresh/
{
    "refresh": "eyJ..."
}
```

توکن تازه‌سازی قدیمی به طور خودکار **لیست سیاه** می‌شود و یک جفت
توکن جدید صادر می‌گردد.

## 📡 نمای کلی API

### اهداف (Targets)

| متد | مسیر | توضیح |
|--------|----------|-------------|
| GET | `/targets/` | لیست تمام اهداف (فیلتر با `address`) |
| POST | `/targets/` | ایجاد یک هدف به همراه زیردامنه‌ها، IPها، CIDRها، ASNها و آسیب‌پذیری‌ها |
| PUT | `/targets/update_target/` | افزودن زیردامنه، IP و... به یک هدف موجود |
| GET | `/targets/all_subdomains/` | لیست تمام زیردامنه‌ها در تمام اهداف |

**نمونه ایجاد هدف:**

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

### پارامترها (Parameters)

| متد | مسیر | توضیح |
|--------|----------|-------------|
| GET | `/parameters/` | لیست پارامترها (فیلتر با `site`، `type`، `top`) |
| POST | `/parameters/` | ذخیره یک پارامتر تکی یا گروهی (آرایه `params`) |

**نمونه‌های پرس‌وجو:**

```
GET /parameters/?type=SQLi
GET /parameters/?site=example.com&type=XSS
GET /parameters/?top=10
```

**نمونه ایجاد گروهی:**

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

## 🖥️ ابزارهای خط فرمان (CLI)

دو اسکریپت پایتون مستقل برای استفادهٔ سریع در ترمینال هنگام تست نفوذ
ارائه شده است.

### راه‌اندازی

اسکریپت‌ها با استفاده از حساب ابرکاربر جنگو احراز هویت می‌شوند.
می‌توانید اطلاعات کاربری را به‌عنوان متغیر محیطی تنظیم کنید
(یا از مقادیر پیش‌فرض استفاده کنید):

```bash
export TAPREPO_USER="your_user"
export TAPREPO_PASS="your_password"
export TAPREPO_URL="http://127.0.0.1:8000"   # اختیاری، پیش‌فرض همین است
```

### `parameters.py`

```bash
# دریافت تمام پارامترها
python parameters.py --get --all

# فیلتر بر اساس سایت و نوع
python parameters.py --get --site example.com --type SQLi

# دریافت ۱۰ پارامتر پرتکرار
python parameters.py --get --top 10

# افزودن یک پارامتر تکی
python parameters.py --add --name user_id --type IDOR --site example.com

# افزودن چندین پارامتر از یک فایل (هر خط یک پارامتر)
python parameters.py --add --read params.txt --type XSS --site example.com
```

### `targets.py`

```bash
# دریافت تمام زیردامنه‌ها
python targets.py --all_subdomains

# دریافت جزئیات کامل یک هدف
python targets.py --address example.com

# افزودن یک هدف جدید با زیردامنه‌ها و IPها
python targets.py --add --address example.com --name "Example Corp" \
  --sub '["dev.example.com","admin.example.com"]' \
  --ip '["192.168.1.1"]'
```

## 🧪 نحوهٔ استفاده در فرایند تست نفوذ

۱. **شناسایی:** یک endpoint جذاب مانند `/api/user?id=123` در
   `example.com` پیدا می‌کنم.
۲. **ثبت:** به `/parameters/` درخواست POST می‌زنم با
   `site=example.com`، `type=IDOR` و `params=["id"]`.
۳. **بازیابی:** هفته‌ها بعد، وقتی API مشابهی را تست می‌کنم،
   `GET /parameters/?type=IDOR` می‌گیرم و بلافاصله یک لیست
   مرتب از نام پارامترها برای Fuzzing دارم
   (مثل `id`، `user_id`، `order_id`).
۴. **مدیریت اهداف:** تمام زیردامنه‌ها، IPها، CIDRها، ASNها و
   آسیب‌پذیری‌های یک هدف را به صورت یکجا از طریق
   `/targets/` نگهداری می‌کنم.

## 👤 نویسنده

رضا چابک – [گیت‌هاب](https://github.com/RezaChabok)

## 📄 مجوز

[MIT](https://choosealicense.com/licenses/mit/)
