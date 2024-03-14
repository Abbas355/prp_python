import streamlit as st

def generate_json_response():
    # Generate JSON response
    data = {
        "message": "This is a JSON response from Streamlit!",
        "result": {
            "key1": "value1",
            "key2": "value2",
            "key3": "value3"
        }
    }
    return data

def main():
    # Generate JSON response
    json_response = generate_json_response()

    # Write JSON response
    st.json(json_response)

if __name__ == "__main__":
    main()
