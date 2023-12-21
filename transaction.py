class Transaction:
    
    def __init__(self, ledger_number, dt, dt_ripple, amt, txn_hash, from_addr, to_addr, txn_type, txn_dir):
        self.ledger_number = ledger_number
        self.dt = dt
        self.dt_ripple = dt_ripple
        self.amt = amt
        self.txn_hash = txn_hash
        self.from_addr = from_addr
        self.to_addr = to_addr
        self.txn_type = txn_type
        self.txn_dir = txn_dir

    def get_dt(self):
        return self.dt

    def get_txn_dir(self):
        return self.txn_dir

    def get_txn_symb(self):
        return "↙" if self.txn_dir == "IN" else "↗"
    
    def get_ripple_time(self):
        return self.dt_ripple

    def get_amt(self):
        return self.amt

    def get_net_txn(self):
        net = self.amt
        if self.txn_dir == "OUT":
            net = "-" + str(self.amt)
        else:
            net = "+" + str(self.amt)
        return net

    def __repr__(self):
        return f"Transaction(LedgerNumber={self.ledger_number}, DateTime={self.dt}, Amount={self.amt}, TxnHash='{self.txn_hash}', FromAddr='{self.from_addr}', ToAddr='{self.to_addr}', TxnType='{self.txn_type}')"