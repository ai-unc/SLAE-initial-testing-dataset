import json, sys

def pipeline_to_kumu(dic, outputPath):


    vars = []
    connections = []
    elementList = []
    connectionList = []

    # Process each JSON object in the list

    # for paper in dic["Papers"]:
    paper = dic
    title = paper['PaperTitle']
    doi = paper['PaperDOI']

    # Extract the variables and connections from each relation in the JSON object
    for relation in paper['Relations']:
        variable_one = relation['VariableOneName']
        variable_two = relation['VariableTwoName']
        relationType = relation['RelationshipClassification']
        SupportingText = relation['SupportingText']
        if "isCausal" in relation:
            if relation['isCausal'] == "True":
                relationType = "causal"
            elif relation['isCausal'] == "False":
                relationType = "non-causal"
        else:
            relationType = ""
        # Add the variables to the list if they are not already present
        if(variable_one not in vars):
            vars.append(variable_one)
        if(variable_two not in vars):
            vars.append(variable_two)
            
        connections.append([variable_one, variable_two, relationType, SupportingText, relationType])

            

    # Create the element list for the output JSON
    for var in vars:
        entry = {
            "label": var,
            "type": "variable",
        }
        elementList.append(entry)
        
    # Create the connection list for the output JSON

    for connection in connections:
        if connection[2] == "direct" or connection[2] == "Direct":
            connection[2] = "directed"
        else:
            connection[2] = "mutual"
        entry = {
            "from": connection[0],
            "to": connection[1],
            "direction": connection[2],
            "type": connection[4],
            "description": connection[3]
        }
        connectionList.append(entry)

    # Write the output JSON to ParsedMultiVariablePipelineOutput.json file
    with open(outputPath + "ParsedMultiVariablePipelineOutput.json", 'w') as g:
        output_dict = {"elements": elementList, "connections": connectionList}
        json_str = json.dumps(output_dict, indent=4)
        g.write(json_str)
    g.close()

# if __name__ == "__main__":
#     outputPath = sys.path[0][:-15] + "outputs\\"
#     f = open(outputPath + "MultiVariablePipelineOutput.txt")
#     pipeline_to_kumu(f, outputPath)
        