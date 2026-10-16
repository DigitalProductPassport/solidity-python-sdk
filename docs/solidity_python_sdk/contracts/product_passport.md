# ProductPassport Module Documentation

## Overview

The `ProductPassport` class provides an interface for interacting with the `ProductPassport` smart contract, which stores product data. Every product references the complex where it was made, so its origin can be resolved on-chain.

## Class: `ProductPassport`

### Common Methods

Every contract class shares these methods from `BaseContract`:

- **`deploy(initial_owner=None)`**: Deploys the contract and returns its address. The owner defaults to the SDK account.
- **`owner(contract_address)`**: Returns the address of the contract owner.
- **`transfer_ownership(contract_address, new_owner)`**: Transfers ownership of the contract.

Write methods return the transaction receipt and raise `TransactionFailedError` if the transaction fails. Read methods return Solidity structs as dicts keyed by their field names.

### Methods

#### `set_complex_management(self, contract_address, complex_management_address)`

Links the `ComplexManagement` contract that products reference.

#### `create_product(self, contract_address, product_id, product_data)`

Creates a new product passport. The complex in `complexId` must exist.

- **Args**:
  - `contract_address` (`str`): The address of the deployed `ProductPassport` contract.
  - `product_id` (`int`): The unique identifier for the product.
  - `product_data` (`dict`): A dictionary with the keys:
    - `description` (`str`)
    - `manuals` (`list[str]`): For example IPFS hashes.
    - `specifications` (`list[str]`)
    - `batchNumber` (`str`)
    - `productionDate` (`str`)
    - `expiryDate` (`str`)
    - `certifications` (`str`)
    - `warrantyInfo` (`str`)
    - `materialComposition` (`list[str]`): Addresses of material passports. At least one is required, because the contract uses it to tell whether a product exists.
    - `complexId` (`str`)

#### `update_product(self, contract_address, product_id, product_data)`

Updates an existing product passport. Takes the same keys as `create_product` except `complexId`, which cannot be changed.

#### `remove_product(self, contract_address, product_id)`

Removes an existing product passport.

#### `get_product_details(self, contract_address, product_id)`

Retrieves a product and the geolocation of the complex where it was made.

- **Returns**:
  - `dict`: `{"product": {...}, "origin": {"latitude", "longitude", "additionalInfo"}}`, where `product` has the keys listed in `create_product`.

#### `product_exists(self, contract_address, product_id)`

- **Returns**:
  - `bool`: Whether a product exists under `product_id`.

#### `complex_management(self, contract_address)`

- **Returns**:
  - `str`: The address of the linked `ComplexManagement` contract.

## Example Usage

```python
from solidity_python_sdk import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()
addresses = sdk.deploy_system()
# Register the complex "FACTORY-1" first, see the ComplexManagement documentation

sdk.product_passport.create_product(addresses["product_passport"], 1, {
    "description": "Brigadeiro",
    "manuals": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "specifications": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    "materialComposition": ["0xMaterialPassportAddress"],
    "complexId": "FACTORY-1"
})

details = sdk.product_passport.get_product_details(addresses["product_passport"], 1)
print(details["product"]["description"], details["origin"])
```
