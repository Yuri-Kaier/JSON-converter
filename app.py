import streamlit as st
import json

def parse_to_json(data: str) -> dict:
    """
    Parses tab-separated text into a JSON object.
    Replaces line breaks inside values with JSON-compatible \\n.
    """
    json_result = {}
    current_object = None

    # Replace actual line breaks within the data with a special marker
    normalized_data = data.replace("\n", "\\n")
    lines = normalized_data.split("\\n")  # Split based on the normalized line breaks

    for line in lines:
        # Split by tab characters
        parts = line.split("\t")

        if len(parts) == 3:
            # Extract object name, key, and value
            object_name, key, value = parts

            # Remove surrounding quotes (if any) and extra whitespace
            object_name = object_name.strip().strip("\"'")
            key = key.strip().strip("\"'")
            value = value.strip().strip("\"'")

            # Restore escaped line breaks as \\n for JSON compatibility
            value = value.replace("\\n", "\n")  # Optional: Show raw line breaks
            value = value.replace("\n", "\\n")  # JSON-escaped line breaks

            # Add to the JSON structure
            if object_name not in json_result:
                json_result[object_name] = {}
            json_result[object_name][key] = value
        else:
            st.error(f"Invalid line format: '{line}'. Each line must have three tab-separated values.")
            return {}

    return json_result

# Streamlit UI
st.title("Tab-separated Data to JSON Converter")

st.write("Paste your tab-separated data below:")
st.markdown("""
#### Example Input:
Book cover\ta\t'New Game with \nline breaks' Book cover\tb\t"Achievements with \n"quotes" and line breaks" Book cover\tc\tMulti-line\nValue Book cover\td\tClose Game
""")

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

st.markdown("Developed by [Your Name](#).")  # Add credits or customize
