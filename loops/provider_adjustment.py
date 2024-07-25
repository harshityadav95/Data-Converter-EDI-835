from typing import Tuple, Iterator, Optional, List

from segments.provider_level_adjustment import ProviderLevelAdjustment as PLBSegment
from utilities import find_identifier

class ProviderAdjustment:
    """Represents a provider adjustment loop in the EDI 835."""
    initiating_identifier = PLBSegment.identification
    terminating_identifiers = ['PLB', 'SE'] # Adjust terminating identifiers as needed

    def __init__(self, adjustments: List[PLBSegment] = None):
        self.adjustments = adjustments if adjustments else []

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    @classmethod
    def build(cls, segment: dict, segments: Iterator[List[dict]]) -> Tuple['ProviderAdjustment', Optional[Iterator[List[dict]]], Optional[dict]]:
        """Builds the provider adjustment loop from the segments.

        Args:
            segment (dict): The current parsed segment.
            segments (Iterator[List[dict]]): Iterator over remaining segments.

        Returns:
            Tuple[ProviderAdjustment, Optional[Iterator[List[dict]]], Optional[dict]]: A tuple containing the built ProviderAdjustment object, the updated segments iterator, and the next segment.
        """
        adjustment = ProviderAdjustment()
        adjustment.adjustments.append(PLBSegment(segment[PLBSegment.identification][0]))

        while True:
            try:
                segment = segments.__next__()
                identifier = find_identifier(segment)

                if identifier == PLBSegment.identification:  
                    adjustment.adjustments.append(PLBSegment(segment[PLBSegment.identification][0]))
                
                elif identifier in cls.terminating_identifiers:
                    return adjustment, segments, segment

            except StopIteration:
                return adjustment, None, None
    
    def to_edi(self) -> List[str]:
        """Converts the provider adjustment loop back to EDI format."""
        return [adjustment.to_edi() for adjustment in self.adjustments]

if __name__ == "__main__":
    pass