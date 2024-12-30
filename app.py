import streamlit as st
import json

def parse_to_json(data: str) -> dict:
    """
    Parses tab-separated text into a JSON object.
    """
    lines = data.strip().split("\n")
    json_result = {}
    current_object = None
    
    for line in lines:
        parts = line.split("\t")
        if len(parts) == 3:
            # This line defines a new object
            object_name, key, value = parts
            if object_name not in json_result:
                json_result[object_name] = {}
            json_result[object_name][key] = value
        else:
            st.error("Invalid line format. Each line must have three tab-separated values.")
            return {}
    
    return json_result

# Streamlit UI
st.title("Tab-separated Data to JSON Converter")

st.write("Paste your tab-separated data below:")

# Input text area
input_data = st.text_area(
    "Input Data",
    placeholder="Example:\nBook cover\ta\tNew Game\nBook cover\tb\tAchievements\n..."
)

if st.button("Convert to JSON"):
    if input_data:
        # Process the input and display the output
        try:
            result_json = parse_to_json(input_data)
            st.json(result_json)
        except Exception as e:
            st.error(f"An error occurred: {e}")
    else:
        st.warning("Please paste data before clicking 'Convert to JSON'.")
