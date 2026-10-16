from solidity_python_sdk.contracts.base import BaseContract


class Geolocation(BaseContract):
    """
    Interface for interacting with the Geolocation smart contract, which stores
    locations (latitude, longitude, additional info) under a string ID.

    Writes are ``onlyOwner``. When the contracts are wired with
    ``DigitalProductPassportSDK.deploy_system``, ComplexManagement owns Geolocation,
    so new locations are created through ``ComplexManagement.add_complex``.
    """

    CONTRACT_NAME = "Geolocation"

    def set_geolocation(self, contract_address, geolocation_id, latitude, longitude, additional_info=""):
        """
        Stores a geolocation under ``geolocation_id``, overwriting any existing one.

        Args:
            contract_address (str): The address of the deployed Geolocation contract.
            geolocation_id (str): The unique identifier for the geolocation.
            latitude (str): The latitude, at most 20 characters.
            longitude (str): The longitude, at most 20 characters.
            additional_info (str, optional): Free-form information about the location.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "setGeolocation", geolocation_id, latitude, longitude, additional_info)

    def update_geolocation(self, contract_address, geolocation_id, latitude, longitude, additional_info=""):
        """
        Updates an existing geolocation.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "updateGeolocation", geolocation_id, latitude, longitude, additional_info)

    def remove_geolocation(self, contract_address, geolocation_id):
        """
        Removes an existing geolocation.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "removeGeolocation", geolocation_id)

    def get_geolocation(self, contract_address, geolocation_id):
        """
        Retrieves a geolocation. Unknown IDs return empty strings.

        Returns:
            dict: ``{"latitude", "longitude", "additionalInfo"}``.
        """
        return self._call(contract_address, "getGeolocation", geolocation_id)

    def geolocation_exists(self, contract_address, geolocation_id):
        """
        Returns:
            bool: Whether a geolocation is stored under ``geolocation_id``.
        """
        return self._call(contract_address, "geolocationExists", geolocation_id)
