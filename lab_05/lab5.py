import requests
import json

urls = [
    "https://loc.gov/resource/cph.3f05183/",
    "https://loc.gov/resource/fsa.8d24709/",
    "https://loc.gov/resource/highsm.64003/",
]
parameters = {"fo": "json"}
for url in urls:
    response = requests.get(url, params=parameters)

    if response.status_code == 200:
        data = response.json()

        lccn = data.get("item", {}).get("lccn", "")
        if not lccn and "lccn" in data:
            lccn = data["lccn"] if isinstance(data["lccn"], list) else data["lccn"]

        lccn = lccn.strip()
        permalink = f"https://loc.gov{lccn}"
        print(f"Resource: {url} -> Permalink: {permalink}")


for index, url in enumerate(urls, start=1):
    response = requests.get(url, params=parameters)
    if response.status_code == 200:
        data = response.json()
        filename = f"item_{index}_data.json"

        with open(filename, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

        print(f"Successfully retrieved and saved data to {filename}")

search_url = "https://loc.gov/search"


user_query = input("Enter your search query: ")

search_parameters = {"fo": "json", "q": user_query}

response = requests.get(search_url, params=search_parameters)

if response.status_code == 200:
    results_data = response.json()
    print("\nSearch results successfully returned from server:")

    print(
        json.dumps(results_data, sort_keys=True, indent=4)[:1000]
        + "\n... [Truncated for preview]"
    )
