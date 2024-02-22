import json
import ast

def kumu_to_pipeline(file):
    curFile = json.load(open("./evaluations/kumu_to_pipeline/inputs/" + file))
    output = {
        "Relations": []
    }
    

    for connection in curFile['connections']:
        consolidate = {
            "relationshipc": [],
            "IsCausal": [],
            "supportingtext": [],
        }
        attrs = connection["attributes"]['description'].split("\n=====\n")
        for attr in attrs:
            temp = ast.literal_eval(attr)
            consolidate['relationshipc'].append(temp['relationType'])
            consolidate['IsCausal'].append(temp['isCausal'])
            consolidate['supportingtext'].append(temp['SupportingText'])

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": consolidate['relationshipc'],
            "IsCausal" : consolidate['IsCausal'],
            "SupportingText": consolidate['supportingtext']
        }
        output['Relations'].append(entry)
    with open("./outputs/" + file[:-5] + "_output.json", "w") as f:
        f.write(json.dumps(output, indent=4))

def kumu_to_pipeline_no_io(dictionary):
    curFile = dictionary
    output = {
        "Relations": []
    }
    

    for connection in curFile['connections']:
        consolidate = {
            "relationshipc": [],
            "IsCausal": [],
            "supportingtext": [],
        }
        attrs = connection["attributes"]['description'].split("\n=====\n")
        for attr in attrs:
            temp = ast.literal_eval(attr)
            consolidate['relationshipc'].append(temp['relationType'])
            consolidate['IsCausal'].append(temp['isCausal'])
            consolidate['supportingtext'].append(temp['SupportingText'])

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": consolidate['relationshipc'],
            "IsCausal" : consolidate['IsCausal'],
            "SupportingText": consolidate['supportingtext']
        }
        output['Relations'].append(entry)
    
    return output


def user_input_to_list_of_relations(dictionary):
    curFile = dictionary
    output = {
        "Relations": []
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
    return output


if __name__ == "__main__":
    kumu_to_pipeline("kumu_test.json")