import json
import ast

def kumu_to_pipeline(file):
    curFile = json.load(open("./evaluations/kumu_to_pipeline/inputs/" + file))
    output = {
        "relations": []
    }
    

    for connection in curFile['connections']:
        consolidate = {
            "relationshipc": [],
            "iscausal": [],
            "supportingtext": [],
        }
        attrs = connection['description'].split("\n=====\n")
        for attr in attrs:
            temp = ast.literal_eval(attr)
            consolidate['relationshipc'].append(temp['relationType'])
            consolidate['iscausal'].append(temp['isCausal'])
            consolidate['supportingtext'].append(temp['SupportingText'])

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": consolidate['relationshipc'],
            "isCausal" : consolidate['iscausal'],
            "SupportingText": consolidate['supportingtext']
        }
        output['relations'].append(entry)
    with open("./outputs/" + file[:-5] + "_output.json", "w") as f:
        f.write(json.dumps(output, indent=4))

def kumu_to_pipeline_no_io(dictionary):
    curFile = dictionary
    output = {
        "relations": []
    }
    

    for connection in curFile['connections']:
        consolidate = {
            "relationshipc": [],
            "iscausal": [],
            "supportingtext": [],
        }
        attrs = connection['description'].split("\n=====\n")
        for attr in attrs:
            temp = ast.literal_eval(attr)
            consolidate['relationshipc'].append(temp['relationType'])
            consolidate['iscausal'].append(temp['isCausal'])
            consolidate['supportingtext'].append(temp['SupportingText'])

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": consolidate['relationshipc'],
            "isCausal" : consolidate['iscausal'],
            "SupportingText": consolidate['supportingtext']
        }
        output['relations'].append(entry)
    
    return output

if __name__ == "__main__":
    kumu_to_pipeline("kumu_test.json")