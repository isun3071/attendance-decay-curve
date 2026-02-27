import requests
import pandas as pd

BASE_URL = "https://bu.campuslabs.com/engage/api/discovery/search/organizations"
DETAIL_URL = "https://bu.campuslabs.com/engage/api/discovery/organization/bykey/{}"

params = {
    "orderBy[0]": "UpperName asc",
    "top": 10,
    "filter": "(CategoryIds/any(x: x eq '12680') or CategoryIds/any(x: x eq '12682') or CategoryIds/any(x: x eq '12684') or CategoryIds/any(x: x eq '12695'))",
    "query": "",
    "skip": 0
}

all_orgs = []

while True:
    response = requests.get(BASE_URL, params=params)
    data = response.json()

    orgs = data.get("value", [])
    if not orgs:
        break

    for org in orgs:
        name = org.get("Name", "").strip()
        key = org.get("WebsiteKey", "")

        detail = requests.get(DETAIL_URL.format(key)).json()
        email = detail.get("email", "")

        all_orgs.append({
            "Name": name,
            "WebsiteKey": key,
            "Email": email
        })
        print(f"{len(all_orgs)}. {name} ({key}): {email}")
        with open("bu_org_emails.txt", "a") as f:
            f.write(f"{len(all_orgs)}. {name} ({key}): {email}\n")

    params["skip"] += params["top"]


print("Done.")