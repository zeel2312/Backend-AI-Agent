import openai
import json
import re
from datetime import datetime

# Set up your OpenAI API key
openai.api_key = 'your_open_api_key'


def query_llm(user_input):
    prompt = f"""
    You are an assistant that parses user input to determine the intended database operation.

    Given the following user input, extract the action (insert, update, delete or any synonyms of these actions), key, and value (if applicable). Ensure the response is always a valid JSON object.
    The action, key, and value information should only come from the user's input. If any one of the mentioned parameters (action/key/value) is not given, then return the corresponding parameter as None.

    ### User Input:
    "{user_input}"
    
    ### Rules:
    1. Look for the action first in the user's input. The action can be one of the following or their synonyms, but use only the original actions (insert, update, delete) when writing in the JSON object:
        - **Insert**: add, set, create, insert, new, make
        - **Update**: change, modify, edit, update, replace, alter
        - **Delete**: remove, delete, drop, erase, del
    2. For every input:
        - always include the three mentioned parameters(action/key/value) in your response.
    3. Extract the key and value next:
        - If the key is explicitly mentioned, use it. If not, return None for the "key" field.
        - If the value is explicitly mentioned, use it. If not, return None for the "value" field.
    4. If no recognizable action is present in the user's input, return None for all three parameters.
    5. Do not assume any parameter unless explicitly mentioned in the user's input.



    ### Expected Response Format:
    {{
        "action": "insert",
        "key": "example_key",
        "value": "example_value"
    }}
    {{
        "action": "update",
        "key": "example_key",
        "value": "new_value"
    }}
    {{
        "action": "delete",
        "key": "example_key",
        "value": "delete_value"
    }}

    ### Examples:
    1. User Input: "Insert an entry with key 'my.test' and value 'my.value'"
       Response: {{"action": "insert", "key": "my.test", "value": "my.value"}}

    2. User Input: "Update the value of 'name' to 'zeel' where 'key' is 'name'"
       Response: {{"action": "update", "key": "name", "value": "zeel"}}

    3. User Input: "Delete the entry with key 'name'"
       Response: {{"action": "delete", "key": "name"}}

    ### Now Parse:
    """
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        # print("direct response from llm without any processing: ", response)
        content = response.choices[0].message['content']

        # Use regex to extract the JSON block
        json_match = re.search(r"{.*?}", content, re.DOTALL)
        if json_match:
            json_content = json_match.group(0)
            # Attempt to parse the extracted JSON block
            return json.loads(json_content)
        else:
            raise ValueError("No JSON found in LLM response")
    except json.JSONDecodeError:
        return {"error": "Invalid JSON"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    test_inputs = [
        "Insert an entry with key 'test1' and value 'value1'.",
        "Update the value of 'test1' to 'value2'.",
        "Delete the key 'test1'.",
        "Add a new key-value pair 'test2:value2'.",
        "Set the value 'value3' for the key 'test3'.",
        "Insert entry 'value4' for the key 'test3'.",
        "Can you pls delet 'test5'?",
        "delete value 'abcd'",
        "Insert 'value8' corresponding to 'test8'.",
        "Insert key 'test9'.",
        "Add value 'abcd'",
        "Insert 'key10':'value11'",
        "This is a very interesting project",
        "Remove the column where key is Prachi",
        "Can you please add the ice as key and cream as value",
        "Can you modify or change value table to tables for key chair",
        "Remove the column where key is Prachi",
        "alter key:abcd value:xyzr"
    ]
    
    for test_input in test_inputs:
        response = query_llm(test_input)
        print(f"User Input: {test_input}\nLLM Response after processing: {response}\n")