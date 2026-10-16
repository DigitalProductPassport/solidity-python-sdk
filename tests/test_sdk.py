import pytest
from web3 import Web3, EthereumTesterProvider
from web3.exceptions import ContractLogicError
from eth_tester.exceptions import TransactionFailed
from solidity_python_sdk.main import DigitalProductPassportSDK

# Real nodes raise ContractLogicError on revert, eth-tester raises TransactionFailed
REVERTED = (ContractLogicError, TransactionFailed)

COMPLEX_ID = "FACTORY-1"
PRODUCT_ID = 1
BATCH_ID = 7

COMPLEX = {
    "complexName": "Sweet Delights Factory",
    "complexCountry": "Brazil",
    "complexAddress": "Rua das Flores 100, Sao Paulo",
    "geolocationId": "GEO-FACTORY-1",
    "complexSiteType": "Manufacturing",
    "complexIndustry": "Food",
    "latitude": "-23.5505",
    "longitude": "-46.6333",
    "additionalInfo": "Main plant",
}

PRODUCT = {
    "description": "Brigadeiro",
    "manuals": ["QmManual"],
    "specifications": ["QmSpec"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    "materialComposition": ["0x000000000000000000000000000000000000dEaD"],
    "complexId": COMPLEX_ID,
}


@pytest.fixture()
def sdk():
    w3 = Web3(EthereumTesterProvider())
    account = w3.eth.account.create()
    w3.eth.send_transaction({"from": w3.eth.accounts[0], "to": account.address, "value": w3.to_wei(100, "ether")})
    return DigitalProductPassportSDK(private_key=account.key, web3=w3)


@pytest.fixture()
def system(sdk):
    return sdk.deploy_system()


@pytest.fixture()
def product(sdk, system):
    sdk.complex_management.add_complex(system["complex_management"], COMPLEX_ID, COMPLEX)
    sdk.product_passport.create_product(system["product_passport"], PRODUCT_ID, PRODUCT)


def test_load_contracts(sdk):
    for name in ["Geolocation", "ComplexManagement", "ProductPassport", "IntegratedProductPassportBatch"]:
        assert sdk.contracts[name]["abi"], f"ABI not found for '{name}'"
        assert sdk.contracts[name]["bytecode"], f"Bytecode not found for '{name}'"


def test_deploy_system_wires_contracts(sdk, system):
    assert all(Web3.is_address(address) for address in system.values())
    assert sdk.complex_management.geolocation_contract(system["complex_management"]) == system["geolocation"]
    assert sdk.product_passport.complex_management(system["product_passport"]) == system["complex_management"]
    assert sdk.geolocation.owner(system["geolocation"]) == system["complex_management"]
    assert sdk.batch.owner(system["batch"]) == sdk.account.address


def test_geolocation(sdk):
    address = sdk.geolocation.deploy()
    sdk.geolocation.set_geolocation(address, "GEO-1", "40.7128", "-74.0060", "New York City")
    assert sdk.geolocation.geolocation_exists(address, "GEO-1")
    assert sdk.geolocation.get_geolocation(address, "GEO-1") == {
        "latitude": "40.7128", "longitude": "-74.0060", "additionalInfo": "New York City",
    }

    sdk.geolocation.update_geolocation(address, "GEO-1", "51.5074", "-0.1278", "London")
    assert sdk.geolocation.get_geolocation(address, "GEO-1")["additionalInfo"] == "London"

    sdk.geolocation.remove_geolocation(address, "GEO-1")
    assert not sdk.geolocation.geolocation_exists(address, "GEO-1")


def test_complex_management(sdk, system):
    address = system["complex_management"]
    sdk.complex_management.add_complex(address, COMPLEX_ID, COMPLEX)

    assert sdk.complex_management.complex_exists(address, COMPLEX_ID)
    assert sdk.complex_management.get_complex(address, COMPLEX_ID) == {
        "complexName": "Sweet Delights Factory",
        "complexCountry": "Brazil",
        "complexAddress": "Rua das Flores 100, Sao Paulo",
        "complexSiteType": "Manufacturing",
        "complexIndustry": "Food",
        "geolocationId": "GEO-FACTORY-1",
    }
    assert sdk.complex_management.get_complex_geolocation(address, COMPLEX_ID) == {
        "latitude": "-23.5505", "longitude": "-46.6333", "additionalInfo": "Main plant",
    }

    sdk.complex_management.update_complex(address, COMPLEX_ID, dict(COMPLEX, complexName="Renamed Factory"))
    assert sdk.complex_management.get_complex(address, COMPLEX_ID)["complexName"] == "Renamed Factory"

    sdk.complex_management.remove_complex(address, COMPLEX_ID)
    assert not sdk.complex_management.complex_exists(address, COMPLEX_ID)


def test_product_passport(sdk, system, product):
    address = system["product_passport"]
    assert sdk.product_passport.product_exists(address, PRODUCT_ID)

    details = sdk.product_passport.get_product_details(address, PRODUCT_ID)
    assert details["product"] == PRODUCT
    assert details["origin"] == {"latitude": "-23.5505", "longitude": "-46.6333", "additionalInfo": "Main plant"}

    updated = {key: value for key, value in PRODUCT.items() if key != "complexId"}
    updated["description"] = "Brigadeiro Gourmet"
    sdk.product_passport.update_product(address, PRODUCT_ID, updated)
    assert sdk.product_passport.get_product_details(address, PRODUCT_ID)["product"]["description"] == "Brigadeiro Gourmet"

    sdk.product_passport.remove_product(address, PRODUCT_ID)
    assert not sdk.product_passport.product_exists(address, PRODUCT_ID)


def test_create_product_requires_existing_complex(sdk, system):
    with pytest.raises(REVERTED, match="Complex does not exist"):
        sdk.product_passport.create_product(system["product_passport"], PRODUCT_ID, PRODUCT)


def test_create_product_requires_all_fields(sdk, system):
    with pytest.raises(ValueError, match="complexId"):
        sdk.product_passport.create_product(
            system["product_passport"], PRODUCT_ID, {key: value for key, value in PRODUCT.items() if key != "complexId"}
        )


def test_batch(sdk, system, product):
    address = system["batch"]
    sdk.batch.create_batch(address, {
        "batchId": BATCH_ID,
        "amount": 100,
        "assemblingTime": 1687262400,
        "transportDetails": "Shipped via Express",
        "productId": PRODUCT_ID,
    })

    assert sdk.batch.owner_of(address, BATCH_ID) == sdk.account.address
    assert sdk.batch.get_batch(address, BATCH_ID) == {
        "amount": 100,
        "assemblingTime": 1687262400,
        "transportDetails": "Shipped via Express",
        "currentGeolocationId": "GEO-FACTORY-1",
        "originGeolocationId": "GEO-FACTORY-1",
    }

    # Geolocation is owned by ComplexManagement, so a batch can only move to an existing location
    warehouse = dict(COMPLEX, geolocationId="GEO-WAREHOUSE", latitude="51.5074", longitude="-0.1278", additionalInfo="London")
    sdk.complex_management.add_complex(system["complex_management"], "WAREHOUSE-1", warehouse)
    sdk.batch.update_batch_location(address, BATCH_ID, "GEO-WAREHOUSE")

    details = sdk.batch.get_batch_details(address, BATCH_ID, PRODUCT_ID)
    assert details["batch"]["currentGeolocationId"] == "GEO-WAREHOUSE"
    assert details["product"] == PRODUCT
    assert details["complex"]["complexName"] == "Sweet Delights Factory"
    assert details["currentLocation"]["additionalInfo"] == "London"
    assert details["originLocation"]["additionalInfo"] == "Main plant"

    sdk.batch.set_token_uri(address, BATCH_ID, "ipfs://QmMetadata")
    assert sdk.batch.token_uri(address, BATCH_ID) == "ipfs://QmMetadata"


def test_batch_cannot_create_new_geolocation_without_owning_it(sdk, system, product):
    address = system["batch"]
    sdk.batch.create_batch(address, {
        "batchId": BATCH_ID, "amount": 1, "assemblingTime": 0, "transportDetails": "", "productId": PRODUCT_ID,
    })
    with pytest.raises(REVERTED):
        sdk.batch.update_batch_location(address, BATCH_ID, "GEO-NEW", "1.0", "2.0", "Nowhere")
