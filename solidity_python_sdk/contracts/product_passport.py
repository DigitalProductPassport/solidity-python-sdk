from solidity_python_sdk.contracts.base import BaseContract, args_from

UPDATE_PRODUCT_FIELDS = [
    "description", "manuals", "specifications", "batchNumber", "productionDate",
    "expiryDate", "certifications", "warrantyInfo", "materialComposition",
]
CREATE_PRODUCT_FIELDS = UPDATE_PRODUCT_FIELDS + ["complexId"]


class ProductPassport(BaseContract):
    """
    Interface for interacting with the ProductPassport smart contract, which stores
    product data. Every product references the complex where it was made.
    """

    CONTRACT_NAME = "ProductPassport"

    def set_complex_management(self, contract_address, complex_management_address):
        """
        Links the ComplexManagement contract that products reference.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "setComplexManagement", complex_management_address)

    def create_product(self, contract_address, product_id, product_data):
        """
        Creates a new product passport. The complex in "complexId" must exist.

        Args:
            contract_address (str): The address of the deployed ProductPassport contract.
            product_id (int): The unique identifier for the product.
            product_data (dict): A dictionary with the keys:
                "description" (str), "manuals" (list[str], e.g. IPFS hashes),
                "specifications" (list[str]), "batchNumber" (str), "productionDate" (str),
                "expiryDate" (str), "certifications" (str), "warrantyInfo" (str),
                "materialComposition" (list[str], addresses of material passports, at least one),
                "complexId" (str).

        Returns:
            dict: The transaction receipt.
        """
        args = args_from(product_data, CREATE_PRODUCT_FIELDS)
        return self._transact(contract_address, "createProduct", int(product_id), *args)

    def update_product(self, contract_address, product_id, product_data):
        """
        Updates an existing product passport. The complex cannot be changed.

        Args:
            product_data (dict): The same keys as ``create_product`` except "complexId".

        Returns:
            dict: The transaction receipt.
        """
        args = args_from(product_data, UPDATE_PRODUCT_FIELDS)
        return self._transact(contract_address, "updateProduct", int(product_id), *args)

    def remove_product(self, contract_address, product_id):
        """
        Removes an existing product passport.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "removeProduct", int(product_id))

    def get_product_details(self, contract_address, product_id):
        """
        Retrieves a product and the geolocation of the complex where it was made.

        Returns:
            dict: ``{"product": {...}, "origin": {"latitude", "longitude", "additionalInfo"}}``,
            where "product" has the keys listed in ``create_product``.
        """
        product, origin = self._call(contract_address, "getProductDetails", int(product_id))
        return {"product": product, "origin": origin}

    def product_exists(self, contract_address, product_id):
        """
        Returns:
            bool: Whether a product exists under ``product_id``.
        """
        return self._call(contract_address, "productExists", int(product_id))

    def complex_management(self, contract_address):
        """
        Returns:
            str: The address of the linked ComplexManagement contract.
        """
        return self._call(contract_address, "complexManagement")
