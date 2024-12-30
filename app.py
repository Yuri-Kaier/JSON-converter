import streamlit as st
import json

def parse_to_json(data: str) -> dict:
    """
    Parses tab-separated text into a JSON object.
    Handles multi-line values, quotes, and ensures JSON-compatible escaping.
    """
    lines = data.strip().split("\n")  # Split input by actual line breaks
    json_result = {}
    current_object = None
    current_key = None
    current_value = None
    is_multiline = False

    for line in lines:
        if not is_multiline:
            # Split by tab characters
            parts = line.split("\t")
            if len(parts) == 3:
                # Extract object name, key, and value
                object_name, key, value = parts

                # Remove surrounding quotes and whitespace
                object_name = object_name.strip().strip("\"'")
                key = key.strip().strip("\"'")
                value = value.strip("\"'")  # Handle value

                # Check if the value starts a multi-line string
                if value.startswith('"""') and not value.endswith('"""'):
                    is_multiline = True
                    current_object = object_name
                    current_key = key
                    current_value = value[3:]  # Remove the opening triple quotes
                else:
                    # Add the value directly if it's a single line
                    if object_name not in json_result:
                        json_result[object_name] = {}
                    json_result[object_name][key] = value
            else:
                st.error(f"Invalid line format: '{line}'. Each line must have three tab-separated values.")
                return {}
        else:
            # If currently handling a multi-line value, continue appending
            if line.endswith('"""'):
                is_multiline = False
                current_value += "\n" + line[:-3]  # Remove closing triple quotes
                # Save the multi-line value
                if current_object not in json_result:
                    json_result[current_object] = {}
                json_result[current_object][current_key] = current_value.replace("\n", "\\n")
            else:
                current_value += "\n" + line

    # Handle edge case: If multiline is still True at the end
    if is_multiline:
        st.error("Unterminated multi-line value detected. Please check your input.")
        return {}

    return json_result

# Streamlit UI
st.title("Tab-separated Data to JSON Converter")

# Input text area
input_data = st.text_area(
    "Input Data",
    placeholder="Paste your data here...",
    height=300
)

if st.button("Convert to JSON"):
    if input_data.strip():
        try:
            # Process the input and display the output
            result_json = parse_to_json(input_data)
            if result_json:
                st.subheader("Converted JSON:")
                st.json(result_json)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please paste data before clicking 'Convert to JSON'.")
