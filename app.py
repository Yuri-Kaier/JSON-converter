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
