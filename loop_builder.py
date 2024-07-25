from typing import List, Dict, Iterator, Optional, Tuple

from segment_parser import SegmentParser
from utilities import find_identifier


class LoopBuilder:
    """Builds hierarchical loop structures from parsed EDI segments."""

    loop_start_identifiers = ['LX', 'CLP', 'NM1', 'SVC', 'PLB']  # Add 'PLB' if it starts a loop
    loop_end_identifier = 'SE'

    def __init__(self, segment_delimiter: str = "*"):
        self.segment_parser = SegmentParser(segment_delimiter)

    def build(self, segments: Iterator[str]) -> List[Dict]:
        """Builds the loop structure from the list of parsed EDI segments.

        Args:
            segments (Iterator[str]): An iterator over EDI segments.

        Returns:
            List[Dict]: A list of dictionaries, each representing a loop or segment.
                       Loops will have nested structures.
        """

        loop_stack = []
        result = []

        for segment in segments:
            parsed_segment = self.segment_parser.parse(segment)
            identifier = find_identifier(segment)

            if identifier in self.loop_start_identifiers:
                loop_stack.append([parsed_segment])

            elif identifier == self.loop_end_identifier:
                completed_loop = loop_stack.pop()
                if loop_stack:
                    loop_stack[-1].append(completed_loop)
                else:
                    result.append(completed_loop)

            else:
                if loop_stack:
                    loop_stack[-1].append(parsed_segment)
                else:
                    result.append(parsed_segment)

        return result

if __name__ == "__main__":
    pass