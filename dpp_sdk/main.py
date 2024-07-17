import json
import os
from web3 import Web3
from dotenv import load_dotenv
from dpp_sdk.resources import ABI

class DigitalProductPassportSDK:
    """
    SDK for interacting with Digital Product Passport smart contracts.

    Attributes:
        web3 (Web3): Instance of Web3 for interacting with Ethereum blockchain.
        account (LocalAccount): Account instance for signing transactions.
        product_passport_contract (dict): ABI and bytecode for the Product Passport contract.
        batch_contract (dict): ABI and bytecode for the Batch contract.
    """

    def __init__(self, provider_url=None, private_key=None):
        """
        Initialize the SDK with optional provider URL and private key.

        Args:
            provider_url (str, optional): Ethereum provider URL.
            private_key (str, optional): Private key for the Ethereum account.

        Raises:
            ValueError: If private key is not provided.
        """
        if provider_url and private_key:
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
            self.account = self.web3.eth.account.from_key(private_key)
        else:
            load_dotenv()
            provider_url = os.getenv("PROVIDER_URL")
            private_key = os.getenv("PRIVATE_KEY")
            self.web3 = Web3(Web3.HTTPProvider(provider_url))
            self.account = self.web3.eth.account.from_key(private_key)
        if private_key is None:
            raise ValueError("Private key must be provided.")
        
        self.product_passport_contract = self.load_contract("ProductPassport.sol/ProductPassport.json")
        self.batch_contract = self.load_contract("Batch.sol/Batch.json")

    def load_contract(self, contract_path):
        """
        Load the contract's ABI and bytecode from the local JSON file.

        Args:
            contract_path (str): Path to the contract JSON file.

        Returns:
            dict: Loaded contract containing ABI and bytecode.
        """
        ABI_PATH = os.path.join(os.path.dirname(ABI.__file__), contract_path)
        with open(ABI_PATH) as file:
            contract_interface = json.load(file)
        return {
            "abi": contract_interface['abi'],
            "bytecode": contract_interface['bytecode']
        }

    def deploy_contract(self, contract):
        """
        Deploy a smart contract to the blockchain.

        Args:
            contract (dict): Contract containing ABI and bytecode.

        Returns:
            str: Address of the deployed contract.
        """
        Greeter = self.web3.eth.contract(abi=contract['abi'], bytecode=contract['bytecode'])
        tx_hash = Greeter.constructor().transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt.contractAddress

    def create_product_passport(self, contract_address, product_details):
        """
        Create a new product passport on the blockchain.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_details (dict): Details of the product.

        Returns:
            dict: Transaction receipt of the product passport creation.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        tx_hash = contract.functions.createProductPassport(
            product_details["productId"],
            product_details["description"],
            product_details["manuals"],
            product_details["specifications"],
            product_details["batchNumber"],
            product_details["productionDate"],
            product_details["expiryDate"],
            product_details["certifications"],
            product_details["warrantyInfo"],
            product_details["materialComposition"],
            product_details["complianceInfo"],
            product_details["ipfs"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def interact_with_existing_contract(self, contract_address, product_id):
        """
        Interact with an existing product passport contract.

        Args:
            contract_address (str): Address of the Product Passport contract.
            product_id (int): ID of the product.

        Returns:
            dict: Product passport details.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.product_passport_contract['abi'])
        product_passport = contract.functions.getProductPassport(product_id).call()
        return product_passport

    def create_batch(self, contract_address, batch_details):
        """
        Create a new batch on the blockchain.

        Args:
            contract_address (str): Address of the Batch contract.
            batch_details (dict): Details of the batch.

        Returns:
            dict: Transaction receipt of the batch creation.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.batch_contract['abi'])
        tx_hash = contract.functions.createBatch(
            batch_details["batchId"],
            batch_details["batchNumber"],
            batch_details["productionDate"],
            batch_details["expiryDate"],
            batch_details["quantity"]
        ).transact({'from': self.account.address})
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash)
        return tx_receipt

    def interact_with_existing_batch(self, contract_address, batch_id):
        """
        Interact with an existing batch contract.

        Args:
            contract_address (str): Address of the Batch contract.
            batch_id (int): ID of the batch.

        Returns:
            dict: Batch details.
        """
        contract = self.web3.eth.contract(address=contract_address, abi=self.batch_contract['abi'])
        batch_details = contract.functions.getBatch(batch_id).call()
        return batch_details