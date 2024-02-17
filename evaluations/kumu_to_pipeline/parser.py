import json

def kumu_to_pipeline(file):
    curFile = json.load(open("./inputs/" + file))
    output = {
        "relations": []
    }
    

    for connection in curFile['connections']:
        if connection["direction"] == "directed":
            connection["direction"] = "direct"

        if connection["type"] == "causal":
            connection["type"] = "True"
        elif connection["type"] == "non-causal":
            connection["type"] = "False"

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": connection['direction'],
            "isCausal" : connection['type'],
            "SupportingText": connection['description']
        }
        output['relations'].append(entry)
    with open("./outputs/" + file[:-5] + "_output.json", "w") as f:
        f.write(json.dumps(output, indent=4))

