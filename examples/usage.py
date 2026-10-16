import json
from solidity_python_sdk.main import DigitalProductPassportSDK

def deploy_and_set_product(details_file_path):
    # Initialize the SDK
    sdk = DigitalProductPassportSDK()

    # Load the details from the JSON file
    with open(details_file_path, 'r') as f:
        details = json.load(f)

    product_id = details.get("productId")
    if not product_id:
        raise ValueError("Product ID not found in JSON file")

    # Deploy and link all the contracts
    addresses = sdk.deploy_system()
    print(f"Contracts deployed at: {addresses}")

    # Every product must come from a registered complex
    sdk.complex_management.add_complex(addresses["complex_management"], details["complexId"], details["complex"])

    tx_receipt = sdk.product_passport.create_product(addresses["product_passport"], product_id, details["product"])

    if tx_receipt["status"] == 1:
        print("Product created successfully.")
        print(sdk.product_passport.get_product_details(addresses["product_passport"], product_id))
    else:
        print("Failed to create product.")

    return addresses

if __name__ == '__main__':
    deploy_and_set_product('details.json')
