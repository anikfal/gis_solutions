import requests
import pandas as pd
def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": "my_username",
        "password": "my_password",
        "grant_type": "password",
        }
    try:
        r = requests.post("https://identity.dataspace.copernicus.eu/auth/realms/CDSE/protocol/openid-connect/token",
        data=data,
        )
        r.raise_for_status()
    except Exception as e:
        raise Exception(
            f"Keycloak token creation failed. Reponse from the server was: {r.json()}"
            )
    return r.json()["access_token"]
keycloak_token = get_keycloak("username", "password")

start_date = "2022-06-01"
end_date = "2022-06-02"
data_collection = "SENTINEL-2"
aoi = "POLYGON((4.220581 50.958859,4.521264 50.953236,4.545977 50.906064,4.541858 50.802029,4.489685 50.763825,4.23843 50.767734,4.192435 50.806369,4.189689 50.907363,4.220581 50.958859))'"

json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}) and ContentDate/Start gt {start_date}T00:00:00.000Z and ContentDate/Start lt {end_date}T00:00:00.000Z").json()
pd.DataFrame.from_dict(json['value']).head(5)

session = requests.Session()
session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products(acdd7b9a-a5d4-5d10-9ac8-554623b8a0c9)/$value"
response = session.get(url, allow_redirects=False)
while response.status_code in (301, 302, 303, 307):
    url = response.headers['Location']
    response = session.get(url, allow_redirects=False)

file = session.get(url, verify=False, allow_redirects=True)

with open(f"product.zip", 'wb') as p:
    p.write(file.content)
