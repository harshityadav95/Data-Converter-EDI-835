from typing import List

from elements.identifier import Identifier
from elements.dollars import Dollars
from elements.service_code import ServiceCode
from elements.service_qualifier import ServiceQualifer
from elements.service_modifier import ServiceModifier
from elements.integer import Integer
from utilities import split_segment, get_element


class Service:
    """Represents the SVC segment (Service Payment Information) in the EDI 835."""
    identification = 'SVC'

    identifier = Identifier()
    charge_amount = Dollars()
    paid_amount = Dollars()
    code = ServiceCode()
    qualifier = ServiceQualifer()
    modifier = ServiceModifier()
    allowed_units = Integer()
    billed_units = Integer()
    revenue_code = str()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.code = segment[1]
        self.qualifier = segment[1]
        self.modifier = segment[1]
        self.charge_amount = get_element(segment, 2)
        self.paid_amount = get_element(segment, 3)
        self.revenue_code = get_element(segment, 4)

        # assume unit count of one if unit not provided
        default = 0 if self.paid_amount == 0 else 1
        self.allowed_units = get_element(segment, 5, default=default)

        self.billed_units = get_element(segment, 7, default=self.allowed_units)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the SVC segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.code,  # The code property already includes qualifier and modifier
            self.charge_amount,
            self.paid_amount,
            self.revenue_code if self.revenue_code else '',  # Include revenue code if present
            self.allowed_units,
            '',  # Placeholder for another composite element
            self.billed_units,
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.code = data.get('code')
        segment.qualifier = data.get('qualifier')
        segment.modifier = data.get('modifier')
        segment.charge_amount = data.get('charge_amount')
        segment.paid_amount = data.get('paid_amount')
        segment.allowed_units = data.get('allowed_units')
        segment.billed_units = data.get('billed_units')
        segment.revenue_code = data.get('revenue_code')
        return segment

if __name__ == "__main__":
    pass