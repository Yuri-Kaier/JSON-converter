import streamlit as st
import json
import csv
from io import StringIO

def parse_to_json_from_csv(csv_data: str) -> dict:
    """
    Parses CSV data into a JSON object.
    Handles multi-line values, quotes, and ensures JSON-compatible escaping.
    """
    csv_file = StringIO(csv_data)  # Convert the string input into a file-like object for CSV parsing
    csv_reader = csv.reader(csv_file, delimiter=',')
    
    json_result = {}
    current_object = None
    current_key = None
    current_value = None
    is_multiline = False
    
    for row in csv_reader:
        if len(row) != 3:
            st.error(f"Invalid row format: '{','.join(row)}'. Each row must have three columns (Passage, Variable, English).")
            return {}

        object_name, key, value = row
        
        # Strip surrounding quotes and whitespace from each part
        object_name = object_name.strip().strip("\"'")
        key = key.strip().strip("\"'")
        value = value.strip("\"'")  # Handle value
        
        # Check if the value starts a multi-line string
        if value.startswith('"""') and not value.endswith('"""'):
            is_multiline = True
            current_object = object_name
            current_key = key
            current_value = value[3:]  # Remove the opening triple quotes
        elif is_multiline:
            # If we're in a multi-line value, continue appending
            if value.endswith('"""'):
                is_multiline = False
                current_value += "\n" + value[:-3]  # Remove the closing triple quotes
                # Save the multi-line value to the result
                if current_object not in json_result:
                    json_result[current_object] = {}
                json_result[current_object][current_key] = current_value.replace("\n", "\\n")
            else:
                current_value += "\n" + value
        else:
            # Add the value directly if it's a single line
            if object_name not in json_result:
                json_result[object_name] = {}
            json_result[object_name][key] = value

    # Handle edge case: If multiline is still True at the end
    if is_multiline:
        st.error("Unterminated multi-line value detected. Please check your input.")
        return {}

    return json_result

# Streamlit UI
st.title("CSV to JSON Converter")

st.write("Paste your CSV data below:")

# Input text area
input_data = st.text_area(
    "Input CSV Data",
    placeholder="Paste your CSV data here...",
    height=300
)

if st.button("Convert to JSON"):
    if input_data.strip():
        try:
            # Process the input and display the output
            result_json = parse_to_json_from_csv(input_data)
            if result_json:
                st.subheader("Converted JSON:")
                st.json(result_json)
        except Exception as e:
            st.error(f"An unexpected error occurred: {e}")
    else:
        st.warning("Please paste data before clicking 'Convert to JSON'.")
