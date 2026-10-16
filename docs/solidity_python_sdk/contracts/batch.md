# Batch Module Documentation

## Overview

The `Batch` class provides an interface for interacting with the `IntegratedProductPassportBatch` smart contract. The contract mints an ERC-721 token (`DPP`) for each production batch, with the batch ID as the token ID, and tracks the batch's origin and current location.

## Class: `Batch`

### Common Methods

Every contract class shares these methods from `BaseContract`:

- **`deploy(initial_owner=None)`**: Deploys the contract and returns its address. The owner defaults to the SDK account.
- **`owner(contract_address)`**: Returns the address of the contract owner.
- **`transfer_ownership(contract_address, new_owner)`**: Transfers ownership of the contract.

Write methods return the transaction receipt and raise `TransactionFailedError` if the transaction fails. Read methods return Solidity structs as dicts keyed by their field names.

### Methods

#### `initialize_contracts(self, contract_address, product_passport_address, complex_management_address, geolocation_address)`

Links the `ProductPassport`, `ComplexManagement` and `Geolocation` contracts.

#### `create_batch(self, contract_address, batch_details)`

Creates a batch for an existing product and mints its NFT to the contract owner. The batch's origin and current location are set to the geolocation of the product's complex.

- **Args**:
  - `contract_address` (`str`): The address of the deployed batch contract.
  - `batch_details` (`dict`): A dictionary with the keys:
    - `batchId` (`int`): The unique identifier for the batch, also the NFT token ID.
    - `amount` (`int`): The quantity of items in the batch, greater than zero.
    - `assemblingTime` (`int`): The UNIX timestamp of the assembling time.
    - `transportDetails` (`str`): Details about the transport.
    - `productId` (`int`): The product the batch belongs to.

#### `update_batch_location(self, contract_address, batch_id, geolocation_id, latitude="", longitude="", additional_info="")`

Moves a batch to `geolocation_id`. If the geolocation does not exist, the contract tries to create it from `latitude`, `longitude` and `additional_info`. That requires the batch contract to own `Geolocation`, so with `sdk.deploy_system()` it reverts: register the location as a complex first.

#### `get_batch(self, contract_address, batch_id)`

- **Returns**:
  - `dict`: `{"amount", "assemblingTime", "transportDetails", "currentGeolocationId", "originGeolocationId"}`. Unknown batches have an amount of 0.

#### `get_batch_details(self, contract_address, batch_id, product_id)`

Retrieves a batch together with its product, complex and locations.

- **Returns**:
  - `dict`: `{"batch", "product", "complex", "currentLocation", "originLocation"}`.

#### `set_token_uri(self, contract_address, batch_id, token_uri)`

Links a batch NFT to off-chain metadata, for example an IPFS JSON file.

#### `token_uri(self, contract_address, batch_id)`

- **Returns**:
  - `str`: The metadata URI of the batch NFT.

#### `owner_of(self, contract_address, batch_id)`

- **Returns**:
  - `str`: The address that holds the batch NFT.

## Example Usage

```python
from solidity_python_sdk import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()
addresses = sdk.deploy_system()
# Register complexes and create product 1 first

sdk.batch.create_batch(addresses["batch"], {
    "batchId": 1,
    "amount": 100,
    "assemblingTime": 1687262400,
    "transportDetails": "Shipped via Express",
    "productId": 1
})
sdk.batch.update_batch_location(addresses["batch"], 1, "GEO-WAREHOUSE-1")

details = sdk.batch.get_batch_details(addresses["batch"], 1, 1)
print(details["originLocation"], details["currentLocation"])
```
