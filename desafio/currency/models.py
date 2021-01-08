from dataclasses import dataclass


@dataclass
class RequestCurrencyQuotationParam():
    def __init__(self, from_simbol, to_simbol, initial_date, final_date):
        self.to_simbol = to_simbol
        self.from_simbol = from_simbol
        self.initial_date = initial_date
        self.final_date = final_date

