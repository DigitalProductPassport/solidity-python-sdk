from datetime import datetime
from solidity_python_sdk.main import DigitalProductPassportSDK

# Initialize SDK
sdk = DigitalProductPassportSDK()

# Complex where the product is made
factory = {
    "complexId": "SWEET-DELIGHTS-SP",
    "complexName": "Sweet Delights Factory",
    "complexCountry": "Brazil",
    "complexAddress": "Rua das Flores 100, Sao Paulo",
    "geolocationId": "GEO-SAO-PAULO",
    "complexSiteType": "Manufacturing",
    "complexIndustry": "Food",
    "latitude": "-23.5505",
    "longitude": "-46.6333",
    "additionalInfo": "Sao Paulo, Brazil"
}

# Distribution centers the batches are shipped to. Geolocation is owned by
# ComplexManagement, so batches can only move to locations registered as complexes.
distribution_centers = [
    {"complexId": "DC-NYC", "geolocationId": "GEO-NYC", "latitude": "40.7128", "longitude": "-74.0060", "additionalInfo": "New York City, USA"},
    {"complexId": "DC-LA", "geolocationId": "GEO-LA", "latitude": "34.0522", "longitude": "-118.2437", "additionalInfo": "Los Angeles, USA"},
    {"complexId": "DC-LONDON", "geolocationId": "GEO-LONDON", "latitude": "51.5074", "longitude": "-0.1278", "additionalInfo": "London, UK"},
    {"complexId": "DC-TOKYO", "geolocationId": "GEO-TOKYO", "latitude": "35.6895", "longitude": "139.6917", "additionalInfo": "Tokyo, Japan"},
    {"complexId": "DC-SYDNEY", "geolocationId": "GEO-SYDNEY", "latitude": "-33.8688", "longitude": "151.2093", "additionalInfo": "Sydney, Australia"}
]

# Product data to deploy
product_id = 1
product_data = {
    "description": "Brigadeiro Product Passport",
    "manuals": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "specifications": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    # Addresses of the material passports (condensed milk, cocoa, butter, sprinkles)
    "materialComposition": ["0x000000000000000000000000000000000000dEaD"],
    "complexId": factory["complexId"]
}

metadata_ipfs_hash = "QmWDYhFAaT89spcqbKYboyCm6mkYSxKJaWUuS18Akmw96t"

def convert_to_unix_timestamp(date_string):
    date_format = "%Y-%m-%d %H:%M:%S"
    dt = datetime.strptime(date_string, date_format)
    return int(dt.timestamp())

def register_complexes(complex_management_address):
    sdk.complex_management.add_complex(complex_management_address, factory["complexId"], factory)

    for center in distribution_centers:
        sdk.complex_management.add_complex(complex_management_address, center["complexId"], {
            "complexName": f"Distribution Center {center['additionalInfo']}",
            "complexCountry": center["additionalInfo"].split(", ")[-1],
            "complexAddress": center["additionalInfo"],
            "complexSiteType": "Distribution",
            "complexIndustry": "Logistics",
            **center
        })

def deploy_product_passport(product_passport_address):
    result = sdk.product_passport.create_product(product_passport_address, product_id, product_data)
    print(f"Create Product Result: {result}")

def deploy_batches(batch_address):
    assembling_time = convert_to_unix_timestamp("2023-06-20 12:00:00")

    for i, center in enumerate(distribution_centers):
        batch_id = i + 1
        sdk.batch.create_batch(batch_address, {
            "batchId": batch_id,
            "amount": 100,
            "assemblingTime": assembling_time,
            "transportDetails": f"Shipped via Express {batch_id}",
            "productId": product_id
        })
        sdk.batch.update_batch_location(batch_address, batch_id, center["geolocationId"])
        sdk.batch.set_token_uri(batch_address, batch_id, f"ipfs://{metadata_ipfs_hash}")
        print(f"Batch {batch_id} shipped to {center['additionalInfo']}")

if __name__ == '__main__':
    addresses = sdk.deploy_system()
    register_complexes(addresses["complex_management"])
    deploy_product_passport(addresses["product_passport"])
    deploy_batches(addresses["batch"])

    print(f"ProductPassport Contract Address: {addresses['product_passport']}")
    print(f"Batch Contract Address: {addresses['batch']}")
