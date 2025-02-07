from typing import List

from elements.identifier import Identifier
from elements.dollars import Dollars
from elements.amount_qualifier import AmountQualifier
from utilities import split_segment


class Amount:
    """Represents the AMT segment (Monetary Amount Information) in the EDI 835."""
    identification = 'AMT'

    identifier = Identifier()
    qualifier = AmountQualifier()
    amount = Dollars()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.qualifier = segment[1]
        self.amount = segment[2] 

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the AMT segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.qualifier, 
            self.amount,
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.qualifier = data.get('qualifier')
        segment.amount = data.get('amount')
        return segment

if __name__ == "__main__":
    pass