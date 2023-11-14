import os
vars = [] #The list of vars and what they are connected to
dir = "./models"
for filename in os.listdir(dir):
    with open("models/test.mdl", "r") as f:
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
                print(sline)
            elif sline[0] == '1':
                vars.append([])
                factors = []
                factors.append(vars[int(sline[2])-1][0])
                match sline[6]:
                    case "0":
                        factors.append("Neutral")
                    case "43":
                        factors.append("+")
                    case "45":
                        factors.append("-")
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
                        factors.append("?")
                vars[int(sline[3]) - 1].append(factors)
            elif line[0] == "/":
                f.close()
                break

    #Basic output from list to file output
    with open(f"outputs/{filename[:-4]}.json", 'w') as g:
        g.write("Variable:  Influenced by\n")
        for var in vars:
            if len(var) > 0:
                line = var[0] + ":  "
                if len(var) > 1:
                    for item in var[1:]:
                        line += item[0] + " (" + item[1] + "), "
                g.write(line[:len(line)-2] + '\n')
    g.close()
 