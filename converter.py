from edi_to_json import edi_to_json
from json_to_edi import json_to_edi

def main():
    """Main function for user interaction."""
    while True:
        choice = input("What would you like to do? (1) EDI to JSON (2) JSON to EDI (3) Exit: ")

        if choice == '1':
            edi_file_path = input("Enter the path to your EDI 835 file: ")
            json_output = edi_to_json(edi_file_path)
            print(json_output)
        elif choice == '2':
            json_file_path = input("Enter the path to your JSON file: ")
            with open(json_file_path, 'r') as f:
                json_data = f.read()
            edi_output = json_to_edi(json_data)
            print(edi_output)
        elif choice == '3':
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")


if __name__ == "__main__":
    main() 