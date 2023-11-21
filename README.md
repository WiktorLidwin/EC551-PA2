# EC551-PA2

Input format: 
{
    "Number_of_LUTs": 100,
    "LutType" : 4,
    "FullyConnected" : false,
    "Partial_arch" : [2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2], 
    "Number_of_inputs" : 10,
    "Number_of_outputs" : 3,
    "Expressions" : [
        [["A", "B", "C", "D"], ["E", "F", "B"],["E", "F", "B'"] ,["E", "F", "A'"], ["G", "H"]],
        [["A", "B", "C", "D"], ["E", "F"], ["G", "I"]],
        [["A", "B", "C", "D"], ["G", "J"]]
    ]
}

Expressions will be minimized using Program 1.

Main2.py controlls all logic and outputs the results to a json file. This file is then read and the results are displayed on the winforms app in the Program2Display project.

The core logic works by constructing trees of the "simplified expressions" ex. H = abc + cd, H/a=1,c=1 = b+d

After each expression's tree is generated, the algorithm will look for overlaps and simplifications.

Each path is given a score based on how many LUTs it saves when considering all expressions.

Highest scoring LUTs are then created as the final product.

Architecture for partial is similar to Neural Network structure with the max LUTs per layer defined. 

Make sure to change paths in Main2.py and Program2Display/form1.cs
