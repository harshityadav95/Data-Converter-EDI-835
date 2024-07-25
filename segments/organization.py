from typing import List

from elements.identifier import Identifier
from elements.organization_type import OrganizationType
from utilities import split_segment, get_element


class Organization:
    """Represents the N1 segment (Name) in the EDI 835."""
    identification = 'N1'

    identifier = Identifier()
    type = OrganizationType()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.type = segment[1]
        self.name = get_element(segment, 2)
        self.identification_code_qualifier = get_element(segment, 3)
        self.identification_code = get_element(segment, 4)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the N1 segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.type,
            self.name,
            self.identification_code_qualifier if self.identification_code_qualifier else '',
            self.identification_code if self.identification_code else ''
            # ... (Add other elements if present in your EDI data)
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.type = data.get('type')
        segment.name = data.get('name')
        segment.identification_code_qualifier = data.get('identification_code_qualifier')
        segment.identification_code = data.get('identification_code')
        return segment

if __name__ == "__main__":
    pass