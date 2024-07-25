from typing import List, Optional, Union 


def split_segment(segment: str, segment_delimiter: str = "*") -> List[str]:
    """Splits an EDI segment into its individual elements.

    Handles segments delimited by '*' or '|'.

    Args:
        segment (str): The EDI segment string.
        segment_delimiter (str): Delimiter for splitting elements. Defaults to '*'.

    Returns:
        List[str]: A list of the segment's elements.
    """

    return segment.split(segment_delimiter)


def find_identifier(segment: Union[str, dict]) -> str:
    """
    Extracts the segment identifier from an EDI segment string or dictionary.

    Args:
        segment (Union[str, dict]): The EDI segment.

    Returns:
        str: The segment identifier.
    """

    if isinstance(segment, str):
        segment = split_segment(segment)
        return segment[0]
    elif isinstance(segment, dict):
        return list(segment.keys())[0]
    else:
        raise TypeError("Invalid segment type. Must be string or dictionary.")

def get_element(segment: List[str], index: int, default=None) -> Optional[str]:
    """Gets an element from a list, handling cases where the index might be out of range.

    Args:
        segment (List[str]): The list of elements.
        index (int): The index of the desired element.
        default: The default value to return if the index is out of range.

    Returns:
        Optional[str]: The element at the specified index or the default value.
    """
    element = default
    if index < len(segment):
        element = segment[index]
    return element


if __name__ == "__main__":
    pass 