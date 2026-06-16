"""Activation / grace gate — tiny verifier the edge calls via Caddy forward_auth.

It checks a vendor-signed license token (EdDSA/RS256 JWT) against the bundled
PUBLIC key. The vendor keeps the private key OFF the box, so the client can't
forge or extend a license. Reversible: drop in a new signed token and the next
request unlocks — no data is ever touched.

Endpoints:
  GET /verify  -> 204 when active/grace (Caddy proceeds), 402 + activation page otherwise.
  GET /status  -> JSON {state, expires, days_left, sub} for an optional grace banner.

State machine: active -> grace (within grace_days of exp) -> expired.
Fails CLOSED (no/invalid token => locked) and resists clock rollback via a
high-water-mark on a volume.
"""
import os
import time
import pathlib

import jwt  # PyJWT
from cryptography.hazmat.primitives.serialization import load_pem_public_key
from fastapi import FastAPI, Response

TOKEN_PATH = os.environ.get("LICENSE_TOKEN_PATH", "/license/token.jwt")
PUBKEY_PATH = os.environ.get("LICENSE_PUBKEY_PATH", "/license/public.pem")
STATE_PATH = os.environ.get("LICENSE_STATE_PATH", "/state/highwater")
VENDOR = os.environ.get("VENDOR_NAME", "the vendor")
CONTACT = os.environ.get("VENDOR_CONTACT", "")
# How far the clock may legitimately move backwards (NTP/timezone) before we
# treat it as tampering. Default 2 days.
ROLLBACK_SKEW = int(os.environ.get("LICENSE_ROLLBACK_SKEW_SEC", str(2 * 86400)))

app = FastAPI(title="activation-gate")


def _read(path: str) -> str | None:
    try:
        return pathlib.Path(path).read_text().strip()
    except Exception:
        return None


def _highwater() -> int:
    try:
        return int(_read(STATE_PATH) or 0)
    except Exception:
        return 0


def _bump(now: int) -> None:
    hw = max(_highwater(), now)
    try:
        p = pathlib.Path(STATE_PATH)
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(str(hw))
    except Exception:
        pass


def evaluate() -> dict:
    now = int(time.time())
    hw = _highwater()
    if hw and now < hw - ROLLBACK_SKEW:
        return {"state": "tamper", "reason": "clock rolled back", "expires": None, "days_left": 0}
    _bump(now)

    token = _read(TOKEN_PATH)
    if not token:
        return {"state": "missing", "reason": "no license token", "expires": None, "days_left": 0}
    pub = _read(PUBKEY_PATH)
    if not pub:
        return {"state": "misconfigured", "reason": "no public key", "expires": None, "days_left": 0}
    try:
        key = load_pem_public_key(pub.encode())
        claims = jwt.decode(token, key, algorithms=["EdDSA", "RS256"], options={"verify_exp": False})
    except Exception as e:  # bad signature / malformed
        return {"state": "invalid", "reason": f"bad token: {e}", "expires": None, "days_left": 0}

    exp = int(claims.get("exp", 0))
    grace = int(claims.get("grace_days", 0)) * 86400
    sub = claims.get("sub")
    days_left = max(0, (exp - now) // 86400)
    if now >= exp:
        return {"state": "expired", "reason": "license expired", "expires": exp, "days_left": 0, "sub": sub}
    if now >= exp - grace:
        return {"state": "grace", "expires": exp, "days_left": days_left, "sub": sub}
    return {"state": "active", "expires": exp, "days_left": days_left, "sub": sub}


def _page(info: dict) -> str:
    contact = f'<p>Contact: <a href="mailto:{CONTACT}">{CONTACT}</a></p>' if CONTACT else ""
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Activation required</title>
<style>
  html,body{{height:100%;margin:0;font-family:system-ui,Segoe UI,Roboto,sans-serif}}
  body{{display:grid;place-items:center;background:#0f1115;color:#e8eaed}}
  .card{{max-width:34rem;padding:2.5rem;text-align:center}}
  h1{{font-size:1.6rem;margin:0 0 .5rem}}
  p{{color:#aab;line-height:1.6}}
  .tag{{display:inline-block;margin-bottom:1rem;padding:.25rem .7rem;border-radius:999px;
       background:#3a2a12;color:#f0c674;font-size:.8rem;letter-spacing:.03em}}
  a{{color:#7fb0ff}}
</style></head><body><div class="card">
  <div class="tag">{info.get('state','locked').upper()}</div>
  <h1>Activation required</h1>
  <p>This deployment's evaluation period has ended. It will resume immediately
     once {VENDOR} activates it — no data is affected.</p>
  {contact}
</div></body></html>"""


@app.get("/verify")
def verify():
    info = evaluate()
    if info["state"] in ("active", "grace"):
        return Response(status_code=204)
    return Response(content=_page(info), media_type="text/html", status_code=402)


@app.get("/status")
def status():
    return evaluate()


@app.get("/healthz")
def healthz():
    return {"ok": True}
