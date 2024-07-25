from typing import List

from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.adjustment_group_code import AdjustmentGroupCode
from edi_835_parser.elements.adjustment_reason_code import AdjustmentReasonCode
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.segments.utilities import split_segment, get_element


class ServiceAdjustment:
    """Represents the CAS segment (Claim Adjustment) in the EDI 835."""

    identification = 'CAS'

    identifier = Identifier()
    group_code = AdjustmentGroupCode()
    reason_code = AdjustmentReasonCode()
    amount = Dollars()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.group_code = segment[1]
        self.reason_code = segment[2]
        self.amount = get_element(segment, 3)
        self.quantity = get_element(segment, 4)  # Add quantity element 

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the CAS segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.group_code.code,  # Get code from AdjustmentGroupCode
            self.reason_code.code, # Get code from AdjustmentReasonCode
            self.amount,
            self.quantity if self.quantity else '',  # Include quantity if present
            # Add any other missing elements as needed
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.group_code = AdjustmentGroupCode().parser(data.get('group_code', {}).get('code'))
        segment.reason_code = AdjustmentReasonCode().parser(data.get('reason_code', {}).get('code'))
        segment.amount = data.get('amount')
        segment.quantity = data.get('quantity')
        return segment


if __name__ == "__main__":
    passHi