# Neshan MCP Server

سرور [MCP](https://modelcontextprotocol.io) برای پلتفرم نقشه نشان. وب‌سرویس‌های نشان (جستجو، جئوکدینگ، مسیریابی خودرو/پیاده/تاریخی/معمول، ایزوکرون، ماتریس فاصله، TSP، نقشه استاتیک، نقشه استاتیک با کمان و map matching) را به‌صورت ابزارهای MCP در اختیار محیط‌های هوش مصنوعی (Claude Desktop، Cursor و …) قرار می‌دهد.

ساختار لایه‌ای با مدل کاری `tool → handler → service → http`، گروه‌بندی‌شده بر اساس دامنه (`search` / `routing` / `map`).

کلید API را **کلاینت** فراهم می‌کند: در حالت HTTP در هدر هر درخواست (`Neshan-Api-Key`) فرستاده می‌شود؛ در حالت stdio به‌عنوان fallback از env سرور خوانده می‌شود.

## معماری

```
src/neshan_mcp/
├── index.py             # entry point برای stdio
├── indexHttp.py         # entry point برای HTTP
├── createServer.py      # factory ساخت FastMCP + ثبت ابزارها + بستن client
├── appConfig.py         # تنظیمات runtime + lookup کلید از env
├── constants.py         # اندپوینت‌ها، نسخه‌ها، نام هدرها، نگاشت env کلید
├── auth/
│   └── apiKeyResolver.py   # resolve کلید: هدر کلاینت → fallback به env
├── handlers/            # validate (schema) → فراخوان service → نرمال‌سازی خطا
│   ├── searchHandler.py
│   ├── routingHandler.py
│   ├── mapHandler.py
│   └── shared/responseTrimmer.py
├── schemas/             # مدل‌های pydantic برای اعتبارسنجی ورودی (per-domain)
│   ├── search/  (searchSchema.py, common.py)
│   ├── routing/ (routingSchema.py, common.py)
│   ├── map/     (mapSchema.py)
│   └── shared/  (validators.py)
├── services/            # wrapper خام API (per-domain) + کلاینت پایه
│   ├── base/    (neshanClient.py)
│   ├── search/  (searchService.py, types.py)
│   ├── routing/ (routingService.py, types.py)
│   └── map/     (mapService.py, types.py)
├── tools/               # تعریف نازک ابزار MCP که به handler delegate می‌کند
│   ├── searchTools.py
│   ├── routingTools.py
│   └── mapTools.py
├── types/               # مدل‌های مقدار مشترک (Coordinate و …)
├── utils/               # apiErrorHandler, logger, coords
└── apps/                # (placeholder) لایه‌ی UI تعاملی؛ فعلاً پیاده‌سازی نشده
```

مسئولیت هر لایه:
- **tools**: رابط MCP (امضای تمیز + docstring که مدل می‌بیند)؛ فقط handler را صدا می‌زند.
- **handlers**: ورودی را با schema اعتبارسنجی می‌کند، service را صدا می‌زند، و خطاها را به فرمت یکدست تبدیل می‌کند (با decoratorِ `handle_api_errors`).
- **services**: نگاشت پارامتر به اندپوینت و فراخوان API؛ هیچ دانشی از MCP ندارد.
- **services/base**: تنها نقطه‌ای که با شبکه و کلید سروکار دارد (retry، تزریق کلید، نرمال‌سازی خطا).

> نکته: نام فایل‌ها به‌صورت camelCase نگه داشته شده تا با چیدمان مرجع هم‌خوان باشد (برخلاف قرارداد snake_case معمول پایتون). این یک انتخاب آگاهانه برای هم‌خوانی ساختاری است.

افزودن سرویس جدید در یک دامنه: متدش را به `<domain>Service` و `<domain>Schema` و `<domain>Handler` و `<domain>Tools` اضافه کن. افزودن دامنه‌ی جدید: یک پوشه در هر چهار لایه بساز و آن را در `tools/__init__.py:register_all` ثبت کن.

## ابزارها

| ابزار | دامنه | اندپوینت نشان | توضیح |
|---|---|---|---|
| `neshan_search` | search | `/v1/search` | جستجوی مکان |
| `neshan_reverse_geocode` | search | `/v5/reverse` | تبدیل مختصات به آدرس |
| `neshan_geocode` | search | `/geocoding/v1/` | تبدیل آدرس به مختصات |
| `neshan_geocode_plus` | search | `/geocoding/v1/plus` | جئوکدینگ پیشرفته |
| `neshan_direction` | routing | `/v4/direction` | مسیریابی با ترافیک لحظه‌ای |
| `neshan_direction_no_traffic` | routing | `/v4/direction/no-traffic` | مسیریابی بدون ترافیک |
| `neshan_direction_pedestrian` | routing | `/v4/direction` (`type=pedestrian`) | مسیریابی پیاده |
| `neshan_direction_typical` | routing | `/v1/direction/typical` | مسیریابی با ترافیک معمول (هر ۱۵ دقیقه به‌روزرسانی) |
| `neshan_direction_historical` | routing | `/v1/direction/historical` | مسیریابی برای زمان آینده بر اساس داده‌های تاریخی |
| `neshan_isochrone` | routing | `/v1/isochrone` | محاسبه ناحیه دسترس‌پذیر از یک نقطه در زمان/فاصله مشخص |
| `neshan_distance_matrix` | routing | `/v1/distance-matrix` | ماتریس فاصله/زمان چند نقطه |
| `neshan_tsp` | routing | `/v3/trip` | بهینه‌سازی مسیر چندایستگاهی (TSP) |
| `neshan_map_matching` | routing | ⚠️ نیازمند تأیید | تطبیق مسیر با جاده‌ها |
| `neshan_static_map` | map | `/v5/static` | تصویر نقشه استاتیک |
| `neshan_static_map_arc` | map | `/v4/static/arc` | تصویر نقشه استاتیک با رسم کمان بین مبدا و مقصد |

تمام مختصات `(lat, lng)` اعشاری.

## نصب

```bash
pip install -e .
```

نیازمند Python 3.10+ .

## پیکربندی (کلید)

**حالت HTTP — کلید در هدر هر درخواست:**

| هدر | کاربرد |
|---|---|
| `Neshan-Api-Key` | کلید برای همه‌ی سرویس‌ها |
| `Neshan-Api-Key-<service>` | override برای یک سرویس (مثل `Neshan-Api-Key-static`) |
| `Api-Key` | alias |

نام سرویس‌ها: `search`، `geocoding`، `routing`، `historical`، `isochrone`، `matrix`، `tsp`، `static`، `map_matching`.

**حالت stdio — fallback از env:**

```bash
cp .env.example .env   # NESHAN_API_KEY را قرار بده
```

کلیدهای نشان **service-scoped** هستند؛ هم در هدر و هم در env امکان کلید جدا برای هر سرویس وجود دارد.

## اجرا

```bash
neshan-mcp          # stdio (پیش‌فرض)
neshan-mcp-http     # HTTP
```

### Docker

```bash
docker build -t neshan-mcp .
docker run -p 3000:3000 --env-file .env neshan-mcp
```

## اتصال کلاینت

### HTTP (کلید در هدر)

```json
{
  "mcpServers": {
    "neshan": {
      "type": "http",
      "url": "http://localhost:3000/mcp",
      "headers": { "Neshan-Api-Key": "your_api_key_here" }
    }
  }
}
```

```bash
curl --location 'http://localhost:3000/mcp' \
  --header 'Accept: application/json, text/event-stream' \
  --header 'Content-Type: application/json' \
  --header 'Neshan-Api-Key: <API_KEY>' \
  --data '{"jsonrpc":"2.0","id":1,"method":"tools/call",
           "params":{"name":"neshan_reverse_geocode",
                     "arguments":{"lat":35.6997,"lng":51.3375}}}'
```

### Claude Desktop (stdio، کلید از env)

```json
{
  "mcpServers": {
    "neshan": {
      "command": "neshan-mcp",
      "env": { "NESHAN_API_KEY": "your_api_key_here" }
    }
  }
}
```

## نکات تأیید (قبل از production)

- `neshan_reverse_geocode` روی `v5` است؛ اگر اکانتت `v4` است، `Endpoints.REVERSE` را در `constants.py` عوض کن.
- `neshan_map_matching`: مسیر و نام پارامتر اندپوینت **تأیید نشده**؛ با مستندات زنده تطبیق بده یا `NESHAN_MAP_MATCHING_PATH` را ست کن.
- نقشه استاتیک کلید را به‌صورت query param (`key=`) می‌گیرد نه هدر — در `services/base/neshanClient.py` مدیریت شده است.

## مرجع

- مستندات نشان: https://platform.neshan.org/docs
- شروع به کار API: https://platform.neshan.org/api/getting-started
