import pytest
from web3 import Web3
from solidity_python_sdk.main import DigitalProductPassportSDK

@pytest.fixture
def sdk():
    return DigitalProductPassportSDK()

def test_load_contract(sdk):
    contract = sdk.load_all_contracts()
    assert "abi" in contract['ProductPassport']
    assert "bytecode" in contract['ProductPassport']

def test_deploy_product_passport_contract(sdk):
    contract_address = sdk.product_passport.deploy(sdk.account.address)
    assert Web3.isAddress(contract_address)

def test_set_and_get_product(sdk):
    contract_address = sdk.product_passport.deploy(sdk.account.address)
    product_details = {
        "uid": "unique_id",
        "gtin": "1234567890123",
        "taricCode": "1234",
        "manufacturerInfo": "Manufacturer XYZ",
        "consumerInfo": "Consumer XYZ",
        "endOfLifeInfo": "Dispose properly"
    }
    tx_receipt = sdk.product_passport.set_product(contract_address, 1, product_details)
    assert tx_receipt["status"] == 1

    product = sdk.product_passport.get_product(contract_address, 1)
    assert product["productId"] == 1

def test_set_and_get_product_data(sdk):
    contract_address = sdk.product_passport.deploy(sdk.account.address)
    product_data = {
        "description": "Product description",
        "manuals": ["manual1.pdf"],
        "specifications": ["spec1.pdf"],
        "batchNumber": "123ABC",
        "productionDate": "2023-01-01",
        "expiryDate": "2023-12-31",
        "certifications": "ISO123",
        "warrantyInfo": "1 year",
        "materialComposition": "Materials",
        "complianceInfo": "Complies with regulations"
    }
    tx_receipt = sdk.product_passport.set_product_data(contract_address, 1, product_data)
    assert tx_receipt["status"] == 1

    product_data_retrieved = sdk.product_passport.get_product_data(contract_address, 1)
    assert product_data_retrieved["description"] == "Product description"
