import xrpl
import datetime
from xrpl.clients import JsonRpcClient
from xrpl.models.transactions import Payment, Transaction
from xrpl.wallet import generate_faucet_wallet
from xrpl.transaction import autofill_and_sign, submit, sign_and_submit
from xrpl.models.requests import AccountTx, AccountInfo
from transaction import Transaction

class wallet:
    def __init__(self):
        JSON_RPC_URL = "https://s.altnet.rippletest.net:51234/"

        self._client = JsonRpcClient(JSON_RPC_URL)
        # Hardcoded testnet address for now
        self._addr = "raCfubD45wbbXazD7bSodkyJ5SKT2NM2LR"

        account_info_request = AccountInfo(
            account=self._addr,
            ledger_index="validated"
        )
        response = self._client.request(account_info_request)

        if response.is_successful():
            balance = response.result["account_data"]["Balance"]
            self._balance = int(balance) / 1_000_000
        else:
            print("Failed to fetch account info:", response.result)

    def get_balance(self):
        return self._balance

    def _ripple_time_to_datetime(self, ripple_time):
        unix_time = ripple_time + 946_684_800
        return datetime.datetime.utcfromtimestamp(unix_time).strftime('%Y-%m-%d %H:%M:%S UTC')

    def _drops_to_xrp(self, drops):
        return int(drops) / 1_000_000

    def _parse_transaction(self, tx):
        txn_type = tx.get("TransactionType", "Unknown")
        from_addr = tx.get("Account", "Unknown")
        txn_hash = tx.get("hash", "Unknown")

        if txn_type == "Payment":
            to_addr = tx.get("Destination", "Unknown")
            amount = tx.get("Amount", "Unknown")
        else:
            return

        txn_date_ripple = tx.get("date")
        txn_date = self._ripple_time_to_datetime(txn_date_ripple)

        txn_dir = None
        if to_addr == self._addr:
            txn_dir = "IN"
        else:
            txn_dir = "OUT"
        txn = Transaction(
            ledger_number=0,
            dt=txn_date,
            dt_ripple=txn_date_ripple,
            amt=self._drops_to_xrp(amount),
            txn_hash=txn_hash,
            from_addr=from_addr,
            to_addr=to_addr,
            txn_type="PAYMENT",
            txn_dir=txn_dir
        )
        return txn

    def get_txn_history(self):
        account_tx_request = AccountTx(
            account=self._addr
        )

        response = self._client.request(account_tx_request)
        transactions = response.result.get("transactions", [])

        txns = []
        for tx in transactions:
            if 'tx' in tx:
                txn = self._parse_transaction(tx['tx'])
                if txn:
                    txns.append(txn)
        return txns

    def manual_sign(self, txn):
        # vm, imp
        pass

    async def send(self, addr, xrp_amt):
        if not xrpl.core.addresscodec.is_valid_xaddress(addr) and not xrpl.core.addresscodec.is_valid_classic_address(addr):
            raise ValueError("Invalid destination address")
        # vm, imp
        pass
    