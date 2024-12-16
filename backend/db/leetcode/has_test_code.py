import json
from pathlib import Path

def print_test_codes(directory: str) -> None:
    """
    Iterate through JSON files in directory and print test code if present.

    Args:
        directory: Path to the interview_data directory
    """
    # Convert string path to Path object
    data_path = Path(directory)

    # Iterate through all JSON files
    for json_file in data_path.glob("*.json"):
        try:
            with open(json_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Check if test_code exists and is not empty
            if test_code := data.get("test_code"):
                print(f"\n=== Test code for {json_file.name} ===")
                print(test_code)

        except json.JSONDecodeError:
            print(f"Error: Could not parse JSON file: {json_file}")
        except Exception as e:
            print(f"Error processing {json_file}: {str(e)}")

if __name__ == "__main__":
    # Adjust this path to match your project structure
    interview_data_dir = "interview_data"
    print_test_codes(interview_data_dir)
