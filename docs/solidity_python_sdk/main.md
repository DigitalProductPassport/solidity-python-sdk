# Digital Product Passport SDK Documentation

## Overview

The `DigitalProductPassportSDK` is a Python SDK designed for interacting with Digital Product Passport smart contracts on the Ethereum blockchain. This SDK provides an interface for managing and interacting with smart contracts related to digital product passports, including functionalities for product information, production sites (complexes), batch management, and geolocation.

[Read about the project](https://www.web3digitalproductpassport.com/)

## File Structure

The SDK is contained within the file `solidity_python_sdk/main.py`, which includes the following key components:

- **Initialization of the SDK**
- **Loading smart contracts**
- **Access to contract instances**
- **Deploying and linking the full contract system**

## Usage

### Importing the SDK

To use the SDK, import it as follows:

```python
from solidity_python_sdk import DigitalProductPassportSDK
```

### Initialization

Create an instance of `DigitalProductPassportSDK` with the necessary parameters:

```python
sdk = DigitalProductPassportSDK(
    provider_url="https://mainnet.infura.io/v3/YOUR_INFURA_PROJECT_ID",
    private_key="YOUR_PRIVATE_KEY",
    gas=254362,
    gwei_bid=3
)
```

- **provider_url**: URL of the Ethereum provider (e.g., Infura or Alchemy).
- **private_key**: Your Ethereum private key.
- **gas**: Gas limit for transactions (default: 254362).
- **gwei_bid**: Gas price bid in gwei (default: 3).
- **web3** (optional): A ready-made `Web3` instance to use instead of connecting to `provider_url`, for example a local test chain.

### Attributes

- **`sdk.product_passport`**: Instance of the `ProductPassport` contract.
- **`sdk.batch`**: Instance of the `Batch` class, for the `IntegratedProductPassportBatch` contract.
- **`sdk.geolocation`**: Instance of the `Geolocation` contract.
- **`sdk.complex_management`**: Instance of the `ComplexManagement` contract.

### Methods

#### `__init__(self, provider_url=None, private_key=None, gas=254362, gwei_bid=3, pinata_api_key=None, pinata_secret_key=None, web3=None)`

Initializes the SDK with the provided Ethereum provider URL and private key. It also sets up gas limit and gas price.

- **Parameters**:
  - `provider_url` (str): Ethereum provider URL.
  - `private_key` (str): Ethereum private key.
  - `gas` (int): Gas limit for transactions (default: 254362).
  - `gwei_bid` (int): Gas price bid in gwei (default: 3).
  - `pinata_api_key` (str): Pinata API key, for pinning documents to IPFS.
  - `pinata_secret_key` (str): Pinata API secret.
  - `web3` (Web3): A ready-made Web3 instance to use instead of `provider_url`.

#### `deploy_system(self)`

Deploys `Geolocation`, `ComplexManagement`, `ProductPassport` and `IntegratedProductPassportBatch`, owned by the SDK account, and links them together. Ownership of `Geolocation` is transferred to `ComplexManagement`, because `add_complex` writes geolocations.

- **Returns**:
  - `dict`: The deployed addresses, keyed by `geolocation`, `complex_management`, `product_passport` and `batch`.

#### `load_all_contracts(self)`

Loads all smart contracts from the ABI directory. Each `<Source>.sol` folder can contain several contracts, for example `ExtendedProductPassport.sol/IntegratedProductPassportBatch.json`.

- **Returns**:
  - `dict`: A dictionary of contract names and their respective ABI and bytecode.

#### `load_contract(self, contract_path)`

Loads a single smart contract from a specified path.

- **Parameters**:
  - `contract_path` (str): Path to the contract ABI file.
  
- **Returns**:
  - `dict`: Contains the ABI and bytecode of the contract.

## Environment Variables

The SDK uses environment variables for configuration. Create a `.env` file in your project directory with the following variables:

```dotenv
PROVIDER_URL=<your-ethereum-provider-url>
PRIVATE_KEY=<your-ethereum-private-key>
PINATA_API_KEY=<optional-pinata-api-key>
PINATA_API_SECRET=<optional-pinata-api-secret>
```

Replace `<your-ethereum-provider-url>` and `<your-ethereum-private-key>` with your actual provider URL and private key.

## Dependencies

Ensure you have the following Python packages installed:

- `web3`
- `python-dotenv`
- `solidity-python-sdk`

You can install them using:

```sh
pip install web3 python-dotenv solidity-python-sdk
```

## Contributing

Contributions are welcome! To contribute, follow these steps:

1. **Fork the repository**
2. **Create a new branch (`git checkout -b feature-branch`)**
3. **Commit your changes (`git commit -am 'Add new feature'`)**
4. **Push to the branch (`git push origin feature-branch`)**
5. **Create a Pull Request**


## Contact

For any questions or support, please contact:

- **Author**: Luthiano Trarbach
- **Email**: luthiano.trarbach@proton.me