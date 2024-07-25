from typing import List

from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.date import Date
from edi_835_parser.elements.dollars import Dollars
from edi_835_parser.segments.utilities import split_segment, get_element
from edi_835_parser.elements.adjustment_reason_code import AdjustmentReasonCode
from edi_835_parser.elements.reference_qualifier import ReferenceQualifier

class ProviderLevelAdjustment:
    """Represents the PLB segment in an EDI 835."""

    identification = 'PLB'

    identifier = Identifier()
    fiscal_period_date = Date()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.provider_identifier = segment[1]
        self.fiscal_period_date = segment[2]
        self.adjustment_reason_code = []
        self.reference_identification = []
        self.adjustment_amount = []
        for i in range(3, len(segment), 3):
            if i + 2 < len(segment):
                adjustment_identifier = segment[i]
                parts = adjustment_identifier.split(':')
                self.adjustment_reason_code.append(parts[0])
                self.reference_identification.append(parts[1] if len(parts) > 1 else None)
                self.adjustment_amount.append(segment[i + 1])

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the PLB segment to its EDI representation."""
        elements = [self.identifier, self.provider_identifier, self.fiscal_period_date]

        for i in range(len(self.adjustment_reason_code)):
            adjustment_identifier = self.adjustment_reason_code[i]
            if self.reference_identification[i]:
                adjustment_identifier += ":" + self.reference_identification[i]
            elements.extend([adjustment_identifier, self.adjustment_amount[i]])

        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.provider_identifier = data.get('provider_identifier')
        segment.fiscal_period_date = data.get('fiscal_period_date')
        segment.adjustment_reason_code = data.get('adjustment_reason_code', [])
        segment.reference_identification = data.get('reference_identification', [])
        segment.adjustment_amount = data.get('adjustment_amount', [])
        return segment

if __name__ == "__main__":
    pass