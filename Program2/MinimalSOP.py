import math

def int_to_char(n):
    # print("int_to_char" + str(n))
    if n <= 0:
        return ""
    base = ord('A') 
    cycle_size = 26
    cycle = (n - 1) // cycle_size + 1
    remainder = (n - 1) % cycle_size
    return chr(base + remainder) +  (str(cycle) if cycle != 1 else "")

def getInverseRange(minSOP, NumberOfVars):
    
    returnRange = []
    for e in range(2**NumberOfVars):
        if(e in minSOP):
            continue
        returnRange += [e]
    return returnRange
    
def getCanonicalSOP(minSOP, NumberOfVars):
    
    returnStrings = ""
    for e in minSOP:
        # print("e: "+str(e))
        temp = e
        SOPstring = ""
        for i in range(NumberOfVars-1, -1,-1):
            SOPstring += int_to_char(NumberOfVars-i)
            if(temp >= 2**i):
                temp -= 2**i
            else:
                  SOPstring+= "'"
        # print("SOPstring: "+SOPstring)
        returnStrings += SOPstring + " + "
    return returnStrings[:-3]

def getCanonicalPOS(minSOP, NumberOfVars):


    returnStrings = ""
    for e in range(2**NumberOfVars):
        if(e in minSOP):
            continue

        # print("e: "+str(e))
        temp = e
        SOPstring = "("
        for i in range(NumberOfVars-1, -1,-1):
            SOPstring += int_to_char(NumberOfVars-i)
            if(temp >= 2**i):
                temp -= 2**i
                SOPstring+= "'"
            
            SOPstring += "+"  
        SOPstring = SOPstring[:-1]
        SOPstring += ")"    
        # print("SOPstring: "+SOPstring)
        returnStrings += SOPstring + " * "
    return returnStrings[:-3]

def getInverseCanonicalSOP(minSOP, NumberOfVars):
    return getCanonicalSOP(getInverseRange(minSOP,NumberOfVars),NumberOfVars)

def getInverseCanonicalPOS(minSOP,NumberOfVars):
    return getCanonicalPOS(getInverseRange(minSOP,NumberOfVars),NumberOfVars)




def multiply(x,y): 
    return_list = []
    for i in x:
        for j in y:
            inner_result = []
            found_in_other= False
            for k in i:
                if k+"'" in j or (len(k)==2 and k[0] in j):
                    found_in_other = True
                    break
                else:
                    
                    inner_result.append(k)
            if(found_in_other):
                continue
            for k in j:
                if k not in inner_result:
                    inner_result.append(k)


            if len(inner_result) != 0:
                return_list.append(inner_result)
            
    return return_list

def findEPI(x): 
    return_list = []
    for i in x:
        if len(x[i]) == 1:
            return_list.append(list(x[i])[0])
    return list(set(return_list))

def generate_variations(binary_string):
    dash_indices = [i for i, char in enumerate(binary_string) if char == "-"]
    
    num_variations = 2 ** len(dash_indices)
    
    variations = []
    
    for i in range(num_variations):
        binary = format(i, '0{}b'.format(len(dash_indices)))
        
        variation = ""
        idx = 0
        for j in range(len(binary_string)):
            if binary_string[j] == "-":
                variation += binary[idx]
                idx += 1
            else:
                variation += binary_string[j]
        
        variations.append(int(variation, 2))
    
    return variations

def minimize_sop(num_array, num_variables):
    binary_strings = [format(num, '0' + str(num_variables) + 'b') for num in num_array]

    groups = {}
    for binary in binary_strings:
        num_ones = binary.count('1')
        if num_ones not in groups:
            groups[num_ones] = set()
        groups[num_ones].add(binary)

    
    Prime_implicants = set()
    while True:
        
        new_groups = {}
        merged_values = set()
        new_values = set()
        finished = True
        l = sorted(list(groups.keys()))
        for i in range(len(l)-1):
            for j in groups[l[i]]: 
                for k in groups[l[i+1]]: 
                    distance = check_distance(j, k)
                    if (distance == 1):
                        new_term = combine_terms(j, k)
                        new_term_ones = new_term.count('1')
                        if(new_term_ones not in new_groups):
                            new_groups[new_term_ones] = set()
                        new_groups[new_term_ones].add(new_term)
                        new_values.add(new_term)
                        merged_values.add(j)
                        merged_values.add(k)
                        finished = False
        
        flattened_group = []
        for i in groups:
            flattened_group.extend(groups[i])
        Prime_implicants = Prime_implicants.union(set(flattened_group) - merged_values)
        
        # l = sorted(list(groups.keys()))
        # for i in range(len(l)-1):
        #     for term in groups[l[i]]:
        #         if term not in merged_values:
                   
        #             if check_match_to_terms(term, new_values):
        #                 print("cosdnfjnsdfnsjkldf")
        #                 continue
        #             if(l[i] not in new_groups):
        #                     new_groups[l[i]] = set()
        #             print("ADDDISDJSDJKSNDJK NKJDNKJS D")
        #             print(term)
        #             print(set(flattened_group) - merged_values)
        #             new_groups[l[i]].add(term)
        
        if finished:
            break
        groups = new_groups
    
    
    chart = {}
    for pi in Prime_implicants:
        my_list = generate_variations(pi)
        for i in my_list:
            if i not in chart:
                chart[i] = set()
            chart[i].add(pi)
    
    epi = findEPI(chart)



    for i in epi:
        for j in generate_variations(i):
            try:
                del chart[j]
            except KeyError:
                pass


    sop = []
    if (len(chart)!=0):
        expression_list = []
        P = []
        for i in chart:
            P_inner = []
            for j in chart[i]:
                temp = binary_to_sop(j)
                if temp not in expression_list:
                    expression_list.append(temp)
                P_inner.append(chr(expression_list.index(temp)+65))
            P.append(P_inner)
        temp = P[0]
        for i in range(1,len(P)):
            temp = multiply(temp,P[i])
        sop = [min(temp,key=len)] 
        temp = []
        for i in sop:
            for j in i:
                temp.append(expression_list[ord(j)-65])
        sop = temp
        sop.extend(binary_to_sop(i) for i in epi) 
    else:
        sop = [binary_to_sop(i) for i in epi]


    return sop


def check_match_to_terms(term, new_terms):
    for i in new_terms:
        for bit1, bit2 in zip(term, i):
            if bit2 == "-" or bit1 == "-":
                continue
            if bit1 != bit2:
                return True
    return False

def check_distance(binary1, binary2):
    distance = 0
    for bit1, bit2 in zip(binary1, binary2):
        if bit1 != bit2:
            distance += 1
    return distance


def combine_terms(term1, term2):
    combined = ''
    for i, (bit1, bit2) in enumerate(zip(term1, term2)):
        if bit1 == bit2:
            combined += bit1
        else:
            combined += '-'
    return combined
    

def binary_to_sop(binary):
    var_list = []
    for i in range(len(binary)):
        if binary[i] == '0':
            var_list.append(chr(i+65)+"'")
        elif binary[i] == '1':
            var_list.append(chr(i+65))
    return var_list


def convertToPOS(x):
    return_string  = ""
    z = x.split(" + ")
    for e in z:
        return_string += "("
        variables = []
        
        for c in range(1,len(e)):
            if(e[c] =="'" ):
                variables.append(e[c-1])
            elif e[c-1] !="'":
                variables.append(e[c-1]+"'")
        if (e[len(e)-1]) != "'":
            variables.append(e[len(e)-1]+"'")
        return_string += " + ".join(variables) + ") * "
    
    return return_string[:-2]

def cal_gates_for_sop(x):
    
    gates  = 0
    z = x.split(" + ")
    for e in z:
        variables = []
        
        for c in range(1,len(e)):
            if(e[c] =="'" ):
                variables.append(e[c-1])
            elif e[c-1] !="'":
                variables.append(e[c-1]+"'")
        if (e[len(e)-1]) != "'":
            variables.append(e[len(e)-1]+"'")
        gates += len(variables)-1
    gates += len(z)-1
    return gates
def cal_gates_for_pos(x):
    gates  = 0
    z = x.split(" * ")
    for e in z:
        
        gates += len(e.split(" + "))-1
    gates += len(z)-1
    return gates

def read_from_file():
    try:
        with open("pla.txt", 'r') as file:
            lines = file.readlines()[2:12]  
            
            equation = []
            
            for line in lines:
                current_express = ""
                x = line.split()
                # print(line)
                # print(x)
                if(x[-1] == "1"):
                    for i in range(3):
                        if(x[i].count("1") == 1):
                            current_express += x[i][0]
                        else:
                            current_express += "-"
                if (current_express == ""):
                    continue
                
                equation += generate_variations(current_express)
            
            return equation   
            
                        
    except Exception as e:
        print(f"An error occurred: {e}")


# input_str = input("Enter space-separated integers: ")
# int_list = []
# if (input_str == "file"):
#     int_list = read_from_file()
# else:
#     input_list = input_str.split()

#     int_list = [int(x) for x in input_list]

# int_list = [1,3,5,6,7] 
# int_list = [1,3] 
# int_list = [4,8,10,11,12,15] 
int_list = [4,5,7,12,14,15] 

def getNumberOfVars(minSOP):
    NumberOfVars = math.log(max(minSOP) , 2)
    if NumberOfVars.is_integer():
        NumberOfVars = int(NumberOfVars)
    else:
        NumberOfVars = math.ceil(NumberOfVars)
    return NumberOfVars

# x = getNumberOfVars(int_list)
# print("\n***************\n")
# print(getCanonicalSOP(int_list,x))
# print("\n***************\n")
# print(getCanonicalPOS(int_list,x))
# print("\n***************\n")
# print("\n***************\n")
# print(getInverseCanonicalSOP(int_list,x))
# print("\n***************\n")
# print(getInverseCanonicalPOS(int_list,x))
# print("\n***************\n")
# print("\n***************\n")
# print(minimize_sop(int_list,x)[0])
# print("Saved " +str(getCanonicalSOP(int_list,x).count("+") - minimize_sop(int_list,x)[0].count("+")) +" literals ")
# print("\n***************\n")
# print(convertToPOS(minimize_sop(getInverseRange(int_list,x),x)[0]))
# print("Saved " +str(getCanonicalPOS(int_list,x).count("*")- convertToPOS(minimize_sop(getInverseRange(int_list,x),x)[0]).count("*")) + " literals")
# print("\n***************\n")
# print("Prime Implicants "+ str(len(minimize_sop(int_list,x)[1])))
# print("Essential Prime Implicants "+ str(len(minimize_sop(int_list,x)[2])))

# print("Number of ON-Set minterms: " + str(len(int_list)))
# print("Number of ON-Set maxterms: " + str(2**x - len(int_list)))

# print("Number of 2-input gates needed for SOP " + str(cal_gates_for_sop(minimize_sop(int_list,x)[0])))
# print("Number of 2-input gates needed for POS " + str(cal_gates_for_pos(convertToPOS(minimize_sop(getInverseRange(int_list,x),x)[0]))))