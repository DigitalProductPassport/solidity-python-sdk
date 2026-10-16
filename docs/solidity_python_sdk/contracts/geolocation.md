# Geolocation Module Documentation

## Overview

The `Geolocation` class provides an interface for interacting with the `Geolocation` smart contract, which stores locations (latitude, longitude and additional info) under a string ID.

All write methods are `onlyOwner`. When the contracts are deployed with `sdk.deploy_system()`, `ComplexManagement` owns `Geolocation`, so new locations are created through `ComplexManagement.add_complex`.

## Class: `Geolocation`

### Common Methods

Every contract class shares these methods from `BaseContract`:

- **`deploy(initial_owner=None)`**: Deploys the contract and returns its address. The owner defaults to the SDK account.
- **`owner(contract_address)`**: Returns the address of the contract owner.
- **`transfer_ownership(contract_address, new_owner)`**: Transfers ownership of the contract.

Write methods return the transaction receipt and raise `TransactionFailedError` if the transaction fails. Read methods return Solidity structs as dicts keyed by their field names.

### Methods

#### `set_geolocation(self, contract_address, geolocation_id, latitude, longitude, additional_info="")`

Stores a geolocation under `geolocation_id`, overwriting any existing one.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `Geolocation` contract.
  - `geolocation_id` (`str`): The unique identifier for the geolocation.
  - `latitude` (`str`): The latitude, at most 20 characters.
  - `longitude` (`str`): The longitude, at most 20 characters.
  - `additional_info` (`str`, optional): Free-form information about the location.

#### `update_geolocation(self, contract_address, geolocation_id, latitude, longitude, additional_info="")`

Updates an existing geolocation.

#### `remove_geolocation(self, contract_address, geolocation_id)`

Removes an existing geolocation.

#### `get_geolocation(self, contract_address, geolocation_id)`

- **Returns**:
  - `dict`: `{"latitude", "longitude", "additionalInfo"}`. Unknown IDs return empty strings.

#### `geolocation_exists(self, contract_address, geolocation_id)`

- **Returns**:
  - `bool`: Whether a geolocation is stored under `geolocation_id`.

## Example Usage

```python
from solidity_python_sdk import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()

# A standalone Geolocation contract owned by the SDK account
contract_address = sdk.geolocation.deploy()
sdk.geolocation.set_geolocation(contract_address, "GEO-NYC", "40.7128", "-74.0060", "New York City")

print(sdk.geolocation.get_geolocation(contract_address, "GEO-NYC"))
# {'latitude': '40.7128', 'longitude': '-74.0060', 'additionalInfo': 'New York City'}
```
