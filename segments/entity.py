from typing import List, Optional

from elements.identifier import Identifier
from elements.entity_code import EntityCode
from elements.entity_type import EntityType
from elements.identification_code_qualifier import IdentificationCodeQualifier
from utilities import split_segment, get_element


class Entity:
    """Represents the NM1 segment (entity name and identification) in the EDI 835."""
    identification = 'NM1'

    identifier = Identifier()
    entity = EntityCode()
    type = EntityType()
    identification_code_qualifier = IdentificationCodeQualifier()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.entity = segment[1]
        self.type = segment[2]
        self.last_name = get_element(segment, 3)
        self.first_name = get_element(segment, 4)
        self.middle_name = get_element(segment, 5)
        self.name_prefix = get_element(segment, 6)
        self.name_suffix = get_element(segment, 7)
        self.identification_code_qualifier = get_element(segment, 8)
        self.identification_code = get_element(segment, 9)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the NM1 segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.entity,
            self.type,
            self.last_name,
            self.first_name if self.first_name else '',
            self.middle_name if self.middle_name else '',
            self.name_prefix if self.name_prefix else '',
            self.name_suffix if self.name_suffix else '',
            self.identification_code_qualifier if self.identification_code_qualifier else '',
            self.identification_code if self.identification_code else ''
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict) -> 'Entity':
        """Creates an Entity object from dictionary data."""
        segment = cls('')
        segment.entity = data.get('entity')
        segment.type = data.get('type')
        segment.last_name = data.get('last_name')
        segment.first_name = data.get('first_name')
        segment.middle_name = data.get('middle_name')
        segment.name_prefix = data.get('name_prefix')
        segment.name_suffix = data.get('name_suffix')
        segment.identification_code_qualifier = data.get('identification_code_qualifier')
        segment.identification_code = data.get('identification_code')
        return segment

    @property
    def name(self) -> str:
        """Returns the formatted name of the entity."""
        name_parts = [
            self.name_prefix,
            self.first_name,
            self.middle_name,
            self.last_name,
            self.name_suffix
        ]
        return " ".join(part for part in name_parts if part).strip()

if __name__ == '__main__':
    pass