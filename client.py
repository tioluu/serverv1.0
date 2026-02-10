import http.client
import urllib
import os
from dotenv import load_dotenv
load_dotenv()


host = "localhost:8080"
path = "/shorten"

data = urllib.parse.urlencode({"url": "https://github.com/tiolu"})

headers = {
    "User-Agent": "MyCustomClient/1.0",
    "Accept-Language": "en-US,en;q=0.9",
    "Content-type": "application/x-www-form-urlencoded",
    "Authorization": f"Bearer {os.getenv('SPOO_API_KEY')}",
}

conn = http.client.HTTPConnection(host)
conn.request("POST", path, body=data, headers=headers)

response = conn.getresponse()
print("Status:", response.status, response.reason)

data = response.read()
print("Data:", data.decode("utf-8"))
conn.close()
