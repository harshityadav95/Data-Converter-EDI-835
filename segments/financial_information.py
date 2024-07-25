from typing import List

from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.payment_method import PaymentMethod
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.elements.date import Date
from edi_835_parser.segments.utilities import split_segment, get_element


class FinancialInformation:
    """Represents the BPR segment (Financial Information) of the EDI 835."""

    identification = 'BPR'

    identifier = Identifier()
    amount_paid = Dollars()
    payment_method = PaymentMethod()
    transaction_date = Date()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.transaction_handling_code = segment[1]
        self.amount_paid = get_element(segment, 2)
        self.credit_debit_flag_code = get_element(segment, 3)
        self.payment_method = get_element(segment, 4)
        self.payment_format_code = get_element(segment, 5)
        self.transaction_date = get_element(segment, 16)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the BPR segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.transaction_handling_code,
            self.amount_paid,
            self.credit_debit_flag_code,
            self.payment_method,
            self.payment_format_code,
            # Pad with empty strings for missing elements
            *['' for _ in range(10)], 
            self.transaction_date
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.transaction_handling_code = data.get('transaction_handling_code')
        segment.amount_paid = data.get('amount_paid')
        segment.credit_debit_flag_code = data.get('credit_debit_flag_code')
        segment.payment_method = data.get('payment_method')
        segment.payment_format_code = data.get('payment_format_code')
        segment.transaction_date = data.get('transaction_date')
        return segment


if __name__ == "__main__":
    pass