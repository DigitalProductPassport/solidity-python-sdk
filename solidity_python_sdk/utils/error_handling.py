import json
import logging
import os
from web3 import Web3
from eth_account import Account

class InsufficientFundsError(Exception):
    pass

class TransactionFailedError(Exception):
    pass
