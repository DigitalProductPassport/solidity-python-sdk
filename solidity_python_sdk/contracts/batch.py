from solidity_python_sdk.contracts.base import BaseContract, args_from

CREATE_BATCH_FIELDS = ["batchId", "amount", "assemblingTime", "transportDetails", "productId"]


class Batch(BaseContract):
    """
    Interface for interacting with the IntegratedProductPassportBatch smart contract,
    which mints an ERC-721 token (DPP) for each production batch and tracks its
    origin and current location.
    """

    CONTRACT_NAME = "IntegratedProductPassportBatch"

    def initialize_contracts(self, contract_address, product_passport_address, complex_management_address, geolocation_address):
        """
        Links the ProductPassport, ComplexManagement and Geolocation contracts.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(
            contract_address, "initializeContracts",
            product_passport_address, complex_management_address, geolocation_address
        )

    def create_batch(self, contract_address, batch_details):
        """
        Creates a batch for an existing product and mints its NFT to the contract owner.
        The batch's origin and current location are set to the product's complex.

        Args:
            contract_address (str): The address of the deployed batch contract.
            batch_details (dict): A dictionary with the keys:
                "batchId" (int): The unique identifier for the batch, also the NFT token ID.
                "amount" (int): The quantity of items in the batch, greater than zero.
                "assemblingTime" (int): The UNIX timestamp of the assembling time.
                "transportDetails" (str): Details about the transport.
                "productId" (int): The product the batch belongs to.

        Returns:
            dict: The transaction receipt.
        """
        batch_id, amount, assembling_time, transport_details, product_id = args_from(batch_details, CREATE_BATCH_FIELDS)
        return self._transact(
            contract_address, "createBatch",
            int(batch_id), int(amount), int(assembling_time), transport_details, int(product_id)
        )

    def update_batch_location(self, contract_address, batch_id, geolocation_id, latitude="", longitude="", additional_info=""):
        """
        Moves a batch to ``geolocation_id``. If the geolocation does not exist, it is
        created from ``latitude``, ``longitude`` and ``additional_info``, which requires
        the batch contract to own the Geolocation contract.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(
            contract_address, "updateBatchLocation",
            int(batch_id), geolocation_id, latitude, longitude, additional_info
        )

    def get_batch(self, contract_address, batch_id):
        """
        Retrieves the stored batch record.

        Returns:
            dict: ``{"amount", "assemblingTime", "transportDetails", "currentGeolocationId",
            "originGeolocationId"}``. Unknown batches have an amount of 0.
        """
        return self._call(contract_address, "batches", int(batch_id))

    def get_batch_details(self, contract_address, batch_id, product_id):
        """
        Retrieves a batch together with its product, complex and locations.

        Returns:
            dict: ``{"batch", "product", "complex", "currentLocation", "originLocation"}``.
        """
        return self._call(contract_address, "getBatchDetails", int(batch_id), int(product_id))

    def set_token_uri(self, contract_address, batch_id, token_uri):
        """
        Links a batch NFT to off-chain metadata, for example an IPFS JSON file.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "setTokenURI", int(batch_id), token_uri)

    def token_uri(self, contract_address, batch_id):
        """
        Returns:
            str: The metadata URI of the batch NFT.
        """
        return self._call(contract_address, "tokenURI", int(batch_id))

    def owner_of(self, contract_address, batch_id):
        """
        Returns:
            str: The address that holds the batch NFT.
        """
        return self._call(contract_address, "ownerOf", int(batch_id))
