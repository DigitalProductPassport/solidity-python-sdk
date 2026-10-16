# Digital Product Passport Demo

This project demonstrates the usage of the `DigitalProductPassportSDK` for managing digital product passports using a web interface built with `NiceGUI`. The demo allows users to input contract addresses and retrieve detailed information about products and batches.

## Prerequisites to run localy

- Python 3.7+
- Web3.py
- NiceGUI
- Solidity Python SDK
- Pinata API keys and secrets
- Pinata Gateway
- Private keys
- Provider

## Installation

1. Clone the repository:

    ```bash
    git clone https://github.com/DigitalProductPassport/solidity-python-sdk.git
    ```

2. Install the required packages:

    ```bash
    pip install nicegui web3 solidity-python-sdk
    ```

3. Set up environment variables for Pinata:

    ```bash
    export PINATA_GATEWAY_TOKEN=your_pinata_gateway_token
    export PINATA_GATEWAY_URL=your_pinata_gateway_url
    export PROVIDER_URL=the_provider_rpc
    export PRIVATE_KEY=your_private_key
    ```

## Deploying Demo Contracts

The demo reads from deployed contracts. To deploy them, register a factory and five distribution centers, create a product, and ship five batches, run:

```bash
python deploy.py
```

It prints the ProductPassport and Batch contract addresses to use in the demo.

## Running the Demo

To start the demo application, run the following command:

```bash
python main.py
```

This will start a local web server. Open your browser and navigate to `http://localhost:8080` to view the demo.

You can also use docker-compose

```bash
docker-compose up
```

And use Elastic Beanstalk or Google Cloud run

```bash
eb init -p docker ddp-demo
eb setenv PINATA_GATEWAY_TOKEN=your_pinata_gateway_token PINATA_GATEWAY_URL=your_pinata_gateway_url \
PROVIDER_URL=the_provider_rpc  PRIVATE_KEY=your_private_key
eb deploy
```


## Features

- **Home Page**: Displays the title and logo.
- **Tabs**: Two tabs for "Product Information" and "Batch".
- **Product Information**:
  - Inputs for Product Contract Address and Product ID
  - Button to fetch product details
  - Displays product information including description, batch number, dates, certifications, warranty, material composition and complex
  - Displays the product's origin on a map, and its documents
- **Batch**:
  - Inputs for Batch Contract Address, Batch ID and Product ID
  - Button to fetch batch details
  - Displays batch information including Quantity, Assembling Time, Transport Details, product and complex
  - Displays the batch's origin and current location on a map


## How to use

### Product Information

You can click on Product information tab, and then add the contract address for the product passport and the product ID on the text inputs.
Use the ProductPassport address printed by `deploy.py` and product ID 1.
![](https://github.com/DigitalProductPassport/solidity-python-sdk/blob/main/examples/passport_details/images/product_details.gif)

### Batch Information

You can click on Batch tab, and then add the contract address for the Batch, the batch ID and the product ID on the text inputs.
Use the Batch address printed by `deploy.py`, a batch ID from 1 to 5, and product ID 1.
![](https://github.com/DigitalProductPassport/solidity-python-sdk/blob/main/examples/passport_details/images/batch.gif)


## Code Overview

### `index()`

Defines the home page layout with title, logo, tabs, and input fields for contract addresses.

### `get_product_details(product_contract_address, product_id)`

Fetches and displays product details and origin based on the provided contract address and product ID.

### `get_batch_details(batch_contract_address, batch_id, product_id)`

Fetches and displays batch details based on the provided contract address, batch ID and product ID.

### `plot_geolocations(geolocations)`

Plots a list of geolocations (origin, current location) on a map using Leaflet.

### `get_pinata_url(ipfs_hash)`

Generates a URL for Pinata-hosted IPFS content.

### `plot_product_specifications(product)`

Displays product specifications in a grid layout.

### `plot_product_documents(product)`

Displays product documents (manuals and specifications) using embedded PDF viewers.

