import streamlit as st
import json

def parse_to_json(data: str) -> dict:
    """
    Parses tab-separated text into a JSON object.
    Handles quotes (single or double) and line breaks.
    """
    lines = data.strip().split("\n")  # Split input by line breaks
    json_result = {}
    current_object = None

    for line in lines:
        # Split by tab characters
        parts = line.split("\t")
        
        if len(parts) == 3:
            # Extract object name, key, and value
            object_name, key, value = parts

            # Remove surrounding quotes from values, if present
            object_name = object_name.strip().strip("\"'")
            key = key.strip().strip("\"'")
            value = value.strip().strip("\"'")

            # Add to JSON structure
            if object_name not in json_result:
                json_result[object_name] = {}
            json_result[object_name][key] = value
        else:
            # Show error for malformed input
            st.error(f"Invalid line format: '{line}'. Each line must have three tab-separated values.")
            return {}

    return json_result

# Streamlit UI
st.title("Tab-separated Data to JSON Converter")

st.write("Paste your tab-separated data below:")
st.markdown("""
#### Example Input:
