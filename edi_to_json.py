import json
from typing import Union, List

from transaction_set_builder import TransactionSet, TransactionSetBuilder


def edi_to_json(edi_file_path: str) -> str:
    """Converts an EDI 835 file to JSON format.

    Args:
        edi_file_path (str): The path to the EDI 835 file.

    Returns:
        str: The JSON representation of the EDI 835 file. 
    """

    with open(edi_file_path, 'r') as f:
        edi_data = f.read()

    builder = TransactionSetBuilder()
    transaction_set = builder.build(iter(edi_data.split('~')))

    json_output = json.dumps(transaction_set, default=_custom_serializer, indent=4)
    return json_output


def _custom_serializer(obj):
    """Handles serialization of custom objects."""
    if isinstance(obj, (TransactionSet, ClaimLoop, ServiceLoop, OrganizationLoop)):
        return obj.__dict__
    
    if hasattr(obj, '__dict__'):
        return obj.__dict__
    
    if isinstance(obj, (list, tuple)):
        return [_custom_serializer(item) for item in obj]
    
    raise TypeError(f"Type {type(obj)} not serializable")

if __name__ == "__main__":
    pass 