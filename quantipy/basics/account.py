import uuid

class Account(object):
    def __init__(self, i_description=""):
        self.id = uuid.uuid4()
        self.description = i_description
        self.interest_rate = 0.0
        self.init_margin_sec = 0.0
        self.maint_margin_sec = 0.0
        self.naked_put_factor = 0.0
        self.naked_call_factor = 0.0
        self.init_margin_span = 0.0
        self.maint_margin_span = 0.0
        self.balance = 0.0
        self.currency = ""
        self.commission_id = ""


class Commission(object):
    def __init__(self, i_description):
        self.id = uuid.uuid4()
        self.description = i_description
        self.base_fee_stocks = 0.0
        self.per_open_fee_stocks = 0.0
        self.per_close_fee_stocks = 0.0
        self.min_fee_stocks = 0.0
        self.base_fee_options = 0.0
        self.per_open_fee_options = 0.0
        self.per_close_fee_options = 0.0
        self.min_fee_options = 0.0
        self.base_fee_futures = 0.0
        self.per_open_fee_futures = 0.0
        self.per_close_fee_futures = 0.0
        self.min_fee_futures = 0.0


