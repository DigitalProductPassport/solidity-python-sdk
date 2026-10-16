import logging
import json
from web3 import Web3
from dotenv import load_dotenv
import os
from eth_account import Account
from solidity_python_sdk.contracts.product_passport import ProductPassport
from solidity_python_sdk.contracts.geolocation import Geolocation
from solidity_python_sdk.contracts.complex_management import ComplexManagement
from solidity_python_sdk.contracts.batch import Batch
from solidity_python_sdk.resources import ABI
from solidity_python_sdk.utils.pinata_utils import PinataUtility

class DigitalProductPassportSDK:
    """
    SDK for interacting with Digital Product Passport smart contracts.
    """

    def __init__(self, provider_url=None, private_key=None, gas=254362, gwei_bid=3, pinata_api_key=None, pinata_secret_key=None, web3=None):
        """
        Initializes the SDK with a provider URL and private key.

        Args:
            web3 (Web3, optional): A ready-made Web3 instance to use instead of
                connecting to ``provider_url``, for example a local test chain.
        """
        logging.basicConfig(level=logging.DEBUG)
        load_dotenv()
        provider_url = provider_url or os.getenv("PROVIDER_URL")
        private_key = private_key or os.getenv("PRIVATE_KEY")
        pinata_api_key = pinata_api_key or os.getenv("PINATA_API_KEY")
        pinata_secret_key = pinata_secret_key or os.getenv("PINATA_API_SECRET")

        if not private_key:
            raise ValueError("Private key must be provided.")

        self.web3 = web3 or Web3(Web3.HTTPProvider(provider_url))
        self.account = self.web3.eth.account.from_key(private_key)
        self.gas = gas
        self.gwei_bid = gwei_bid
        self.contracts = self.load_all_contracts()

        if pinata_api_key and pinata_secret_key:
            self.pinata_utility = PinataUtility(pinata_api_key, pinata_secret_key)
        self.product_passport = ProductPassport(self)
        self.batch = Batch(self)
        self.geolocation = Geolocation(self)
        self.complex_management = ComplexManagement(self)

        logging.info("DigitalProductPassportSDK initialized successfully.")

    def load_all_contracts(self):
        contracts = {}
        abi_folder_path = os.path.dirname(ABI.__file__)
        for filename in os.listdir(abi_folder_path):
            file_path = os.path.join(abi_folder_path, filename)
            if os.path.isdir(file_path) and filename.endswith('.sol'):
                # A source file can hold contracts with other names, e.g.
                # ExtendedProductPassport.sol/IntegratedProductPassportBatch.json
                for artifact in os.listdir(file_path):
                    if artifact.endswith('.json') and not artifact.endswith('.dbg.json'):
                        contract_name = os.path.splitext(artifact)[0]
                        contracts[contract_name] = self.load_contract(os.path.join(file_path, artifact))
        return contracts

    def load_contract(self, contract_path):
        with open(contract_path) as file:
            contract_interface = json.load(file)
        return {
            "abi": contract_interface['abi'],
            "bytecode": contract_interface['bytecode']
        }

    def deploy_system(self):
        """
        Deploys Geolocation, ComplexManagement, ProductPassport and
        IntegratedProductPassportBatch, owned by the SDK account, and links them the
        same way as the smart contracts' Ignition module. Ownership of Geolocation is
        transferred to ComplexManagement, because ``add_complex`` writes geolocations.

        Returns:
            dict: The deployed addresses, keyed by "geolocation", "complex_management",
            "product_passport" and "batch".
        """
        addresses = {
            "geolocation": self.geolocation.deploy(),
            "complex_management": self.complex_management.deploy(),
            "product_passport": self.product_passport.deploy(),
            "batch": self.batch.deploy(),
        }
        self.complex_management.set_geolocation_contract(addresses["complex_management"], addresses["geolocation"])
        self.product_passport.set_complex_management(addresses["product_passport"], addresses["complex_management"])
        self.batch.initialize_contracts(
            addresses["batch"], addresses["product_passport"], addresses["complex_management"], addresses["geolocation"]
        )
        self.geolocation.transfer_ownership(addresses["geolocation"], addresses["complex_management"])
        logging.info(f"Digital Product Passport system deployed: {addresses}")
        return addresses
    
    def add_documents_from_config(self, config_path):
        pinned_data = self.pinata_utility.pin_files_from_config(config_path)
        passport_data = self.create_passport_json(pinned_data)
        return self.pinata_utility.pin_json(passport_data)

    def create_passport_json(self, pinned_data):
        passport_json = {
            "description": pinned_data.get("description", ""),
            "manuals": pinned_data.get("manuals", []),
            "specifications": pinned_data.get("specifications", []),
            "batchNumber": pinned_data.get("batchNumber", ""),
            "productionDate": pinned_data.get("productionDate", ""),
            "expiryDate": pinned_data.get("expiryDate", ""),
            "certifications": pinned_data.get("certifications", ""),
            "warrantyInfo": pinned_data.get("warrantyInfo", ""),
            "materialComposition": pinned_data.get("materialComposition", ""),
            "complianceInfo": pinned_data.get("complianceInfo", "")
        }
        return passport_json
