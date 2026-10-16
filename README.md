# Solidity Python SDK

## Overview

The **Solidity Python SDK** is a Python library designed for interacting with Digital Product Passport smart contracts. It provides an easy-to-use interface for deploying and interacting with smart contracts on the Ethereum blockchain.

[Read about the project](https://www.web3digitalproductpassport.com/)

## Features

- **Deploy the full system**: Deploy and link all Digital Product Passport contracts with one call.
- **Production sites**: Register complexes (factories, warehouses) and their geolocations.
- **Product passports**: Create, update, remove and read product data, including its origin.
- **Batch NFTs**: Mint an ERC-721 token per production batch and track where it is.
- **Support for IPFS**: Integrate with IPFS for storing and retrieving product-related documents.

The SDK targets the contracts in [DigitalProductPassport/SmartContracts](https://github.com/DigitalProductPassport/SmartContracts):

| Contract | SDK attribute | Purpose |
| --- | --- | --- |
| `Geolocation` | `sdk.geolocation` | Stores locations (latitude, longitude, additional info) under a string ID. |
| `ComplexManagement` | `sdk.complex_management` | Registers production sites and links each to a geolocation. |
| `ProductPassport` | `sdk.product_passport` | Stores product data. Every product references the complex where it was made. |
| `IntegratedProductPassportBatch` | `sdk.batch` | Mints an ERC-721 token (`DPP`) per batch and tracks its origin and current location. |

## Installation

To install the SDK, you can use pip:

```bash
pip install -i https://test.pypi.org/simple/ solidity-python-sdk
```

or 

```bash
pip install solidity-python-sdk
```

## Usage

Here's a quick start guide to help you get started with the SDK.

### Basic Usage

The SDK reads `PROVIDER_URL` and `PRIVATE_KEY` from the environment (or a `.env` file), or you can pass them in:

```python
from solidity_python_sdk.main import DigitalProductPassportSDK

sdk = DigitalProductPassportSDK()
```

### Deploy the Contracts

`deploy_system` deploys all four contracts, links them together, and transfers ownership of `Geolocation` to `ComplexManagement`:

```python
addresses = sdk.deploy_system()
print(addresses)
# {'geolocation': '0x...', 'complex_management': '0x...', 'product_passport': '0x...', 'batch': '0x...'}
```

Each wrapper also has its own `deploy(initial_owner=None)` if you want to deploy and link the contracts yourself.

### Register a Complex

Every product must come from a registered complex. Adding a complex also stores its geolocation:

```python
sdk.complex_management.add_complex(addresses["complex_management"], "FACTORY-1", {
    "complexName": "Sweet Delights Factory",
    "complexCountry": "Brazil",
    "complexAddress": "Rua das Flores 100, Sao Paulo",
    "geolocationId": "GEO-FACTORY-1",
    "complexSiteType": "Manufacturing",
    "complexIndustry": "Food",
    "latitude": "-23.5505",
    "longitude": "-46.6333",
    "additionalInfo": "Main plant",  # optional
})
```

### Create a Product

```python
sdk.product_passport.create_product(addresses["product_passport"], 1, {
    "description": "Brigadeiro",
    "manuals": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "specifications": ["QmbnzbFDcmtJhyw5XTLkcnkJMhW86YZg6oc3FsNBeN2r4W"],
    "batchNumber": "BRG-2023-001",
    "productionDate": "2023-06-20",
    "expiryDate": "2023-12-31",
    "certifications": "FDA-5678",
    "warrantyInfo": "Not applicable",
    "materialComposition": ["0xMaterialPassportAddress"],  # at least one address
    "complexId": "FACTORY-1",
})
```

`update_product` takes the same fields except `complexId`. `remove_product` and `product_exists` are also available.

### Get Product Details

```python
details = sdk.product_passport.get_product_details(addresses["product_passport"], 1)
print(details["product"]["description"])  # Brigadeiro
print(details["origin"])  # {'latitude': '-23.5505', 'longitude': '-46.6333', 'additionalInfo': 'Main plant'}
```

Contract structs are returned as dicts keyed by their Solidity field names.

### Create and Track a Batch

Creating a batch mints an NFT with the batch ID as the token ID. The batch starts at its product's complex:

```python
sdk.batch.create_batch(addresses["batch"], {
    "batchId": 1,
    "amount": 100,
    "assemblingTime": 1687262400,  # UNIX timestamp
    "transportDetails": "Shipped via Express",
    "productId": 1,
})

sdk.batch.update_batch_location(addresses["batch"], 1, "GEO-WAREHOUSE-1")
sdk.batch.set_token_uri(addresses["batch"], 1, "ipfs://QmMetadata")

details = sdk.batch.get_batch_details(addresses["batch"], 1, 1)
# {'batch': {...}, 'product': {...}, 'complex': {...}, 'currentLocation': {...}, 'originLocation': {...}}
```

> **Note:** With `deploy_system`, `ComplexManagement` owns `Geolocation`, so `update_batch_location` can only move a batch to a geolocation that already exists, for example one created by registering a warehouse with `add_complex`. Moving to a new geolocation reverts. This is a [known limitation](https://github.com/DigitalProductPassport/SmartContracts#project-status) of the contracts.

### Upgrading from 0.1.x

Version 0.2.0 follows the new contracts and is not backward compatible:

- `authorize_entity`, `set_product`/`get_product` and `set_product_data`/`get_product_data` were removed. Use `create_product`, `update_product` and `get_product_details`.
- Products need a `complexId`, and `materialComposition` is now a list of addresses. `complianceInfo` was removed.
- `Batch` wraps `IntegratedProductPassportBatch`. `deploy()` no longer takes a ProductPassport address (call `initialize_contracts`), and batches reference a `productId` instead of an `ipfsHash`.
- `Geolocation.set_geolocation` takes a string geolocation ID and an optional `additional_info`.

## Running the Tests

The tests run against an in-memory chain, so they don't need a provider or funded account:

```bash
pip install -e ".[test]"
pytest
```

## Documentation

The documentation for the SDK is available in the `docs` directory. You can view the documentation in Markdown format or convert it to other formats if needed.

## Contributing

We welcome contributions to improve the SDK! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your changes.
3. Make your changes and write tests.
4. Submit a pull request with a clear description of your changes.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Contact

For any questions or support, please contact:

- **Author**: Luthiano Trarbach
- **Email**: luthiano.trarbach@proton.me
