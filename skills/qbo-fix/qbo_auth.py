#!/usr/bin/env python3
"""
CFTA QBO auth helper — ALWAYS use this instead of hardcoding tokens.
Intuit rotates refresh tokens; this persists the rotated token back to the
creds file on every call so the chain never breaks.

Usage:
    from qbo_auth import get_token, BASE_URL
    token = get_token()
"""
import json
import os
import requests

CREDS_PATH = os.path.expanduser("~/.config/cfta/qbo_creds.json")
REALM_ID = "9130350131931956"
BASE_URL = f"https://quickbooks.api.intuit.com/v3/company/{REALM_ID}"


def get_token():
    with open(CREDS_PATH) as f:
        creds = json.load(f)
    r = requests.post(
        "https://oauth.platform.intuit.com/oauth2/v1/tokens/bearer",
        auth=(creds["client_id"], creds["client_secret"]),
        data={"grant_type": "refresh_token", "refresh_token": creds["refresh_token"]},
        headers={"Accept": "application/json"},
    )
    if r.status_code != 200:
        raise RuntimeError(
            f"QBO token refresh failed ({r.status_code}): {r.text[:200]}\n"
            "If invalid_grant: the refresh token is dead — re-authorize via the "
            "Intuit OAuth playground and update ~/.config/cfta/qbo_creds.json. "
            "Meanwhile use the QBO MCP connector tools for customer/invoice work."
        )
    body = r.json()
    # CRITICAL: persist the rotated refresh token
    new_rt = body.get("refresh_token")
    if new_rt and new_rt != creds["refresh_token"]:
        creds["refresh_token"] = new_rt
        tmp = CREDS_PATH + ".tmp"
        with open(tmp, "w") as f:
            json.dump(creds, f, indent=1)
        os.replace(tmp, CREDS_PATH)
    return body["access_token"]


if __name__ == "__main__":
    t = get_token()
    print(f"token ok ({len(t)} chars); refresh token persisted if rotated")
