import logging
from solidity_python_sdk.utils import utils
from solidity_python_sdk.utils.error_handling import TransactionFailedError


class BaseContract:
    """
    Shared logic for the contract wrappers: deployment, signing and sending
    transactions, read-only calls, and the Ownable functions every contract has.

    Subclasses set ``CONTRACT_NAME`` to the name of the compiled contract.

    Attributes:
        sdk (DigitalProductPassportSDK): The SDK instance for interacting with the blockchain.
        web3 (Web3): Web3 instance for blockchain interactions.
        account (Account): Ethereum account used for transactions.
        gwei_bid (int): Gas price in gwei.
        contract (dict): ABI and bytecode of the contract.
        logger (Logger): Logger instance for logging information and debug messages.
    """

    CONTRACT_NAME = None

    def __init__(self, sdk):
        """
        Args:
            sdk (DigitalProductPassportSDK): The SDK instance for blockchain interactions.

        Raises:
            KeyError: If the contract is not found in the SDK contracts.
        """
        self.sdk = sdk
        self.web3 = sdk.web3
        self.account = sdk.account
        self.gas = sdk.gas
        self.gwei_bid = sdk.gwei_bid

        if self.CONTRACT_NAME not in sdk.contracts:
            raise KeyError(f"Contract '{self.CONTRACT_NAME}' not found in SDK")

        self.contract = sdk.contracts[self.CONTRACT_NAME]
        self.logger = logging.getLogger(type(self).__module__)

    def deploy(self, initial_owner=None):
        """
        Deploys the contract to the blockchain.

        Args:
            initial_owner (str, optional): The address of the initial owner of the contract.
                Defaults to the SDK account's address.

        Returns:
            str: The address of the deployed contract.
        """
        self.logger.info(f"Deploying {self.CONTRACT_NAME} contract from {self.account.address}")
        Contract = self.web3.eth.contract(abi=self.contract["abi"], bytecode=self.contract["bytecode"])
        tx_receipt = self._send(Contract.constructor(initial_owner or self.account.address))
        self.logger.info(f"{self.CONTRACT_NAME} contract deployed at address: {tx_receipt.contractAddress}")
        return tx_receipt.contractAddress

    def owner(self, contract_address):
        """
        Returns:
            str: The address of the current owner of the contract.
        """
        return self._call(contract_address, "owner")

    def transfer_ownership(self, contract_address, new_owner):
        """
        Transfers ownership of the contract. Only the current owner can do this.

        Returns:
            dict: The transaction receipt.
        """
        return self._transact(contract_address, "transferOwnership", new_owner)

    def _instance(self, contract_address):
        return self.web3.eth.contract(address=contract_address, abi=self.contract["abi"])

    def _transact(self, contract_address, function_name, *args):
        function = getattr(self._instance(contract_address).functions, function_name)(*args)
        try:
            tx_receipt = self._send(function)
        except Exception as e:
            self.logger.error(f"{self.CONTRACT_NAME}.{function_name} failed: {e}")
            raise
        self.logger.info(f"{self.CONTRACT_NAME}.{function_name} transaction receipt: {tx_receipt}")
        return tx_receipt

    def _call(self, contract_address, function_name, *args):
        function = getattr(self._instance(contract_address).functions, function_name)(*args)
        try:
            result = function.call()
        except Exception as e:
            self.logger.error(f"{self.CONTRACT_NAME}.{function_name} call failed: {e}")
            raise
        return decode_outputs(result, function.abi["outputs"])

    def _send(self, function):
        """Builds, signs and sends a transaction, then waits for its receipt."""
        tx = function.build_transaction({
            'from': self.account.address,
            'nonce': self.web3.eth.get_transaction_count(self.account.address, 'pending'),
            'gas': function.estimate_gas({'from': self.account.address}),
            'gasPrice': self.web3.to_wei(self.gwei_bid, 'gwei')
        })
        utils.check_funds(self.web3, self.account.address, tx['gas'] * tx['gasPrice'])

        signed_tx = self.web3.eth.account.sign_transaction(tx, self.account.key)
        tx_hash = self.web3.eth.send_raw_transaction(signed_tx.raw_transaction)
        tx_receipt = self.web3.eth.wait_for_transaction_receipt(tx_hash, timeout=300)
        if tx_receipt["status"] != 1:
            raise TransactionFailedError(f"Transaction {tx_hash.hex()} failed: {tx_receipt}")
        return tx_receipt


def decode_outputs(result, outputs):
    """
    Converts the raw result of a contract call into Python values, turning Solidity
    structs into dicts keyed by their field names.

    A single output is returned on its own. Several named outputs are returned as a
    dict, and several unnamed outputs as a tuple.
    """
    if len(outputs) == 1:
        return _decode(result, outputs[0])
    decoded = [_decode(value, output) for value, output in zip(result, outputs)]
    if all(output["name"] for output in outputs):
        return {output["name"]: value for output, value in zip(outputs, decoded)}
    return tuple(decoded)


def _decode(value, param):
    if not param["type"].startswith("tuple"):
        return value
    if param["type"].endswith("]"):
        element = dict(param, type=param["type"][:param["type"].rindex("[")])
        return [_decode(item, element) for item in value]
    return {component["name"]: _decode(item, component) for component, item in zip(param["components"], value)}


def args_from(data, fields):
    """Returns the values of ``fields`` from ``data`` in order, as contract call arguments."""
    missing = [field for field in fields if field not in data]
    if missing:
        raise ValueError(f"Missing required fields: {', '.join(missing)}")
    return [data[field] for field in fields]
