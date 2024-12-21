import json


def get_chars_before_position(file_path, target_position, char_count=100):
    """
    Read JSON file and get characters before specific position

    Args:
        file_path (str): Path to JSON file
        target_position (int): Target position in file
        char_count (int): Number of characters to retrieve before position

    Returns:
        str: Characters before position
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            # Read entire file content
            content = file.read()

            # Calculate start position (handle edge case if target_position < char_count)
            start_pos = max(0, target_position - char_count)

            # Extract characters
            return content[start_pos:target_position]

    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None


# Example usage
if __name__ == "__main__":
    file_path = "D:\\zDSA Project\\PartOne\\Search_Engine_DSA_project\\data\\Lexicons\\Testing\\LexiconGlobalNewsDataset13_English2_Testing.json"
    position = 7323735
    result = get_chars_before_position(file_path, position)
    if result:
        print(f"Characters before position {position}: {result}")