import json
from json import JSONDecodeError

json_text = json.loads('{"messages":[{"message":"This is the first message","timestamp":"2021-06-04 16:40:53"},{"message":"And this is a second message","timestamp":"2021-06-04 16:41:01"}]}')

try:
    print(json_text["messages"][1]["message"])
except JSONDecodeError:
    print("Response is not in JSON format")