# App Server – Step-by-step guide (no Python knowledge needed)

This project is a **back end**: a program that runs on your computer, waits for requests
(like `POST /orders`), does some work, and answers. It also contains a **message broker**,
a "post office" that lets different parts of the program talk to each other by leaving
messages instead of calling each other directly.

---

## 1. Words you will see

| Word | Plain meaning |
|---|---|
| **Endpoint** | A web address the server answers, e.g. `http://127.0.0.1:8000/orders`. |
| **Service file** | One `.py` file that groups the endpoints for one topic (orders, shipping, ...). |
| **Message broker** | The post office. A service *publishes* a message on a **topic** (e.g. `order.created`); any service that *subscribed* to that topic receives it. |
| **Topic** | The name on the message, like `order.created`. `order.*` means "any topic starting with `order.`". |
| **Redis** | A separate program (on your Linux machine) that stores messages safely, so they survive restarts and can be shared between servers. |
| **Dead letter** | A message that failed every retry. It is put aside so you can inspect it. |
| **venv (`.venv`)** | A private folder holding the libraries this project needs, so nothing else on your PC is affected. |

---

## 2. What is in the folder

```
Server/
├─ setup.ps1            <- the ONE script you run (installs everything, starts the server)
├─ config.env           <- ALL settings you may want to change (Redis address, port...)
├─ requirements.txt     <- list of libraries to download (setup.ps1 reads it)
├─ GUIDE.md             <- this file
└─ app/
   ├─ main.py           <- starts the server, finds the service files, starts the broker
   ├─ core/config.py    <- reads config.env
   ├─ broker/           <- the message broker
   │   ├─ base.py          rules every broker follows (Message, retries)
   │   ├─ memory.py        broker that lives inside the program (no setup)
   │   ├─ redis_broker.py  broker that stores messages in Redis
   │   └─ factory.py       picks memory or redis according to config.env
   └─ services/         <- ONE FILE PER TOPIC. Files must end in _service.py
       ├─ health_service.py    /health, /broker/stats, /broker/dead-letters
       ├─ orders_service.py    /orders   (creates orders, publishes messages)
       └─ shipping_service.py  listens for new orders and "ships" them
```

---

## 3. Running it on Windows (first time)

1. Open **PowerShell** and go to the folder:
   ```powershell
   cd F:\prototipos\Python\App\Server
   ```
2. Run:
   ```powershell
   .\setup.ps1
   ```
   If Windows refuses with "running scripts is disabled", run this once and try again:
   ```powershell
   Set-ExecutionPolicy -Scope CurrentUser RemoteSigned
   ```
3. What the script does for you, in order:
   1. **Checks Python** (version 3.10 or newer). If it is missing, it installs Python
      3.12 using `winget` (built into Windows 10/11). Note: the Windows "Store" `python`
      shortcut does not count as installed; the script knows this.
   2. Creates the private `.venv` folder (first time only).
   3. Downloads the libraries listed in `requirements.txt` into `.venv`.
   4. Starts the server.
4. Open <http://127.0.0.1:8000/docs> in a browser. That page lists every endpoint and lets
   you try them with a button.
5. Stop the server with **Ctrl+C**.

Only want to install, without starting? `.\setup.ps1 -NoRun`

### Running it as a command (`server`)

`server.cmd` starts the server with one word, from any folder. It skips the reinstall
checks once `.venv` exists, so it starts fast (if `.venv` is missing it runs `setup.ps1` first).

- From inside the project folder: `.\server.cmd`
- From anywhere: add the project folder to your user PATH **once**:
  ```powershell
  $dir = "F:\prototipos\Python\App\Server"
  [Environment]::SetEnvironmentVariable("Path", [Environment]::GetEnvironmentVariable("Path","User") + ";$dir", "User")
  ```
  Close and reopen the terminal, then just type:
  ```
  server
  ```
- To undo it, remove that folder from *Settings > System > About > Advanced system settings >
  Environment Variables > Path (User)*.

### Try it

In the `/docs` page, open `POST /orders`, click **Try it out**, use
`{"item": "book", "quantity": 2}` and **Execute**. Then `GET /orders/1`: the status is
`shipped`. Nobody told the orders service to ship it; it happened through messages:

```
POST /orders ──> orders_service ──publishes "order.created"──> broker
                                                                  │
shipping_service <────────── receives "order.created" ────────────┘
shipping_service ──publishes "order.shipped"──> broker ──> orders_service (status = shipped)
```

`GET /broker/stats` shows how many messages each listener handled.

---

## 4. Using Redis on your Linux machine

By default `BROKER_BACKEND=memory`: nothing to install, but messages vanish when the
server stops. With Redis, messages are stored on the Linux machine.

### 4.1 Install and prepare Redis on the Linux machine

Debian/Ubuntu example (run on Linux):

```bash
sudo apt update && sudo apt install -y redis-server
sudo nano /etc/redis/redis.conf
```

Change these lines in `redis.conf`:

```
bind 0.0.0.0                 # accept connections from other machines (default is local only)
requirepass CHOOSE_A_STRONG_PASSWORD
```

Then:

```bash
sudo systemctl restart redis-server
sudo systemctl enable redis-server          # start on boot
sudo ufw allow from <WINDOWS_PC_IP> to any port 6379   # only if you use ufw firewall
hostname -I                                  # shows the Linux machine's IP address
```

**Security:** never open port 6379 to the internet. Keep it on your local network (or a VPN),
and always set a password.

### 4.2 Point the server at it

Edit **`config.env`** (any text editor):

```
BROKER_BACKEND=redis
REDIS_HOST=192.168.0.10        <- the Linux machine's IP
REDIS_PORT=6379
REDIS_PASSWORD=CHOOSE_A_STRONG_PASSWORD
```

Save, then run `.\setup.ps1` again. In the log you should see
`redis broker connected to 192.168.0.10:6379/0`. `GET /broker/stats` will show
`"backend": "redis"`.

If Redis cannot be reached, the server refuses to start and prints a message telling you
which settings to check (address, password, firewall). Quick test from Windows:
```powershell
Test-NetConnection 192.168.0.10 -Port 6379
```

### 4.3 What you gain with Redis

- Messages are **not lost** if the server restarts; work continues where it stopped.
- If the server crashes while handling a message, another server instance picks it up
  after 30 seconds.
- You can run **several copies** of the server against the same Redis. Copies share the work.
- A failing message is retried (`BROKER_MAX_RETRIES`, default 3), then stored in a
  dead-letter list, visible at `GET /broker/dead-letters`.

Peek inside Redis from the Linux machine: `redis-cli -a PASSWORD XLEN appserver:events`

---

## 5. All settings (`config.env`)

| Name | Default | Meaning |
|---|---|---|
| `APP_HOST` | `127.0.0.1` | `127.0.0.1` = only this PC can call the API. `0.0.0.0` = other machines can too. |
| `APP_PORT` | `8000` | Port of the API. |
| `BROKER_BACKEND` | `memory` | `memory` or `redis`. |
| `BROKER_MAX_RETRIES` | `3` | Attempts before a message is dead-lettered. |
| `REDIS_HOST` / `REDIS_PORT` | – / `6379` | Where Redis is. |
| `REDIS_PASSWORD` | empty | Redis password. |
| `REDIS_DB` | `0` | Redis database number (0–15). |
| `REDIS_SSL` | `false` | `true` if your Redis uses TLS. |
| `REDIS_PREFIX` | `appserver` | Prefix of the keys created in Redis. |

A setting can also come from a Windows environment variable of the same name, which wins
over the file. Setting `APP_CONFIG` to a file path makes the server read that file instead
(handy to keep a separate file for production).

---

## 6. Adding your own service (a new topic)

1. Create `app/services/customers_service.py` (the name **must end in `_service.py`**).
2. Use this template:

```python
from fastapi import APIRouter, Depends
from app.broker import Broker, Message
from app.core.deps import get_broker

router = APIRouter(prefix="/customers", tags=["customers"])   # the address: /customers

@router.post("")                                              # POST /customers
async def create_customer(name: str, broker: Broker = Depends(get_broker)):
    await broker.publish("customer.created", {"name": name})  # leave a message
    return {"ok": True}

def register(broker: Broker):                                 # optional: listen to topics
    broker.subscribe("order.created", on_order, name="customers.on_order")

async def on_order(msg: Message):                             # runs when a message arrives
    print("New order:", msg.payload)
```

3. Restart the server. **Nothing else to edit**: the file is found automatically.

Rules to remember:
- The `name=` of every subscription must be **unique across all files**.
- If a listener raises an error, the message is retried, then dead-lettered. Listeners
  should be safe to run twice for the same message (Redis guarantees "at least once" delivery).
- Message content (`payload`) must be plain data: numbers, text, lists, dictionaries.

---

## 7. Testing

### 7.1 Manual testing with Postman (`postman/` folder)

1. Postman > **Import** > select the three files in `postman/`.
2. Top-right environment dropdown: choose **App Server - Local** (`http://127.0.0.1:8000`)
   or **App Server - Remote** (edit `base_url` to the IP of the machine running the server).
3. Start the server (`server`), then open the collection **App Server** > **Run**.
   Every request has checks (green/red): health, create order, get order, 404, 422 for a
   bad quantity, shipping list, broker stats, dead letters.

### 7.2 Automated tests (`tests/` folder)

They start the app in memory and need no running server and no Redis (Redis is
simulated). One-time setup, then run:

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
.\.venv\Scripts\python.exe -m pytest -q
```

Expected: `12 passed`. What is checked:
- `tests/test_api.py`: endpoints, validation errors, and that an order becomes `shipped`
  through the broker.
- `tests/test_broker.py`: the same broker behaviour on **both** memory and Redis backends:
  topic matching, retries then dead-letter, duplicate subscription names rejected.

Tests ignore `config.env` and always use the memory broker, so they never touch your real Redis.

---

## 8. Troubleshooting

| Problem | Fix |
|---|---|
| `running scripts is disabled` | `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` |
| "Python was installed but is not visible yet" | Close PowerShell, open a new one, run `.\setup.ps1` again. |
| `Cannot reach Redis at ...` | Wrong `REDIS_HOST`/port, Redis stopped (`sudo systemctl status redis-server`), `bind` still local-only, or firewall. |
| Redis `NOAUTH` / `invalid password` | `REDIS_PASSWORD` does not match `requirepass`. |
| Port 8000 already in use | Change `APP_PORT` in `config.env`. |
| My new service does not appear | File name must end in `_service.py`, and must define `router`. |
| Other PC cannot reach the API | Set `APP_HOST=0.0.0.0` and allow the port in the Windows firewall. |

## 9. Limits to know about

- **No login/authentication** on the API yet. Do not expose it beyond your own network as is.
- Orders are kept in program memory (a plain list), so they vanish on restart. Only the
  *messages* are durable with Redis. A real database is the natural next step.
