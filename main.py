from bs4 import BeautifulSoup


class States:

    def __init__(self, isFinal=False, isInitial=False, name=None):
        self.isFinal = isFinal
        self.isInitial = isInitial
        self.name = name
        self.transitions = {}

    def setNextState(self, alph, state):
        self.transitions[alph] = state

    def getNextState(self, alph):
        return self.transitions[alph]

    def getName(self):
        return self.name

    def getFinalStatus(self):
        return self.isFinal

    def getInitialStatus(self):
        return self.isInitial


with open('automata2.xml', 'r') as f:
    data = f.read()

soup = BeautifulSoup(data, 'xml')

Alphabets = soup.find('Alphabets')
number_of_alphabets = int(Alphabets.get('numberOfAlphabets'))
alphabet_tags = Alphabets.find_all('alphabet')
alphabets = []
i = 0
while i < number_of_alphabets:
    alphabets.append(alphabet_tags[i].get('letter'))
    i += 1

States_tag = soup.find('States')
number_of_states = int(States_tag.get('numberOfStates'))
state_tags = States_tag.find_all('state')
states = []
i = 0
while i < number_of_states:
    states.append(state_tags[i].get('name'))
    i += 1

initialState_tag = States_tag.find('initialState')
initialState = initialState_tag.get('name')

FinalStates_tag = soup.find('FinalStates')
number_of_final_states = int(FinalStates_tag.get('numberOfFinalStates'))
finalState_tags = FinalStates_tag.find_all('finalState')
finalStates = []
i = 0
while i < number_of_final_states:
    finalStates.append(finalState_tags[i].get('name'))
    i += 1

stateObj = []
i = 0
while i < number_of_states:
    if states[i] == initialState:
        isInitial = True
    else:
        isInitial = False

    j = 0
    isFinal = False
    while j < number_of_final_states:
        if states[i] == finalStates[j]:
            isFinal = True
            break
        j += 1

    obj = States(isFinal, isInitial, states[i])
    if obj.getInitialStatus():
        initialState_obj = obj
    stateObj.append(obj)
    i += 1

Transitions_tag = soup.find('Transitions')
number_of_trans = int(Transitions_tag.get('numberOfTrans'))
transition_tags = Transitions_tag.find_all('transition')
i = 0
while i < number_of_trans:
    source = transition_tags[i].get('source')
    destination = transition_tags[i].get('destination')
    label = transition_tags[i].get('label')
    j = 0
    objs_found = 0
    destObj = States()
    sourceObj = States()
    while j < number_of_states and objs_found != 2:
        if stateObj[j].getName() == source:
            sourceObj = stateObj[j]
            objs_found += 1

        if stateObj[j].getName() == destination:
            destObj = stateObj[j]
            objs_found += 1
        j += 1

    sourceObj.setNextState(label, destObj)
    i += 1

while True:
    string = input('Enter a string(type "end" to exit): ')
    if string == 'end':
        break
    currentState = initialState_obj
    i = 0
    alph_exists = True
    trans_available = True
    while i < len(string):
        if string[i] not in alphabets:
            alph_exists = False
            break

        currentState = currentState.getNextState(string[i])

        if currentState is None:
            trans_available = False
            break

        i += 1

    if currentState.getFinalStatus() and alph_exists and trans_available:
        print('The input string is accepted.')
    else:
        print('The input string is not accepted.')
