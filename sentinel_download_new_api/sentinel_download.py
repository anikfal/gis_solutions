# Download SENTINEL-2 data over a period of time for specific points.
# Contact person: Amir H. Nikfal <a.nikfal@fz-juelich.de>

import csv
import os
import logging
import json as jsonmod
from glob import glob
import user_inputs as inp
try:
    import requests
except ImportError:
    print("Error: module <requests> is not installed. Install it and run again.")
    exit()

def get_keycloak(username: str, password: str) -> str:
    data = {
        "client_id": "cdse-public",
        "username": inp.username,
        "password": inp.password,
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

start_date = f"{inp.start_year}-{format(inp.start_month, '02d')}-{format(inp.start_day, '02d')}T{format(inp.start_hour, '02d')}:00:00.000Z"
end_date = f"{inp.end_year}-{format(inp.end_month, '02d')}-{format(inp.end_day, '02d')}T{format(inp.end_hour, '02d')}:00:00.000Z"
data_collection = "SENTINEL-2"
logging.basicConfig(filename='log_sentinel_download' + start_date + '.log',
                    filemode='a',
                    format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',
                    level=logging.INFO)

csvfile = open("points_coordinates.csv", newline='')
all_points = csv.DictReader(csvfile)
keycloak_token = get_keycloak("username", "password")

foundtiles_dict = dict()
count = 2
for point in all_points:
        logging.info("Row: " + str(count))
        if (count+4)%5 == 0:
            keycloak_token = get_keycloak("username", "password")
        aoi = "POINT(" + point['LONG'] + " " + point['LAT'] + ")'"
        print("Looking for data over the point:", point)
        json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' \
                            and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}) and ContentDate/Start gt {start_date} \
                                and ContentDate/Start lt {end_date}").json()
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
        lookedup_tiles = json['value']
        for var in lookedup_tiles:
            try:
                if "MSIL2A" in var['Name']:
                    logging.info("Row found: " + str(count))
                    myfilename = var['Name']
                    logging.info("File OK: " + myfilename)
                    mytile = myfilename.split("_")[-2]
                    foundtiles_dict[mytile] = [point['LONG'], point['LAT']]
                    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products(" + var['Id'] + ")/$value"
                    response = session.get(url, allow_redirects=False)
                    while response.status_code in (301, 302, 303, 307):
                        logging.info("response: " + str(response.status_code))
                        url = response.headers['Location']
                        logging.info("next line ...")
                        response = session.get(url, allow_redirects=False)
                        logging.info("Last line ...")
                    file = session.get(url, verify=False, allow_redirects=True)
                    with open(f""+var['Name']+".zip", 'wb') as p:
                        p.write(file.content)
            except:
                pass
        count = count + 1

###############################################################################
# Verifying downloaded files
###############################################################################

keycloak_token = get_keycloak("username", "password")
with open('list_downloaded_files.txt', 'w') as file:
   file.write(jsonmod.dumps(foundtiles_dict))

filelist=glob("S2*.SAFE.zip")
corrupted = []
for var in filelist:
   if int(os.path.getsize(var)/1024) < 10:
      corrupted.append(var)

count = 2
for point in corrupted:
        logging.info("Currpted Row: " + str(count))
        tile_retry = point.split("_")[-2]
        if (count+3)%4 == 0:
            keycloak_token = get_keycloak("username", "password")
        mylong = foundtiles_dict[tile_retry][0]
        mylat = foundtiles_dict[tile_retry][1]
        aoi = "POINT(" + mylong + " " + mylat + ")'"
        print("Retrying to get the point:", mylong, mylat)
        json = requests.get(f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products?$filter=Collection/Name eq '{data_collection}' \
                            and OData.CSC.Intersects(area=geography'SRID=4326;{aoi}) and ContentDate/Start gt {start_date} \
                                and ContentDate/Start lt {end_date}").json()
        session = requests.Session()
        session.headers.update({'Authorization': f'Bearer {keycloak_token}'})
        lookedup_tiles = json['value']
        for var in lookedup_tiles:
            try:
                if "MSIL2A" in var['Name']:
                    logging.info("Currpted Row found: " + str(count))
                    myfilename = var['Name']
                    logging.info("Currpted File OK: " + myfilename)
                    url = f"https://catalogue.dataspace.copernicus.eu/odata/v1/Products(" + var['Id'] + ")/$value"
                    response = session.get(url, allow_redirects=False)
                    while response.status_code in (301, 302, 303, 307):
                        logging.info("Currpted response: " + str(response.status_code))
                        url = response.headers['Location']
                        logging.info("Currpted next line ...")
                        response = session.get(url, allow_redirects=False)
                        logging.info("Currpted Last line ...")
                    file = session.get(url, verify=False, allow_redirects=True)
                    with open(f""+var['Name']+".zip", 'wb') as p:
                        p.write(file.content)
            except:
                pass
        count = count + 1