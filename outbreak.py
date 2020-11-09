'''
Created on Oct 26, 2020

@author: ashyasingh
'''
import sys
import random

############################

# DO NOT CHANGE THIS PART!!

############################

def readGraph(input_file):
    with open(input_file, 'r') as f:
        raw = [line.split(',') for line in f.read().splitlines()]

    N = int(raw[0][0])
    sin = raw[1]
    s = []
    for st in sin:
        s.append(int(st))
    adj_list = []
    for line in raw[2:]:
        if line == ['-']:
            adj_list.append([])
        else:
            adj_list.append([int(index) for index in line])
    return N, s, adj_list

def writeOutput(output_file, prob_infect, avg_day):
    with open(output_file, 'w') as f:
        for i in prob_infect:
            f.write(str(i) + '\n')
        f.write('\n')
        for i in avg_day:
            f.write(str(i) + '\n')



def Run(input_file, output_file):
    N, s, adj_list = readGraph(input_file)
    prob_infect, avg_day =   model_outbreak(N, s, adj_list)
    writeOutput(output_file, prob_infect, avg_day)


def  BFS(N, s, adj_list):
    # We give you three variables:
    # N = the number of vertices in the graphfile
    # s = the start node
    # adj_list = a list of lists:
    # The 0th item is a list of the vertices adjecent to vertex 0.
    # The 1st item is a list of the vertices adjecent to vertex 1.
    # The 2nd item is a list of the vertices adjecent to vertex 2.
    # And so forth.

    # We also give you a variable called level, 
    # which is a list containing N x's as placeholders:
    level = ['x']*N
    # You will write the BFS level of each node here.
    # The 0th item will be the level of vertex 0 in your BFS tree.
    # The 1st item will be the level of vertex 1.
    # Et cetera.

    # PLEASE DO NOT SUBMIT CODE WITH PRINT STATEMENTS.
    # IT WILL MESS UP THE AUTOGRADER.

    ############################

    vi = [False] * N
    queue = []

    for i in s:
        queue.append(i)
        vi[i] = True
        level[i] = 0

    while queue:
        re = queue.pop(0)

        for i in adj_list[re]:
            if vi[i] == False:
                vi[i] = True
                level[i] = level[re] + 1
                queue.append(i)

    return level



def GenRndInstance(s, adj_list, p):
    edges = []
    for i in adj_list:
        e = []
        for j in i:
            active = random.random()
            if active <= p:
                e.append(j)
        edges.append(e)
    edges.append(s)
    return edges

#######################################

# WRITE YOUR SOLUTION IN THIS FUNCTION

########################################

def model_outbreak(N, s, adj_list):
    # Again, you are given N, s, and the adj_list
    # You can also call your BFS algorithm in this function,
    # or write other functions to use here.
    # Return two lists of size n, where each entry represents one vertex:
    prob_infect = [0] * N
    # the probability that each node gets infected after a run of the experiment
    avg_day = ['inf'] * N
    # the average day of infection for each node
    # (you can write 'inf' for infinity if the node is never infected)
    # The code will write this information to a single text file.
    # If you do not name this file at the command prompt, it will be called 'outbreak_output.txt'.
    # The first N lines of the file will have the probability infected for each node.
    # Then there will be a single space.
    # Then the following N lines will have the avg_day_infected for each node.
    p = [0.1, 0.3, 0.5, 0.7]
    for i in range(100):
        G_i = GenRndInstance(s, adj_list, p[3])
        level = BFS(N, s, G_i)
        
        for i in range(N):
            if(level[i] == 'x'):
                continue
            else:
                if(prob_infect[i] == 0):
                    avg_day[i] = 0
                prob_infect[i] += 1
                avg_day[i] += level[i]

    for i in range(N):
        if(prob_infect[i] == 0):
            continue
        else:
            avg_day[i] /= prob_infect[i]
            prob_infect[i] = float(prob_infect[i]) / 100

    return prob_infect, avg_day



############################

# DO NOT CHANGE THIS PART!!

############################


# read command line arguments and then run
def main(args=[]):
    filenames = []

    #graph file
    if len(args)>0:
        filenames.append(args[0])
        input_file = filenames[0]
    else:
        print()
        print('ERROR: Please enter file names on the command line:')
        print('>> python outbreak.py graph_file.txt output_file.txt')
        print()
        return

    # output file
    if len(args)>1:
        filenames.append(args[1])
    else:
        filenames.append('outbreak_output.txt')
    output_file = filenames[1]

    Run(input_file, output_file)


if __name__ == "__main__":
    main(sys.argv[1:])
