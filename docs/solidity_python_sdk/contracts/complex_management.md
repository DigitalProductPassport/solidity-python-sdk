# ComplexManagement Module Documentation

## Overview

The `ComplexManagement` class provides an interface for interacting with the `ComplexManagement` smart contract, which registers production sites ("complexes") and links each one to a geolocation. Every product passport must reference an existing complex.

## Class: `ComplexManagement`

### Common Methods

Every contract class shares these methods from `BaseContract`:

- **`deploy(initial_owner=None)`**: Deploys the contract and returns its address. The owner defaults to the SDK account.
- **`owner(contract_address)`**: Returns the address of the contract owner.
- **`transfer_ownership(contract_address, new_owner)`**: Transfers ownership of the contract.

Write methods return the transaction receipt and raise `TransactionFailedError` if the transaction fails. Read methods return Solidity structs as dicts keyed by their field names.

### Methods

#### `set_geolocation_contract(self, contract_address, geolocation_address)`

Links the `Geolocation` contract used to store complex locations.

#### `add_complex(self, contract_address, complex_id, complex_data)`

Registers a new complex and stores its geolocation in the `Geolocation` contract. `ComplexManagement` must own the `Geolocation` contract.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ComplexManagement` contract.
  - `complex_id` (`str`): The unique identifier for the complex.
  - `complex_data` (`dict`): A dictionary with the keys `complexName`, `complexCountry`, `complexAddress`, `geolocationId`, `complexSiteType`, `complexIndustry`, `latitude`, `longitude` and, optionally, `additionalInfo`.

#### `update_complex(self, contract_address, complex_id, complex_data)`

Updates an existing complex. Its geolocation is not changed.

- **Args**:
  - `complex_data` (`dict`): A dictionary with the keys `complexName`, `complexCountry`, `complexAddress`, `complexSiteType` and `complexIndustry`.

#### `remove_complex(self, contract_address, complex_id)`

Removes an existing complex.

#### `get_complex(self, contract_address, complex_id)`

- **Returns**:
  - `dict`: `{"complexName", "complexCountry", "complexAddress", "complexSiteType", "complexIndustry", "geolocationId"}`.

#### `get_complex_geolocation(self, contract_address, complex_id)`

- **Returns**:
  - `dict`: The complex's geolocation, `{"latitude", "longitude", "additionalInfo"}`.

#### `complex_exists(self, contract_address, complex_id)`

- **Returns**:
  - `bool`: Whether a complex is registered under `complex_id`.

#### `geolocation_contract(self, contract_address)`

- **Returns**:
  - `str`: The address of the linked `Geolocation` contract.

## Example Usage

```python
from solidity_python_sdk import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()
addresses = sdk.deploy_system()

sdk.complex_management.add_complex(addresses["complex_management"], "FACTORY-1", {
    "complexName": "Sweet Delights Factory",
    "complexCountry": "Brazil",
    "complexAddress": "Rua das Flores 100, Sao Paulo",
    "geolocationId": "GEO-FACTORY-1",
    "complexSiteType": "Manufacturing",
    "complexIndustry": "Food",
    "latitude": "-23.5505",
    "longitude": "-46.6333",
    "additionalInfo": "Main plant"
})

print(sdk.complex_management.get_complex_geolocation(addresses["complex_management"], "FACTORY-1"))
```
