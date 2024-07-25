from typing import List

from elements.identifier import Identifier
from elements.date import Date as DateElement
from elements.date_qualifier import DateQualifier
from utilities import split_segment


class Date:
    """Represents the DTM segment (Date/Time Reference) in the EDI 835."""

    identification = 'DTM'

    identifier = Identifier()
    qualifier = DateQualifier()
    date = DateElement()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.qualifier = segment[1]
        self.date = segment[2]

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the DTM segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.qualifier,
            self.date,
        ]
        return '*'.join(str(element) for element in elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.qualifier = data.get('qualifier')
        segment.date = data.get('date')
        return segment

if __name__ == "__main__":
    pass