#!/usr/bin/env python3
"""Check EOL dates for your tech stack using endoflife.date API."""

import sys
import json
from datetime import datetime, date
from urllib.request import urlopen, Request
from urllib.error import HTTPError

RED = "\033[91m"
YELLOW = "\033[93m"
GREEN = "\033[92m"
RESET = "\033[0m"

def fetch_versions(product: str) -> list:
    url = f"https://endoflife.date/api/{product}.json"
    try:
        req = Request(url, headers={"Accept": "application/json"})
        with urlopen(req, timeout=10) as resp:
            return json.loads(resp.read())
    except HTTPError as e:
        if e.code == 404:
            print(f"{product}: not found on endoflife.date")
        return []

def check_eol(product: str):
    versions = fetch_versions(product)
    if not versions:
        return

    today = date.today()

    for v in versions[:6]:  # latest 6 versions
        cycle = v.get("cycle", "?")
        latest = v.get("latest", cycle)
        eol = v.get("eol", False)
        
        if isinstance(eol, bool):
            eol_date = None
            status = "EOL" if eol else "Active"
        else:
            try:
                eol_date = datetime.strptime(str(eol), "%Y-%m-%d").date()
            except ValueError:
                eol_date = None
            
            if eol_date and eol_date < today:
                status = "EOL"
            elif eol_date:
                days_left = (eol_date - today).days
                if days_left < 180:
                    status = "Security"
                else:
                    status = "Active"
            else:
                status = "Active"

        # Format output
        eol_str = str(eol)[:7] if eol and not isinstance(eol, bool) else "N/A"
        
        if status == "EOL":
            icon = f"{RED}❌ EXPIRED{RESET}"
        elif status == "Security":
            if eol_date:
                months = (eol_date - today).days // 30
                icon = f"{YELLOW}⚠️  {months} months left{RESET}"
            else:
                icon = f"{YELLOW}⚠️  Security only{RESET}"
        else:
            if eol_date:
                years = round((eol_date - today).days / 365, 1)
                icon = f"{GREEN}✅ {years} years left{RESET}"
            else:
                icon = f"{GREEN}✅ Active{RESET}"

        print(f"{product:<12}{latest:<10}{status:<10}EOL: {eol_str:<12}{icon}")

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 eol_checker.py <product> [product2] ...")
        print("Example: python3 eol_checker.py python nodejs kubernetes")
        sys.exit(1)

    for product in sys.argv[1:]:
        check_eol(product.lower())
        if product != sys.argv[-1]:
            print()

if __name__ == "__main__":
    main()
