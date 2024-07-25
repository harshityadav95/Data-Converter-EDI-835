from typing import List

from elements.identifier import Identifier
from utilities import split_segment, get_element


class Address:
    """Represents the N3 segment (Address Information) in the EDI 835."""
    identification = 'N3'

    identifier = Identifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.address = get_element(segment, 1) 

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the N3 segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.address,
            # Add any other missing elements as needed 
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.address = data.get('address')
        return segment

if __name__ == "__main__":
    pass