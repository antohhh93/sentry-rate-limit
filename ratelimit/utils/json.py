import json

def output_json(data = None, indent = 4):
    return json.dumps(
                data,
                indent = indent
            )