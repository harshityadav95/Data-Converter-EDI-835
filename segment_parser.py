from typing import List, Dict


from utilities import split_segment

class SegmentParser:
    """Parses EDI segments and their elements."""

    def __init__(self, segment_delimiter: str = "*"):
        self.segment_delimiter = segment_delimiter

    def parse(self, segment: str) -> Dict:
        """Parses a single EDI segment.
        
        Args:
            segment (str): The EDI segment string (e.g., 'CLP*CLAIM123*1*125.00').

        Returns:
            Dict: A dictionary representing the parsed segment with the segment 
                  identifier as the key and a list of data elements as the value.
        """
        parts = split_segment(segment, self.segment_delimiter)
        segment_id = parts[0]
        elements = parts[1:]
        return {segment_id: elements}

if __name__ == "__main__":
    pass 