from typing import List

from elements.identifier import Identifier
from elements.reference_qualifier import ReferenceQualifier
from utilities import split_segment


class Reference:
    """Represents the REF segment (Reference Identification) in the EDI 835."""
    identification = 'REF'

    identifier = Identifier()
    qualifier = ReferenceQualifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.qualifier = segment[1]
        self.value = segment[2] if len(segment) > 2 else '' 

    def __repr__(self) -> str:
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the REF segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.qualifier.code,  # Get code from the ReferenceQualifier object
            self.value,
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.qualifier = ReferenceQualifier().parser(data.get('qualifier', {}).get('code'))
        segment.value = data.get('value')
        return segment

if __name__ == "__main__":
    pass