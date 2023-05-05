import json
import os

import requests
from dotenv import load_dotenv

load_dotenv()


PROVINCE_API = "https://online-gateway.ghn.vn/shiip/public-api/master-data/province"
DISTRICT_API = "https://online-gateway.ghn.vn/shiip/public-api/master-data/district"
WARD_API = "https://online-gateway.ghn.vn/shiip/public-api/master-data/ward"
API_TOKEN = os.environ.get("API_TOKEN")


def get_provinces():
    r = requests.get(PROVINCE_API, headers={"Token": API_TOKEN})
    if r.status_code == 200:
        data = r.json()["data"]
        provinces = [
            {
                "model": "core.province",
                "pk": province["ProvinceID"],
                "fields": {
                    "name": province["ProvinceName"],
                    "code": province["ProvinceID"],
                },
            }
            for province in data
        ]
        return provinces
    else:
        return None


def get_districts(province_id):
    r = requests.get(
        DISTRICT_API, headers={"Token": API_TOKEN}, params={"province_id": province_id}
    )
    if r.status_code == 200:
        data = r.json()["data"]
        districts = [
            {
                "model": "core.district",
                "pk": district["DistrictID"],
                "fields": {
                    "name": district["DistrictName"],
                    "code": district["DistrictID"],
                    "province": province_id,
                },
            }
            for district in data
        ]
        return districts
    else:
        return None


def get_wards(district_id):
    r = requests.get(
        WARD_API, headers={"Token": API_TOKEN}, params={"district_id": district_id}
    )
    if r.status_code == 200:
        data = r.json()["data"]
        if data is None:
            return []
        wards = [
            {
                "model": "core.ward",
                "pk": ward["WardCode"],
                "fields": {
                    "name": ward["WardName"],
                    "code": ward["WardCode"],
                    "district": district_id,
                },
            }
            for ward in data
        ]
        return wards
    else:
        return []


def provices_to_fixtures():
    provinces = get_provinces()
    with open("provinces.json", "w") as f:
        json.dump(provinces, f, indent=4, ensure_ascii=False)

    return provinces


def districts_to_fixtures(provinces):
    districts = []
    for province in provinces:
        province_id = province["pk"]
        districts += get_districts(province_id)
    with open("districts.json", "w") as f:
        json.dump(districts, f, indent=4, ensure_ascii=False)

    return districts


def wards_to_fixtures(districts):
    wards = []
    for district in districts:
        district_id = district["pk"]
        wards += get_wards(district_id)
    with open("wards.json", "w") as f:
        json.dump(wards, f, indent=4, ensure_ascii=False)

    return wards


if __name__ == "__main__":
    with open("districts.json", "r") as f:
        districts = json.load(f)
        wards_to_fixtures(districts)
