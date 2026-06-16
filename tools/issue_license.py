#!/usr/bin/env python3
"""Mint a signed license token. VENDOR-ONLY — needs the private key.

  python tools/issue_license.py --key private.pem --sub pmp --days 30 --grace 14 > token.jwt

Then install token.jwt on the Pi at  license/secrets/token.jwt  and the gate
picks it up on the next request (no restart). On payment, re-run with a longer
--days (or a far-future date) and replace the file to unlock permanently.

Install once:  pip install "pyjwt[crypto]"
"""
import argparse
import time

import jwt
from cryptography.hazmat.primitives.serialization import load_pem_private_key


def main() -> None:
    p = argparse.ArgumentParser(description="Mint a signed license token (EdDSA).")
    p.add_argument("--key", required=True, help="path to private.pem")
    p.add_argument("--sub", required=True, help="client/deployment id, e.g. pmp")
    p.add_argument("--days", type=int, required=True, help="validity in days from now")
    p.add_argument("--grace", type=int, default=14, help="banner window (days) before expiry")
    p.add_argument("--iss", default="vendor", help="issuer label")
    a = p.parse_args()

    now = int(time.time())
    claims = {
        "iss": a.iss,
        "sub": a.sub,
        "iat": now,
        "exp": now + a.days * 86400,
        "grace_days": a.grace,
    }
    key = load_pem_private_key(open(a.key, "rb").read(), password=None)
    print(jwt.encode(claims, key, algorithm="EdDSA"))


if __name__ == "__main__":
    main()
