import math
from anytree import NodeMixin, RenderTree
from MinimalSOP import minimize_sop

class MyNode(NodeMixin):
    def __init__(self, value, description,name, extra, parent=None, children=None):
        super(MyNode, self).__init__()
        self.value = value
        self.description = description
        self.name = name
        self.extra = extra
        self.parent = parent
        if children:
            self.children = children



def createNewEquationWithVariableSubstitution(func, var, value):  
    newfunc = []
    for term in func:
        found = False
        newterm = []
        for v in term:
           if(v == var):
             found = True
             if(value == 0):
               newterm = 0
               break
             elif(len(term) == 1):
               newterm = 1
               break
           elif(v == var+"'"):
             found = True
             if(value == 1):
               newterm = 0
               break
             elif(len(term) == 1):
               newterm = 1
               break
           else:
             newterm.append(v)
        if(found):
          if(newterm == 1  ):
            return 1 #always true
          elif(newterm == 0):
            temp = 0
          else:
            newfunc.append(newterm)
        else:
          newfunc.append(term)
    if(len(newfunc) == 0):
      return 0
    return newfunc

def convert_sop_equation(sop_equation):
    variables = set()
    binary_string = ''
    
    for term in sop_equation:
        for literal in term:
            if(literal[-1] == "'"):
                variables.add(literal[:-1])
            else:
                variables.add(literal)
    
    sorted_variables = sorted(variables)
    num_rows = 2 ** len(sorted_variables)

    for i in range(num_rows):
        case = format(i, f'0{len(sorted_variables)}b')

        found_match = False
        for term in sop_equation:
            term_match = True
            for literal in term:
                variable = literal[:-1]
                if(literal[-1] == "'"):
                    variable = literal[:-1]
                else:
                    variable = literal
                inverse = literal[-1] == "'"

                if (inverse and case[sorted_variables.index(variable)] == '0') or \
                   (not inverse and case[sorted_variables.index(variable)] == '1'):
                    t = 0
                else:
                   term_match = False
                   break

            if term_match:
                found_match = True
                break

        binary_string += '1' if found_match else '0'
    return (",".join(sorted_variables), binary_string)
            
def convertVars(new_vars, function):
#    print("hhsds")
#    print(new_vars)
#    print(function)
   new_func = []
   for term in function:
      newterm = []
      for old_var in term:
        if(old_var[-1] == "'"):
           newterm.append(new_vars[ord(old_var[0])-65] + "'")
        else:
            newterm.append(new_vars[ord(old_var)-65])
      new_func.append(newterm)
   return new_func      


def makeBranch(b, name, var, child):
    # print(name)
    # print(b)
    nums = []
    count = 0
    while(count < len(b[1])):
        if(b[1][count] == '1'):
            nums.append(count)
        count += 1
    # print(nums)
    newsop = convertVars(b[0].split(","), minimize_sop(nums, len(b[0].split(","))))
    # print(minimize_sop(nums, len(b[0].split(","))))
    inner_func = Function(newsop, name  )
    return inner_func.createTree(child)
    

class Function:
  def __init__(self, original_function, name):
    self.original_function = original_function
    self.current_functions = [original_function]
    self.name = name
    self.gates = []
    self.root = None

  def createTree(self, parent=None):
    self.root = MyNode(0,str(convert_sop_equation(self.original_function)), self.name,self.original_function, parent=parent)
    
    


    temp = {}
    for term in self.original_function:
        for var in term:
            temp[var] = 1
    if(len(temp) <= luttype):
       return self.root
    for var in temp:
        var_child = MyNode(0, None, var,None,  parent=self.root)
        

        x1 = createNewEquationWithVariableSubstitution(self.original_function, var, 0)
        x2 = createNewEquationWithVariableSubstitution(self.original_function, var, 1)
        b1 = 0
        b2 = 0
        if ((x1 == 1 or x1 == 0) and (x2 == 1 or x2 == 0)):
           print("Very bad")
        elif (x1 == 1 or x1 == 0):
            
            b1 = convert_sop_equation(x2)


            c= makeBranch(b1,self.name + "/"+ var +":1", var, var_child)
            
            var_child2 = MyNode(math.pow(2,(self.getCurrentLevel()-luttype))-1, None, self.name + "/"+ var +":0", None, parent=var_child)

        elif (x2 == 1 or x2 == 0):
            b1 = convert_sop_equation(x1)
            c = makeBranch(b1,self.name + "/"+ var +":0", var, var_child)
            
            
            var_child2 = MyNode(math.pow(2,(self.getCurrentLevel()-luttype))-1, None, self.name + "/"+ var +":1",None,  parent=var_child)

        else:
            b1 = convert_sop_equation(x1)
            c = makeBranch(b1,self.name + "/"+ var +":0", var, var_child)
            
            
            
            b2 = convert_sop_equation(x2)
            c2 = makeBranch(b2,self.name + "/"+ var +":1", var, var_child)
            
            
        
        # branches.add((self.name, set(b1),set(b2), var))  
    return self.root

  
  def getCurrentLevel(self):
    temp = {}
    for term in self.current_functions[0]:
      for var in term:
        temp[var] = 1
    return len(temp) 





# r = F3.createTree()

# for pre, fill, node in RenderTree(r):
#     print(f"{pre}Value: {node.value}, Description: {node.description}, Name: {node.name}")
    
def search_by_description(node, description):
    result = []
    
    if node.description == description:
        result.append(node)
    
    for child in node.children:
        result.extend(search_by_description(child, description))
    
    return result


def findOverlaps(node, root2):

    if(node.description == None):
       t = "skip"
       for child in node.children:
          findOverlaps(child, root2)
       return
    else:
       r = search_by_description(root2, node.description)
       if (len(r)> 0):
          if (len(node.description.split(",")) > luttype):
            node.value += math.pow(2,(len(node.description.split(","))-luttype))-1 
          else:
             node.value += 1
    for child in node.children:
          findOverlaps(child, root2)





def find_node_with_greatest_value(node, excluded_nodes):
    # Initialize variables to keep track of the node with the greatest value
    current_max_node = None
    max_value = 0

    # Perform depth-first search to traverse the tree
    stack = [node]
    while stack:
        current_node = stack.pop()
        
        # Skip the current node if it is in the excluded nodes list
        if current_node in excluded_nodes:
            continue
        
        # Update the current maximum node and value if necessary
        if current_node.value > max_value:
            max_value = current_node.value
            current_max_node = current_node
        
        # Add the children of the current node to the stack
        stack.extend(current_node.children)
    
    return current_max_node
   
def propagate_values(node):
    if not node.children:
        return node.value

    child_values = []
    for child in node.children:
        child_values.append( propagate_values(child))
    if(node.description == None):
        node.value = max(child_values)
    else:
       node.value += sum(child_values)
    return node.value







def find_max_value_node_2d(node_list):
    max_node = None
    max_value = float('-inf')

    for row in node_list:
        for node in row:
            if node.value > max_value:
                max_value = node.value
                max_node = node

    return max_node


def find_max_child(node):
    if not node.children:
        return None

    max_child = None
    max_value = float('-inf')

    for child in node.children:
        if child.value > max_value:
            max_child = child
            max_value = child.value

    return max_child


# def print_path(node):
#     print(node.value, end=" ")
#     if node.children:
#         max_child = find_max_child(node)
#         print_path(max_child)
# print_path(trees[0])


class LUT:
  def __init__(self, name, function, func_input, output, desc, layer):
    self.name = name
    self.function = function
    self.func_input = func_input
    self.output = output
    self.desc = desc
    self.layer = layer

def findGate(gates, func):
   for g in gates:
      if(g.function == func):
         return g
   return None
def getGates(tree, lut, gates):
    if not (tree.children):
       if (tree.description != None):
          lut.func_input = tree.description[2:].split(",")[:-1]
       elif (tree.parent.description != None):
          lut.func_input = tree.parent.description[2:].split(",")[:-1]
    #    else:
        #  print("DFHSHDISHDUI")
        #  print(tree.name) 
        #  print(tree.parent.name) 
    #    print(tree)
       return
    n = find_max_child(tree)
    n1 = n.children[0]
    n2 = n.children[1]

    r1 = None
    r2 = None


    if(n2.description != None):
        layer = len(n1.description.split(","))-luttype
        layer = 0 if layer <= 0 else layer
    else:
       layer = 0
        
    g1 = findGate(gates,n1.description )
    if (g1):
        r1 = g1
    else:
        r1 = LUT(n1.name, n1.description, [],n1.name, n1.extra,layer) 
        gates.append(r1)
        getGates(n1, r1,gates)


    layer2 = 0
    if(n2.description != None):
       
        layer2 = len(n2.description.split(","))-luttype
        layer2 = 0 if layer2 <= 0 else layer2
    else:
       layer2 = 0

    g2 = findGate(gates,n2.description )
    if (g2):
        r2 = g2
    else:
        r2 = LUT(n2.name, n2.description, [],n2.name, n2.extra, layer2) 
        gates.append(r2)
        getGates(n2, r2,gates)

    
    lut.func_input = [r1,r2]
    

def getLUTS(original_functions): 
    trees = []
    
    for f in original_functions:
        trees.append(f.createTree())
    for i in range(len(trees)):
        tree = trees[i]
        for j in range(0,len(trees)):
            if (i != j):
                findOverlaps(tree,trees[j])

    for i in range(len(trees)):
        tree = trees[i]
        propagate_values(tree)    
        
    gates = []
    for i in range(len(trees)):
        tree = trees[i]
        layer = len(tree.description.split(","))-luttype
        layer = 0 if layer <= 0 else layer
        lut = LUT("F"+str(i),"IDK", [], "f"+str(i), tree.extra,  layer)
        gates.append(lut)
        getGates(tree,lut,gates)
    return gates
    
# print(gates)
# print("layer 5")
# for g in gates:
#    if (g.layer == 5):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")

# print("layer luttype")
# for g in gates:
#    if (g.layer == luttype):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")
# print("layer 3")
# for g in gates:
#    if (g.layer == 3):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")
# print("layer 2")
# for g in gates:
#    if (g.layer == 2):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")
# print("layer 1")
# for g in gates:
#    if (g.layer == 1):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")
# print("layer 0")
# for g in gates:
#    if (g.layer == 0):
#       print(f"function: {g.function}, layer: {g.layer}, Name: {g.name}")
# print(len(gates))

import json

def convertLutToJson(lut):
   count = 0
   newList = []
   
   for lut in luts:
      inputs = []
      if (len(lut.func_input) == 0 or lut.function == None or lut.desc == None) :
         continue
      for i in lut.func_input:
            if (isinstance(i, LUT)):
                inputs.append(i.name)
            else:
                inputs.append(i)
    #   print(inputs)
      newLut = {
       "Layer": lut.layer,
       "Name" : lut.name,
       "ID" : count,
       "Details": lut.function,
       "Function" : lut.desc,
       "Inputs": inputs
      }
      newList.append(newLut)
      count +=1

   return check_arch(newList)
import copy
def check_arch(luts):
   if not(fullyConnected):
      new_list = []
      layer = 0
      new_layer = 0
      new_layer_count = 0
      while(len(new_list) != len(luts)):
        print(len(new_list))
        for i in luts:
            if (i["Layer"] == layer):
                if(partial_arch[new_layer] > new_layer_count):
                    x = copy.deepcopy(i)
                    x["Layer"] = new_layer
                    new_list.append(x)
                    new_layer_count+=1
                else:
                    new_layer += 1
                    x = copy.deepcopy(i)
                    x["Layer"] = new_layer
                    new_list.append(x)
                    new_layer_count=1
        layer +=1
        new_layer +=1
        new_layer_count = 0
      return new_list
   else:
      return luts
def createJsonFile(filename, numberofluts, luttype, fullyConnected, partial_arch, numberofinputs, numberofoutputs, expressions,luts):
    
    
    data = {
        'Number_of_LUTs': numberofluts,
        'LutType': luttype,
        'FullyConnected': fullyConnected,
        'Partial_arch' : partial_arch,
        'Number_of_inputs': numberofinputs,
        'Number_of_outputs': numberofoutputs,
        'Expressions' : expressions,
        'LUTs' : convertLutToJson(luts),
        
    }

    # Save the dictionary as a JSON file
    with open(filename, 'w') as f:
        json.dump(data, f)

numberofluts = 0
luttype = 4
fullyConnected = True
partial_arch = []
numberofinputs = 0
numberofoutputs = 0
expressions = []
luts = []


def loadInput():
   global numberofluts
   global luttype
   global fullyConnected
   global partial_arch
   global numberofinputs
   global numberofoutputs
   global expressions

   with open('input.json', 'r') as f:
    data = json.load(f)
    numberofluts = data['Number_of_LUTs']
    luttype = data['LutType']
    fullyConnected = data['FullyConnected']
    partial_arch = data['Partial_arch']
    numberofinputs = data['Number_of_inputs']
    numberofoutputs = data['Number_of_outputs']
    expressions = data['Expressions']
    new_expressions = []
    for e in expressions:
        b = convert_sop_equation(e)
        nums = []
        count = 0
        while(count < len(b[1])):
            if(b[1][count] == '1'):
                nums.append(count)
            count += 1
        newsop = convertVars(b[0].split(","), minimize_sop(nums, len(b[0].split(","))))
        new_expressions.append(newsop)
    expressions = new_expressions
    print(expressions)

loadInput()

original_functions = []

for i in range(len(expressions)):
   original_functions.append(Function(expressions[i],"F"+str(i+1)))
# F1 = Function( [["A", "B", "C", "D"], ["E", "F"], ["G", "H"]],"F1")
# F2 = Function( [["A", "B", "C", "D"], ["E", "F"], ["G", "I"]],"F2")
# F3 = Function( [["A", "B", "C", "D"], ["G", "J"]],"F3")

# original_functions.append(F1)
# original_functions.append(F2)
# original_functions.append(F3)
luts = getLUTS(original_functions)

createJsonFile('output.json', numberofluts, luttype, fullyConnected, partial_arch, numberofinputs, numberofoutputs, expressions,luts)
print(str(len(convertLutToJson(luts))*100.0/numberofluts) +"% of Luts used")
connections = 0
partialconnections = partial_arch[0]
for i in range(len(partial_arch)-1):
   partialconnections += (partial_arch[i] + numberofinputs) * partial_arch[i+1]
totalconnections = (numberofluts + numberofinputs) * (numberofluts + numberofinputs+1)/2 if fullyConnected else partialconnections
for i in convertLutToJson(luts):
   connections += len(i["Inputs"])
print(str(connections*100.0/totalconnections) +"% of Connections used")
print(str(connections*2*8+len(convertLutToJson(luts)*16)) +" Total memory")