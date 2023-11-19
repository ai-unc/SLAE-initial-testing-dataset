import os, json, sys, re

if sys.argv[1] == "-h" or sys.argv[1] == "--help":
    print("Usage: python script.py -m=MODEL")
    print("MODEL: The name of the model to be parsed.")
    sys.exit()

if len(sys.argv) < 2 or len(sys.argv) > 2:
    print("Invalid number of arguments")
    sys.exit("Type 'python script.py -h' for help")

modelFlag = sys.argv[1]

if not modelFlag.startswith("-m=") or len(modelFlag) < 7 or not modelFlag.endswith(".mdl"):
    sys.exit("Invalid model flag")

#The list of variables for this model
vars = []
with open(f"models/{modelFlag}", "r") as f:
    '''
    Vensim model breakdown
    Item type, item id, item name, (other unneeded data)
    10,1,Births,402,208,42,22,8,3,0,0,-1,0,0,0,0,0,0,0,0,0

    Item type, item id, to, from, ?, ?, relation type, (other unneeded data)
    1,4,1,2,1,0,43,0,0,64,0,-1--1--1,,1|(479,138)|
    '''
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
    
for var in vars:
    if(len(var) < 2):
        vars.remove(var)

#Basic output from list to file output
with open(f"outputs/{modelFlag[:-4]}.json", 'w') as g:
    json_list = []
    for var in vars:
        for item in var[1:]:
            entry = {
                "VariableOneName": var[0],
                "VariableTwoName": item[0],
                "RelationshipClassification": item[1]
            }
            json_list.append(entry)
    output_dict = {"Variables": json_list}
    json_str = json.dumps(output_dict, indent=4)
    g.write(json_str)
g.close()
 