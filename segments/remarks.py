from typing import List

from edi_835_parser.elements.identifier import Identifier
from edi_835_parser.elements.remark_qualifier import RemarkQualifier
from edi_835_parser.elements.remark_code import RemarkCode
from edi_835_parser.segments.utilities import split_segment, get_element


class Remark:
    """Represents the LQ segment (Health Care Remark Codes) in the EDI 835."""
    identification = 'LQ'

    identifier = Identifier()
    qualifier = RemarkQualifier()
    code = RemarkCode()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.qualifier = segment[1]
        self.code = segment[2]

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the LQ segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.qualifier.code,  # Get the code from RemarkQualifier object
            self.code.code,       # Get the code from RemarkCode object
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.qualifier = RemarkQualifier().parser(data.get('qualifier', {}).get('code'))
        segment.code = RemarkCode().parser(data.get('code', {}).get('code'))
        return segment

if __name__ == "__main__":
    pass