
import queue

# PROBLEM 1 FUNCTIONS

"""
Purpose~ Adds all the string combinations, starting with each letter in the alphabet, of each length 1-5 that are nonfail
states to a dictionary as its keys. For those keys/states, determiines the state transitions on input a, b, c, and d, and
adds an array of those 4 transitions as the key's value. Returns the resulting dictionary (dfa).

Args~ alphabet = ['a', 'b', 'c', 'd']
      alphabetLen = 4
"""


def buildDfa(alphabet, alphabetLen):
    dfa = {'0': alphabet}  # initial state -> first transition
    fail = 'FAIL'  # fail state string
    dfa[fail] = [fail, fail, fail,
                 fail]  #fail state stays in fail state on any extra input

    for firstLetter in alphabet:
        dfa[firstLetter] = []  # 1letter state

        #combinations of length 2
        for secondLetterIdx in range(alphabetLen):
            twoLetterStr = firstLetter + alphabet[secondLetterIdx]
            dfa[firstLetter].append(twoLetterStr)
            dfa[twoLetterStr] = []

            #combinations of length 3
            for thirdLetterIdx in range(alphabetLen):
                threeLetterStr = twoLetterStr + alphabet[thirdLetterIdx]
                dfa[twoLetterStr].append(threeLetterStr)
                dfa[threeLetterStr] = []

                #combinations of length 4
                for fourthLetterIdx in range(alphabetLen):
                    fourLetterStr = threeLetterStr + alphabet[fourthLetterIdx]
                    # 4letter pattern fail check
                    if fourLetterStr[0] == fourLetterStr[1] == fourLetterStr[
                            2] == fourLetterStr[3]:
                        dfa[threeLetterStr].append(fail)
                    else:
                        dfa[threeLetterStr].append(fourLetterStr)
                        dfa[fourLetterStr] = []

                        #combinations of length 5
                        for fifthLetterIdx in range(alphabetLen):
                            fiveLetterStr = fourLetterStr + alphabet[
                                fifthLetterIdx]
                            # 5letter pattern fail check
                            if len(set(fiveLetterStr)) < 3:
                                dfa[fourLetterStr].append(fail)
                            else:
                                dfa[fourLetterStr].append(fiveLetterStr)

                                #combinations of length 6
                                fiveLettersA = fiveLetterStr + 'a'
                                fiveLettersB = fiveLetterStr + 'b'
                                fiveLettersC = fiveLetterStr + 'c'
                                fiveLettersD = fiveLetterStr + 'd'
                                #determine if 6letter combo fails. if so, add fail as transition, otherwise add new buffer
                                dfa[fiveLetterStr] = [
                                    fiveLettersA[1:]
                                    if len(set(fiveLettersA)) >= 4 else fail,
                                    fiveLettersB[1:]
                                    if len(set(fiveLettersB)) >= 4 else fail,
                                    fiveLettersC[1:]
                                    if len(set(fiveLettersC)) >= 4 else fail,
                                    fiveLettersD[1:]
                                    if len(set(fiveLettersD)) >= 4 else fail
                                ]
    return dfa


"""
Purpose~ From the dfa, constructs the initial prev dictionary and returns it. The prev dictionary will have
keys=stateNames such as 'aaa', 'bcdad', etc. The values will be the number of strings of length 0, accepted
by starting from the respective states. The only states that will be accepting are of length 5 and have at
least 1 transtion out of its four, that goes to a non-fail state. These values will get 1. States with 4 FAIL
transitions will get 0.

Args~ M = {'state0': [transition on A, ..., transition on D],
              ...,
             'statem': [transition on A, ..., transition on D]
            }
"""


def constructPrev(M):
    prev = {}
    for key in M:
        isNotAccepting = len(key) != 5 or all(transition == "FAIL"
                                              for transition in M[key])
        prev[key] = 0 if isNotAccepting else 1
    return prev


"""
Purpose~ From the prev dictionary, constructs the next dictionary and returns it. The next dictionary will have
keys= stateNames such as 'aaa', 'bcdad', etc. The value for a key will be the sum of the values in prev, at the
keys that the state transitions to.
Example ~ Say N_0 has a path to N_1 and N_(m-2) in the dfa.
          Then the value at N_0 in next{} will be N_0 + N_(m-2) from prev{}.
Dictionaries Visual ~
  prev = {                      next = {
          state: N_0(0),                state: N_0(1),
          state: N_1(0),                state: N_1(1),
          state: ...,                   state: ...,
          state: N_m(0)                 state: N_m(1)
         }                              }
Args~ M = {'state0': [transition on A, ..., transition on D],
              ...,
             'statem': [transition on A, ..., transition on D]
          }
      prev = {'state0': N_0(strlen),
              ...,
              'statem': N_m(strlen)
             }
"""


def constructNextFromPrev(M, prev):
    next = {}
    for key in prev:
        sumPrev = 0
        for transition in M[key]:
            sumPrev += prev[transition]
        next[key] = sumPrev
    return next


"""
Purpose~ Determines the number of strings of length n, accepted by the dfa. We will do this by keeping track of 2
dictionaries, prev and next. It will take 7 stages of transitions from prev to next to find this number. Prev and
next are discussed in detail in the descriptions for functions constructPrev() and constructNextFromPrev()
Args~ M = {'state0': [transition on A, ..., transition on D],
              ...,
             'statem': [transition on A, ..., transition on D]
            }
      n = String length entered by the user for which to check the number of strings of that length that are
      accepted by the DFA
"""


def getNumAcceptedStringsOfLengthN(M, n):
    prev = constructPrev(M)
    for i in range(n):
        next = constructNextFromPrev(M, prev)
        prev = next
    return next['0']


"""
Purpose~ Prints dfa states and transitions row by row
Args~ dfa = {'state0': [transition on A, ..., transition on D],
              ...,
             'statem': [transition on A, ..., transition on D]
            }
"""


def printDfaPairs(M):
    for key in M:
        print(key, M[key])

# PROBLEM 2 FUNCTIONS

#Builds the DFA and returns it
# From project instructions:
# "Create a DFA M = ⟨Q, Σ, δ, 0, F ⟩ where Q = {0,1,··· ,k − 1}, F = {0}, and δ(j,a) = (10 ∗ j + a)%k and call FindString with M and k as inputs.
def createDFA(k, S):
  dfa = {}
  for j in range(k): #states 0 through k-1
    dfa[j] = [] #row for state j in dictionary/dfa
    for a in S: #each permitted digit gets a column/transition
      dfa[j].append( (10*j + a) % k )
  return dfa





    
def findString(S, k):

  # Initialize a queue q
  Q = queue.Queue()

  # Initialize a Boolean array visited of size k
  # Initialize an integer array parent of size k
  # It's not listed as being initialized , but theres a label array
  # in the description of the alg that I'm initializing here as well -J
  # Not in a working state currently, but its at least a start. -J
  visited = []
  parent = []
  label = []
  for i in range(k):
    visited.append(False)
    parent.append(-1)
    label.append(-1)

  next = -1
  foundAccepting = False
  
  for s in range(len(S)):
    if not foundAccepting:
      next = (10 * 0 + S[s]) % k#M[0][s] # next = delta(0, D[s], k)
      if S[s] != 0:
        Q.put(next)
      if (S[s] != 0 and next == 0):
        foundAccepting = True
      visited[next] = True
      parent[next] = 0
      label[next] = S[s]

  while not Q.empty() and not foundAccepting:
    curr = Q.get()
    for s in range(len(S)):
      # if S[s] == 0:
      #  continue # representative of \ {0} ? -J
    # for each s in D \ { 0 } do:
      next = (10 * curr + S[s]) % k#M[curr][s] # next = delta(curr, s, k) // recall delta(q, r, k) = (10 * q + r) % k
      if (next == 0): # accepting state is reached
        parent[next] = curr
        label[next] = S[s]
        # print('breaking out of while loop')
        Q = queue.Queue()
        break # break out of the while loop
      elif not visited[next]:
        visited[next] = True
        parent[next] = curr
        label[next] = S[s]
        Q.put(next)


  

  if (next == 0 or foundAccepting): #reached the accepting state
    output = ''
    while True: 
      output = str(label[next]) + output #the S[i] that got us to the current state
      next = parent[next] #trace one state backward on our path
      if next == 0: #returned to the starting state. done tracing
        return output
        
  return 'No Solution'
    # trace the stting using parent pointers and concatenate the corresponding labels
    # output the reverse of the string
    # while not Q.empty():
    #   output = output + str(Q.get())
    # #output[::-1]
    # print(output)





  
#Prints the DFA, M, row by row in clear format
def printDfa(M):
  for state in M:
    print(f'State {state}: {M[state]}')

# Program Start

selection = input('Select which problem you would like to test: 1 or 2');
selection = int(selection)
print(selection)

if selection == 1:
    print('Problem 1:')
    alphabet = ['a', 'b', 'c', 'd']
    alphabetLen = len(alphabet)
    M = buildDfa(alphabet, alphabetLen)
    print(f"n = 6\tAnswer: {getNumAcceptedStringsOfLengthN(M, 6)}\n")
    print(f"n = 56\tAnswer: {getNumAcceptedStringsOfLengthN(M, 56)}\n")
    n = int(
        input(
            'Enter a string length to check how many strings of that length are accepted by the dfa: '
        ))
    print(f"\nn = {n}\tAnswer: {getNumAcceptedStringsOfLengthN(M, n)}")
elif selection == 2:
    print('Problem 2:')
    print(f"Test case 1:\nInputs: k = 26147, Digits permitted: 1, 3\nOutput: {findString([1, 3], 26147)}\n")
  
    testcase2 = findString([1], 198217)
    print(f"Test case 2:\nInputs: k = 26147, Digits permitted: 1\nOutput: (first & last 10 digits): {testcase2[0:10]}...{testcase2[-10:]}\nLength: {len(testcase2)}\n")
  
    print(f"Test case 3:\nInputs: k = 135, Digits permitted: 1 3 7\nOutput: {findString([1, 3, 7], 135)}\n")
  
    k = int(input('Enter a positive integer k: '))
    S = []
    digit = input('Enter a permitted digit (0-9) or q when finished:\n> ')
    while (digit.lower() != 'q'):
        digit = int(digit)
        if (digit not in S):
            S.append(digit)
            S.sort()
        digit = input('> ')
    print(f'S = {S}')
  
    # M = createDFA(k, S)
    # printDfa(M)
    N = findString(S, k)
    print('Output:', N)
    # print(len(N))


