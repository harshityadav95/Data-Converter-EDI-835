from typing import List

from elements.identifier import Identifier
from elements.organization import Organization
from elements.date import Date
from elements.authorization_information_qualifier import AuthorizationInformationQualifier
from utilities import split_segment, get_element


class Interchange:
    """Represents the ISA segment (Interchange Control Header) of the EDI 835."""

    identification = 'ISA'

    identifier = Identifier()
    authorization_information_qualifier = AuthorizationInformationQualifier()
    sender = Organization()
    receiver = Organization()
    transmission_date = Date()
    interchange_control_number = str()
    component_element_separator = str()

    def __init__(self, segment: str):
        self.segment = segment
        segment = split_segment(segment)

        self.identifier = segment[0]
        self.authorization_information_qualifier = get_element(segment, 1)
        self.sender = get_element(segment, 6)
        self.receiver = get_element(segment, 8)
        self.transmission_date = get_element(segment, 9) + get_element(segment, 10)
        self.interchange_control_number = get_element(segment, 13)
        self.component_element_separator = get_element(segment, 16)

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    def to_edi(self) -> str:
        """Converts the ISA segment back to its EDI representation."""
        elements = [
            self.identifier,
            self.authorization_information_qualifier,
            '          ',  # Authorization Information
            '00',          # Security Information Qualifier
            '          ',  # Security Information
            'ZZ',          # Interchange ID Qualifier
            self.sender,    # Interchange Sender ID
            'ZZ',          # Interchange ID Qualifier
            self.receiver,   # Interchange Receiver ID
            self.transmission_date[:6],  # Interchange Date
            self.transmission_date[6:],  # Interchange Time
            '^',          # Repetition Separator
            '00501',       # Interchange Control Version Number
            self.interchange_control_number,  # Interchange Control Number
            '0',          # Acknowledgment Requested
            'P',          # Usage Indicator
            self.component_element_separator,  # Component Element Separator
        ]
        return '*'.join(elements)

    @classmethod
    def from_dict(cls, data: dict):
        segment = cls('')
        segment.authorization_information_qualifier = data.get('authorization_information_qualifier')
        segment.sender = data.get('sender')
        segment.receiver = data.get('receiver')
        segment.transmission_date = data.get('transmission_date')
        segment.interchange_control_number = data.get('interchange_control_number')
        segment.component_element_separator = data.get('component_element_separator')
        return segment

if __name__ == "__main__":
    pass