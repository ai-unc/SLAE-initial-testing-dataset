# Import necessary libraries
import json

# Check if the first argument is a help flag
# if sys.argv[1] == "-h" or sys.argv[1] == "--help":
#     # If it is, print the usage instructions and exit
#     print("Usage: python script.py -model=MODEL")
#     print("MODEL: The name of the model to be parsed.")
#     sys.exit()

# # Check if the number of arguments is not 2
# if len(sys.argv) < 2 or len(sys.argv) > 2:
#     # If it is not, print an error message and exit
#     print("Invalid number of arguments")
#     sys.exit("Type 'python script.py -h' for help")

# # Get the model flag from the arguments
# modelFlag = sys.argv[1]

# # Check if the model flag is valid
# if not modelFlag.startswith("-model=") or len(modelFlag) < 7 or not modelFlag.endswith('.mdl'):
#     # If it is not, print an error message and exit
#     sys.exit("Invalid model flag")

# Initialize a list to store the variables for this model
def vinsim_to_json_kumu(modelFlag):
    vars = []

    #modelFlag = modelFlag.split("=")[1]

    # Open the model file
    with open(f"./parser/models/{modelFlag}", "r") as f:
        '''
            Vensim model breakdown
            Item type, item id, item name, (other unneeded data)
            10,1,Births,402,208,42,22,8,3,0,0,-1,0,0,0,0,0,0,0,0,0

            Item type, item id, to, from, ?, ?, relation type, (other unneeded data)
            1,4,1,2,1,0,43,0,0,64,0,-1--1--1,,1|(479,138)|
        '''
        # Loop through each line in the file
        for line in f:
            sline = line.split(",")
            if sline[0] == "10":
                #In case the var name contains commas
                if(sline[2][0] == '"'):
                    while(sline[3][-1] != '"'):
                        sline[2] = sline[2] + "," + sline[3]
                        sline.remove(sline[3])
                    sline[2] = sline[2] + "," + sline[3]
                    sline.remove(sline[3])
                vars.append([sline[2]])
                #print(sline)
            elif sline[0] == '1':
                vars.append([])
                factors = []
                factors.append(vars[int(sline[2])-1][0])
                match sline[6]:
                    case "0":
                        factors.append("Neutral")
                    case "43":
                        factors.append("Positive")
                    case "45":
                        factors.append("Inverse")
                    case "83":
                        factors.append("S")
                    case "79":
                        factors.append("O")
                    case "89":
                        factors.append("Y")
                    case "78":
                        factors.append("N")
                    case "85":
                        factors.append("U")
                    case "63":
                        factors.append("Inconclusive")
                vars[int(sline[3]) - 1].append(factors)
            elif line[0] == "/":
                f.close()
                break

    # Remove variables that don't have any relationships
    strippedVars = []
    for var in vars:
        if(len(var) >= 2):
            strippedVars.append(var)

    # Open the output file
    with open(f"./parser/json/{modelFlag[:-4]}.json", 'w') as g:
        # Initialize a list to store the JSON objects
        json_list = []
        # Loop through each variable in the list of variables
        for var in strippedVars:
            # Loop through each relationship for the current variable
            for item in var[1:]:
                # Create a JSON object for the current relationship
                entry = {
                    "VariableOneName": item[0],
                    "VariableTwoName": var[0],
                    "RelationshipClassification": item[1]
                }
                # Add the JSON object to the list of JSON objects
                json_list.append(entry)
        # Create a dictionary to store the list of JSON objects
        output_dict = {"Variables": json_list}
        # Convert the dictionary to a JSON string
        json_str = json.dumps(output_dict, indent=4)
        # Write the JSON string to the output file
        g.write(json_str)
    # Close the output file
    g.close()

    ## I currently do not have access to Kumu to check if this formatting will work
    ## This format is based on the Kumu documentation
    ## https://docs.kumu.io/guides/import/blueprints
    ## If this is wrong when we plug it into Kumu, we can change it
    
    with open(f"./parser/kumu/{modelFlag[:-4]}.json", 'w') as h:
        # Initialize a list to store the elements
        elementList = []
        temp = []
        # Loop through each variable in the list of variables
        for var in vars:
            # Create a JSON object for the current relationship
            if(var.__len__() > 0):
                temp.append(var[0])

        # Add the JSON object to the list of elements
        for element in temp:
            entry = {
                "label": element,
                "type": "variable"
            }
            elementList.append(entry)
        
        # Initialize a list to store the connections
        connectionList = []
        for var in vars:
            for item in var[1:]:
                # Create a JSON object for the current connections
                entry = {
                    "from": item[0],
                    "to": var[0],
                    "type": item[1]
                }
                # Add the JSON object to the list of JSON objects
                connectionList.append(entry)
        
        # Create a dictionary to store the list of JSON objects
        output_dict = {"elements": elementList, "connections": connectionList}
        # Convert the dictionary to a JSON string
        json_str = json.dumps(output_dict, indent=4)
        # Write the JSON string to the output file
        h.write(json_str)
    # Close the output file
    h.close()

# if __name__ == "__main__":
#     for file in os.listdir("./parser/models/"):
#         if file.endswith(".mdl"):
#             main(file)