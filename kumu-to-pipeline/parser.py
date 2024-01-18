import json, sys, os

for file in os.listdir("kumu-to-pipeline/inputs"):
    curFile = json.load(open("kumu-to-pipeline/inputs/" + file))
    output = {
        "relations": []
    }
    tags = {}
    for element in curFile['elements']:
        if element['label'] not in tags:
            tags[element['label']] = element['tags']
        else:
            tags[element['label']].append(element['tags'])
    

    for connection in curFile['connections']:
        if connection["direction"] == "directed":
            connection["direction"] = "direct"

        

        entry = {
            "VariableOneName": connection['from'],
            "VariableTwoName": connection['to'],
            "RelationshipClassification": connection['direction'],
            #"SupportingText": tags[connection['to']][tags[connection['to']].index(connection['from'])][1]
        }
        output['relations'].append(entry)
    with open("kumu-to-pipeline/outputs/" + file[:-5] + "_output.json", "w") as f:
        f.write(json.dumps(output, indent=4))

