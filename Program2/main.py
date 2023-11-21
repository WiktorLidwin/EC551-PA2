from MinimalSOP import minimize_sop


class Network:
  def __init__(self, name, function, func_input, output):
    self.name = name
    self.function = function
    self.func_input = func_input
    self.output = output

class SOP:
  def __init__(self, SOP):
    self.SOP = SOP

  def getLevel():
    temp = {}
    for term in SOP:
      for var in term:
        temp[var] = 1
    return len(temp)


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
                    term_match = False
                    break

            if term_match:
                found_match = True
                break

        binary_string += '1' if found_match else '0'
    return (tuple(sorted_variables), binary_string)
            
             

class Function:
  def __init__(self, original_function, name):
    self.original_function = original_function
    self.current_functions = [original_function]
    self.name = name
    self.gates = []

  def getBranches(self):
    branches = set()
    for func in self.current_functions:
        temp = {}
        for term in func:
            for var in term:
                temp[var] = 1
        for var in temp:
          x1 = createNewEquationWithVariableSubstitution(func, var, 0)
          x2 = createNewEquationWithVariableSubstitution(func, var, 1)
          b1 = 0
          b2 = 0
          if (x1 == 1 or x1 == 0):
            b1 = convert_sop_equation(x2)
            b2 = convert_sop_equation(x2)
          
          elif (x2 == 1 or x2 == 0):
            b1 = convert_sop_equation(x1)
            b2 = convert_sop_equation(x1)
          else:
            b1 = convert_sop_equation(x1)
            b2 = convert_sop_equation(x2)
          
          branches.add((self.name, set(b1),set(b2), var))
    return branches
  def getCurrentLevel(self):
    temp = {}
    for term in self.current_functions[0]:
      for var in term:
        temp[var] = 1
    return len(temp) 

class LUT4:
  def __init__(self, name, function, func_input, output, desc):
    self.name = name
    self.function = function
    self.func_input = func_input
    self.output = output
    self.desc = desc

# def getLevelOfFunction( func):
#   return 0
    
# def getBranches(func):
#   return [] #(source, branch_pair1, branch_pair2)

def convertVars(new_vars, function):
   new_func = []
   for term in function:
      newterm = []
      for old_var in term:
        newterm.append(new_vars[ord(old_var)-65])
      new_func.append(newterm)
   return new_func


def findFunction(functions, name):
  for f in functions:
    if f.name == name:
      return f
  return None

original_functions = []

F1 = Function( [["A", "B", "C", "D"], ["E", "F"], ["G", "H"]],"F1")
F2 = Function( [["A", "B", "C", "D"], ["E", "F"], ["G", "I"]],"F2")
F3 = Function( [["A", "B", "C", "D"], ["G", "J"]],"F3")


original_functions.append(F1)
original_functions.append(F2)
original_functions.append(F3)

current_functions = {}

current_level_dict = {}
created_gates = {}
maxLevel = 10
while(maxLevel > 4):
  while(True): #for one level...
    
    #find max level functions
    maxLevel = 0
    maxLevelFunctions = []
    for f in original_functions:
        funcLevel = f.getCurrentLevel()
        if(funcLevel > maxLevel):
            maxLevel = funcLevel
            maxLevelFunctions = []
        if (maxLevel == funcLevel):
            maxLevelFunctions.append(f)
    
    print(maxLevel)

    if(maxLevel == 4):
        print("Max LEVEL!!!!")
        break

    #get there branches
    all_branches = []
    for f in maxLevelFunctions:
        branches = f.getBranches()
        for b in branches:
            if b[1] not in current_level_dict:
                current_level_dict[b[1]] = 0
            current_level_dict[b[1]] += 1
            if b[2] not in current_level_dict:
                current_level_dict[b[2]] = 0
            current_level_dict[b[2]] += 1
        all_branches.append += branches


    #find best branch
    max_count = 0
    max_count_content =[]
    for b in all_branches:
        branch_count = current_level_dict[b[1]] + current_level_dict[b[2]]
        if( branch_count >max_count ):
            max_count = branch_count
            max_count_content = []
        if(branch_count == max_count):
            max_count_content.append(b)
    
    #no good branches... look at next level
    if(max_count <= 2):
        #todo
        for f in maxLevelFunctions:
            func.current_functions = []
        for b in all_branches:
            func = findFunction(b[0])
            nums = []
            count = 0
            while(count < len(b[1][1])):
                if(b[1][1][count] == 1):
                    nums.append(count)
            count += 1
            newsop = convertVars(b[1][0], minimize_sop(nums, len(b[1][0])))
            
            func.current_functions += newsop

        break
    
    #found good branches!

    conflict_check = {}
    for b in max_count_content:
       func = findFunction(b[0])
       if func.name not in conflict_check:
          conflict_check[func.name] = 0
       conflict_check[func.name] +=1
    
    skip_vals = []

    for x in conflict_check:
       if(conflict_check[x] > 1):
          skip_vals.append(x)
    

    for b in max_count_content:
        func = findFunction(b[0])
        
        if(func.name in skip_vals):
            nums = []
            count = 0
            while(count < len(b[1][1])):
                if(b[1][1][count] == 1):
                    nums.append(count)
            count += 1
            newsop = convertVars(b[1][0], minimize_sop(nums, len(b[1][0])))
            
            func.current_functions += newsop

            continue


        func.current_functions = []
        key1 = (b[1])
        gate1 = None
        if(key1 not in created_gates):
            gate1 = LUT4("name",b[1][1],b[1][0], b[3],b[0])
            created_gates[key1] = gate1
        else:
            gate1 = created_gates[key1]
            gate1.desc += " "+ b[0]
        
        nums = []
        count = 0
        while(count < len(b[1][1])):
            if(b[1][1][count] == 1):
                nums.append(count)
        count += 1
        newsop = convertVars(b[1][0], minimize_sop(nums, len(b[1][0])))

        func.gates += [gate1]
        func.current_functions += newsop

        key2 = (b[2])
        gate2 = None
        if(key2 not in created_gates):
            gate2 = LUT4()
            created_gates[key2] = gate2
        else:
            gate2 = created_gates[key2]
        

        nums = []
        count = 0
        while(count < len(b[2][1])):
            if(b[2][1][count] == 1):
                nums.append(count)
        count += 1
        newsop = convertVars(b[2][0] ,minimize_sop(nums, len(b[2][0])))

        func.gates += [gate2]
        func.current_functions += newsop


    t = 9
        
print(created_gates)