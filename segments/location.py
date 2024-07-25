from typing import List

from elements.identifier import Identifier
from utilities import split_segment, get_element


class Location:
    """Represents the N4 segment (Geographic Location) in the EDI 835."""
    identification = 'N4'

    identifier = Identifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.city = get_element(segment, 1)
        self.state = get_element(segment, 2)
        self.zip_code = get_element(segment, 3)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the N4 segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.city,
            self.state,
            self.zip_code,
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.city = data.get('city')
        segment.state = data.get('state')
        segment.zip_code = data.get('zip_code')
        return segment

if __name__ == "__main__":
    pass