from solidity_python_sdk.contracts.base import BaseContract, args_from

ADD_COMPLEX_FIELDS = [
    "complexName", "complexCountry", "complexAddress", "geolocationId",
    "complexSiteType", "complexIndustry", "latitude", "longitude",
]
UPDATE_COMPLEX_FIELDS = [
    "complexName", "complexCountry", "complexAddress", "complexSiteType", "complexIndustry",
]


class ComplexManagement(BaseContract):
    """
    Interface for interacting with the ComplexManagement smart contract, which
    registers production sites ("complexes") and links each one to a geolocation.
    """

    CONTRACT_NAME = "ComplexManagement"

    def set_geolocation_contract(self, contract_address, geolocation_address):
        """
        Links the Geolocation contract used to store complex locations.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "setGeolocationContract", geolocation_address)

    def add_complex(self, contract_address, complex_id, complex_data):
        """
        Registers a new complex and stores its geolocation in the Geolocation contract.
        ComplexManagement must own the Geolocation contract.

        Args:
            contract_address (str): The address of the deployed ComplexManagement contract.
            complex_id (str): The unique identifier for the complex.
            complex_data (dict): A dictionary with the keys "complexName", "complexCountry",
                "complexAddress", "geolocationId", "complexSiteType", "complexIndustry",
                "latitude", "longitude" and, optionally, "additionalInfo".

        Returns:
            dict: The transaction receipt.
        """
        args = args_from(complex_data, ADD_COMPLEX_FIELDS) + [complex_data.get("additionalInfo", "")]
        return self._transact(contract_address, "addComplex", complex_id, *args)

    def update_complex(self, contract_address, complex_id, complex_data):
        """
        Updates an existing complex. Its geolocation is not changed.

        Args:
            complex_data (dict): A dictionary with the keys "complexName", "complexCountry",
                "complexAddress", "complexSiteType" and "complexIndustry".

        Returns:
            dict: The transaction receipt.
        """
        args = args_from(complex_data, UPDATE_COMPLEX_FIELDS)
        return self._transact(contract_address, "updateComplex", complex_id, *args)

    def remove_complex(self, contract_address, complex_id):
        """
        Removes an existing complex.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "removeComplex", complex_id)

    def get_complex(self, contract_address, complex_id):
        """
        Returns:
            dict: ``{"complexName", "complexCountry", "complexAddress", "complexSiteType",
            "complexIndustry", "geolocationId"}``.
        """
        return self._call(contract_address, "getComplex", complex_id)

    def get_complex_geolocation(self, contract_address, complex_id):
        """
        Returns:
            dict: The complex's geolocation, ``{"latitude", "longitude", "additionalInfo"}``.
        """
        return self._call(contract_address, "getComplexGeolocation", complex_id)

    def complex_exists(self, contract_address, complex_id):
        """
        Returns:
            bool: Whether a complex is registered under ``complex_id``.
        """
        return self._call(contract_address, "complexExists", complex_id)

    def geolocation_contract(self, contract_address):
        """
        Returns:
            str: The address of the linked Geolocation contract.
        """
        return self._call(contract_address, "geolocationContract")
