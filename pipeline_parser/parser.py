import json, sys

# # Get the path to the output directory
# outputPath = sys.path[0][:-15] + "outputs\\"

# # Read the contents of the MultiVariablePipelineOutput.txt file
# with open(path + "MultiVariablePipelineOutput.txt") as f:
#     data = f.read()

def main(f, outputPath):
    data = f.read()
    jsons = []
    first = 0
    file = ""

    # Split the data by newline character and process each line
    for line in data.split("\n"):
        # Check if the line indicates the start of a new JSON object
        if line[:10] == "pre parse:" or line[:31] == "successful parse MULTIRELATION:":
            # If there are already JSON objects in the list or it's not the first object, append the previous object to the list
            if(len(jsons) != 0 or first == 1):
                jsons.append(file)
                file = "{"
            else:
                file += "{"
                first = 1
        else:
            file += line
    
    vars = []
    connections = []
    elementList = []
    connectionList = []

    # Process each JSON object in the list

    for jsn in jsons:
        try:
            temp = json.loads(jsn)
            # Extract the variables and connections from each relation in the JSON object
            for relation in temp['Relations']:
                variable_one = relation['VariableOneName']
                variable_two = relation['VariableTwoName']
                relationType = relation['RelationshipClassification']
                SupportingText = relation['SupportingText']
                if relation['isCausal'] == "True":
                    relationType = "causal"
                elif relation['isCausal'] == "False":
                    relationType = "non-causal"
                # Add the variables to the list if they are not already present
                if(variable_one not in vars):
                    vars.append(variable_one)
                if(variable_two not in vars):
                    vars.append(variable_two)
                
                connections.append([variable_one, variable_two, relationType, SupportingText, relationType])
        except:
            print(jsons.index(jsn))
            

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

if __name__ == "__main__":
    outputPath = sys.path[0][:-15] + "outputs\\"
    f = open(outputPath + "MultiVariablePipelineOutput.txt")
    main(f, outputPath)
        