from typing import List

from elements.identifier import Identifier
from elements.claim_status import ClaimStatus
from elements.dollars import Dollars
from elements.claim_type import ClaimType
from utilities import split_segment, get_element


class Claim:
    """Represents the CLP segment (Claim Payment Information) in the EDI 835."""
    identification = 'CLP'

    identifier = Identifier()
    status = ClaimStatus()
    charge_amount = Dollars()
    paid_amount = Dollars()
    patient_responsibility_amount = Dollars()
    claim_type = ClaimType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.marker = get_element(segment, 1)
        self.status = get_element(segment, 2)
        self.charge_amount = get_element(segment, 3)
        self.paid_amount = get_element(segment, 4)
        self.patient_responsibility_amount = get_element(segment, 5)
        self.claim_type = get_element(segment, 6)
        self.icn = get_element(segment, 7)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the CLP segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.marker,
            self.status.code,  # Access the status code from the Status object
            self.charge_amount,
            self.paid_amount,
            self.patient_responsibility_amount,
            self.claim_type,
            self.icn,
            # Add any other missing elements as empty strings
            *['' for _ in range(4)],  # Adjust the range as needed
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.marker = data.get('marker')
        segment.status = ClaimStatus().parser(data.get('status', {}).get('code'))
        segment.charge_amount = data.get('charge_amount')
        segment.paid_amount = data.get('paid_amount')
        segment.patient_responsibility_amount = data.get('patient_responsibility_amount')
        segment.claim_type = data.get('claim_type')
        segment.icn = data.get('icn')
        return segment


if __name__ == "__main__":
    pass