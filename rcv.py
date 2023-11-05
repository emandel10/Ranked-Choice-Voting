'''
    Purpose: The pupose of this program is to design an algorithm capable
    of determining the winner of a rank-choice voting election
    Author: Ellis Mandel
    Email: ellismandel2025@u.northwestern.edu
    Date Last Modified: 10/26/2021
    Extra Credit: random index of lowest value (find_index_of_min)
'''
import random
def declare_winner(name:str, num_votes_for:int, num_votes_total:int) -> None:
    '''
     Function that prints an election winner and the percent of the vote they earned

        Parameters:
        ------------
        name: str -- candidate's name
        num_votes_for: int -- amount of votes candidate received
        num_votes_total: int -- total votes

        Returns:
        --------
        Prints candidate's name along with the percent of the vote they earned
        '''
    majority = round((num_votes_for/num_votes_total)*100, 2)
    print(f"Candidate {name} wins with {majority}% of the vote.")

def find_candidate(which_candidate:str, candidates:list) -> int:
    '''
     Function that determines whether a candidate is in a list of candidates

        Parameters:
        ------------
        which_candidate: str -- candidate's name
        candidates: int -- list of candidates

        Returns:
        --------
        Returns index if candidate is found in the list
        '''
    for i in range(len(candidates)):
        if which_candidate == candidates[i]:
            return i
    return None

def count_the_votes(candidates:list, votes_list:list) -> list:
    '''
     Function that determines how many votes a candidate got

        Parameters:
        ------------
        votes_liste: list -- list of votes
        candidates: list -- list of candidates

        Returns:
        --------
        Returns list of amount of votes each candidate earned
        '''
    new_list = [0]*(len(candidates))
    for x in range(len(votes_list)):
        index = find_candidate(votes_list[x], candidates)
        if votes_list[x] == candidates[index]:
            new_list[index]+=1
    return new_list

def determine_winner_simple_majority(vote_counts) -> int:
    '''
     Function that determines which candidate received majority of votes

        Parameters:
        ------------
        vote_counts: list -- list of votes

        Returns:
        --------
        Returns index of candidate who has majority of the vote
        '''
    total_votes = 0
    total_votes = sum(vote_counts)
    for i in range(len(vote_counts)):
        if round(vote_counts[i]/total_votes,1) > 0.5:
            return i
    return None

def simple_majority_vote(vote_counts:list) -> int:
    '''
     Function that determines the index of the winning candidate

        Parameters:
        ------------
        candidates: list -- list of candidate names
        choice_1: list -- list of integers with votes given to each candidate

        Returns:
        --------
        Returns index of the winner. If nobody wins, None is returned
        '''
    if are_all_equal(vote_counts):
        random_number = random.randint(0, len(vote_counts)-1)
        return random_number
    return determine_winner_simple_majority(vote_counts)

def sum(some_list:list) -> int:
    '''
     Function that returns the sum of all ints in list

        Parameters:
        ------------
        some_list: list - list of ints

        Returns:
        --------
        Returns sum (int) of everything in the list
        '''
    total = 0
    for x in range(len(some_list)):
        total += some_list[x]
    return total

def are_all_equal(vote_counts: list) -> bool:
    '''
     Function that detrmines whether all values in a list are equal

        Parameters:
        ------------
        vote_counts - list: list of votes

        Returns:
        --------
        Returns True if every index in the list contains the same value, otherwise it returns False
        '''
    number = vote_counts[0]
    for x in range(1, len(vote_counts)):
        if vote_counts[x] != number:
            return False
    return True


def copy_list(some_list: list) -> list:
    '''
     Function that makes a copy of a list

        Parameters:
        ------------
        some_list - list = list of any data type

        Returns:
        --------
        Returns the copy of the original parameter's list
        '''
    new_list = [0]*len(some_list)
    for x in range(len(some_list)):
        new_list[x] = some_list[x]
    return new_list
def simple_rcv(candidates: list, first_choice:list, second_choice:list, third_choice:list, debug: bool = False) -> None:
    '''
     Function that determines the winner, if there is one, for first round voting

        Parameters:
        ------------
        candidates: list - list of candidates
        first_choice: list - list of first choices
        second_choice: list- list of second choices
        third_choice: list - list of third choices
        debug: bool - boolean that, if true, calls print_slate

        Returns:
        --------
        None
        '''
    round1_candidates = copy_list(candidates)
    round1_top_choices = copy_list(first_choice)
    if debug:
        print_slate(round1_candidates, first_choice, second_choice, third_choice, 1)
    round1_vote_count = count_the_votes(round1_candidates, round1_top_choices)
    winner = simple_majority_vote(round1_vote_count)
    if winner != None:
        declare_winner(candidates[winner], round1_vote_count[winner], len(round1_top_choices))
        return

    lowest_index_1 = find_index_of_min(round1_vote_count)
    declare_eliminated(round1_candidates[lowest_index_1], round1_vote_count[lowest_index_1], len(round1_top_choices))
    round2_candidates = remove_candidate(round1_candidates, lowest_index_1)
    round2_top_choices = reassign_votes(round1_top_choices, second_choice, third_choice, round1_candidates[lowest_index_1], round2_candidates)
    if debug:
        print_slate(round2_candidates, round2_top_choices, second_choice, third_choice, 2)
    round2_vote_count = count_the_votes(round2_candidates, round2_top_choices)
    winner_round_2 = simple_majority_vote(round2_vote_count)
    if winner_round_2 != None:
        declare_winner(round2_candidates[winner_round_2], round2_vote_count[winner_round_2], len(round2_top_choices))
        return

    lowest_index_2 = find_index_of_min(round2_vote_count)
    declare_eliminated(round2_candidates[lowest_index_2], round2_vote_count[lowest_index_2], len(round2_top_choices))
    round3_candidates = remove_candidate(round2_candidates, lowest_index_2)
    round3_top_choices = reassign_votes(round2_top_choices, second_choice, third_choice, round2_candidates[lowest_index_2], round3_candidates)
    if debug:
        print_slate(round3_candidates, round3_top_choices, second_choice, third_choice, 3)
    round3_vote_count = count_the_votes(round3_candidates, round3_top_choices)
    winner_round_3 = simple_majority_vote(round3_vote_count)
    if winner_round_3 != None:
        declare_winner(round3_candidates[winner_round_3], round3_vote_count[winner_round_3], len(round3_top_choices))
        return

def print_slate(candidates: list, first_choice: list, second_choice: list, third_choice:list, round: int) -> None:
    '''
     Function that prints round number and candidates

        Parameters:
        ------------
        candidates: list - list of candidates
        first_choice: list - list of first choices
        second_choice: list- list of second choices
        third_choice: list - list of third choices
        round: int - current round

        Returns:
        --------
        None
        '''
    print(f"----- ROUND {round}-----")
    print(f"Candidates {candidates}")
    print(f"Choice 1 votes: {first_choice}")
    print(f"Choice 2 votes: {second_choice}")
    print(f"Choice 3 votes: {third_choice}")

def find_index_of_min(some_list:list) -> int:
    '''
     Function that returns lowest index in voting list

        Parameters:
        ------------
        some_list: list - list of integers

        Returns:
        --------
        Index where lowest value is located
        '''
    multiple_instances = []
    min_value = some_list[0]
    index = 0
    random_num = 0
    for x in range(len(some_list)):
        if some_list[x] < min_value:
            min_value = some_list[x]
            index = x
    for x in range(len(some_list)):
        if some_list[x] == min_value:
            multiple_instances.append(x)
    random_num = random.randint(0, len(multiple_instances)-1)
    return multiple_instances[random_num]
def declare_eliminated(name:str, num_votes_for:int, num_votes_total:int) -> None:
    '''
     Function that prints the name of the eliminated candidate and the amount of votes they received

        Parameters:
        ------------
        name: str - name of eliminated candidate
        num_votes_for - int: number of votes the candidate received
        num_votes_total - int: total number of votes

        Returns:
        --------
        None
        '''
    vote = round((num_votes_for/num_votes_total)*100, 2)
    print(f"Candidate {name} was eliminated with {vote}% of the vote.")
def remove_candidate(candidates: list, index: int) -> list:
    '''
     Function that removes a candidate from the candidate list

        Parameters:
        ------------
        candidates: list - list of candidates
        index - int: index where eliminated candidate is located in the list

        Returns:
        --------
        Updated list of candidates with eliminated candidate gone
        '''
    new_list = []
    for x in range(0, index):
        new_list.append(candidates[x])
    for x in range(index+1, len(candidates)):
        new_list.append(candidates[x])
    return new_list
def reassign_votes(first_choice:list, second_choice:list, third_choice:list, eliminated:str, new_candidates:list) -> list:
    '''
     Function that reassigns votes from eliminated candidates

        Parameters:
        ------------

        first_choice: list - list of first choices
        second_choice: list- list of second choices
        third_choice: list - list of third choices
        eliminated: str - name of eliminated candidate
        new_candidates: list - list of new candidates

        Returns:
        --------
        New list with votes transferred from the eliminated candidate
        '''
    new_first_choice = []
    for x in range(len(first_choice)):
        if first_choice[x] == eliminated:
            first_choice[x] = second_choice[x]
            if second_choice[x] == eliminated:
                first_choice[x] = third_choice[x]
                if third_choice[x] == eliminated:
                    first_choice[x] = None
    return first_choice

def main():
    print("Test find_index_of_min: ")
    new_list = [1, 3, 6, 5, 2]
    print("Expected: 0")
    value = find_index_of_min(new_list)
    print(f"Result: {value}")
    print("--------------------")
    print("Test find_index_of_min: ")
    new_list = [1, 3, 6, 5, 1]
    print("Expected: 0 or 4")
    value = find_index_of_min(new_list)
    print(f"Result: {value}")
    print("--------------------")
    print("Test find_index_of_min: ")
    new_list = [2]
    print("Expected: 0")
    value = find_index_of_min(new_list)
    print(f"Result: {value}")
    print("--------------------")
    print("Test declare_eliminated: ")
    candidate_name = "Jason"
    votes = 10
    total_votes = 200
    declare_winner(candidate_name, votes, total_votes)
    print("Expected: Candidate Jason was eliminated with 5.0% of the vote.")
    print("Result: ")
    declare_eliminated(candidate_name, votes, total_votes)
    print("------------------------------------------")
    print("Test declare_eliminated: ")
    candidate_name = "Alex"
    votes = 5
    total_votes = 30
    declare_eliminated(candidate_name, votes, total_votes)
    print("Expected: Candidate Alex was eliminated with 16.67% of the vote.")
    print("Result: ")
    declare_winner(candidate_name, votes, total_votes)
    print("------------------------------------------")
    print("Test remove_candidate: ")
    new_list = ["Jason", "Josh", "Alice", "Jen"]
    print("Expected: [Josh, Alice, Jen]")
    value = remove_candidate(new_list, 0)
    print(f"Result: {value}")
    print("------------------------------------------")
    print("Test remove_candidate: ")
    new_list = ["Jason", "Josh", "Alice", "Jen"]
    print("Expected: [Jason, Josh, Alice]")
    value = remove_candidate(new_list, 3)
    print(f"Result: {value}")
    print("------------------------------------------")
    print("Test remove_candidate: ")
    new_list = ["Jason", "Josh", "Mason", "Alice", "Jen"]
    print("Expected: [Jason, Josh, Alice, Jen]")
    value = remove_candidate(new_list, 2)
    print(f"Result: {value}")
    print("------------------------------------------")
    print("Test remove_candidate: ")
    new_list = ["Jason", "Josh", "Mason", "Alice", "Jen"]
    print("Expected: [Jason, Mason, Alice, Jen")
    value = remove_candidate(new_list, 1)
    print(f"Result: {value}")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Jake", "Sam"], ["Jake", "Jake", "Sam"],["Jake", "Josh", "Josh"], "Jake", value))
    print("Expected: [None, Josh, Sam]")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Josh", "Sam"], ["Jake", "Jake", "Sam"],["Josh", "Josh", "Josh"], "Jake", value))
    print("Expected: [Josh, Josh, Sam]")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Sam", "Sam"], ["Jake", "Jake", "Sam"],["Josh", "Josh", "Josh"], "Sam", value))
    print("Expected: [Jake, Jake, Josh]")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Jake", "Sam"], ["Jake", "Jake", "Sam"],["Josh", "Josh", "Josh"], "Jake", value))
    print("Expected: [Josh, Josh, Sam]")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Josh", "Sam"], ["Jake", "Jake", "x"],["Josh", "Josh", "Josh"], "Sam", value))
    print("Expected: [Jake, Josh, x]")
    print("------------------------------------------")
    print("Test reassign_votes: ")
    print(reassign_votes(["Jake", "Jake", "Jake"], ["Jake", "Jake", "Jake"],["Jake", "Jake", "Jake"], "Jake", value))
    print("Expected: [None, None, None]")
    simple_rcv(["a", "b", "c"], ["a", "c", "c", "c"], ["c", "c", "c", "c"], ["c", "c", "c", "c"])
def main_rcv_testing():

    # for the tests below, use any four names you like;
    # for "clean" printed output, you may want to make all entries the same
    #   width by including trailing spaces, as in "Alice" below;
    # include exactly four candidates

    names  = ["A", "B", "C", "D"]
    #names = ["Fay", "Jay", "May", "Ray"]
    #names = ["Alice   ", "Frankie ", "Franklin", "Snowball"]

    a,b,c,d = names  # short variables for (max 4) candidates will make list creation below convenient
    x = "x"         # x will indicate a vote that will not be considered in the process


    # <BEGIN> UNCOMMENT THIS BLOCK FOR THE INITIAL TESTING PHASE OF simple_rcv

    # candidate B wins 1st round
    candidates = [a,b,c]     # three candidates
    choice1    = [b,b,a,b,b] # b wins in round 1
    choice2    = [x,x,x,x,x]
    choice3    = [x,x,x,x,x]
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate B wins 1st round w/ 80%")

    print('=' * 70)

    # random candidate wins 1st round
    candidates = [a,b,c]       # use three candidates
    choice1    = [b,b,a,a,c,c] # randomly-selected winner in round 1
    choice2    = [x,x,x,x,x,x]
    choice3    = [x,x,x,x,x,x]
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Random candidate wins 1st round by lot w/ 33%")

    print('=' * 70)



    # candidate A wins 2nd round
    candidates = [a,b,c]      # three candidates
    choice1    = [a,b,c,a,b]  # c will be eliminated in round 1
    choice2    = [b,b,a,b,b]  # choice2[2] replaces choice1[2] --> a wins in round 2
    choice3    = [c,b,b,a,b]
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate A wins 2nd round w/ 60%")

    print('=' * 70)

    # candidate A or B wins 2nd round
    candidates = [a,b,c]        # three candidates
    choice1    = [a,b,c,a,b,b]  # c will be eliminated in round 1
    choice2    = [x,x,a,x,x,x]  # choice2[2] replaces choice1[2] --> a or b @ random in round 2
    choice3    = [x,x,x,x,x,x]
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Random candidate A or B wins 2nd round by lot w/ 50%")

    print('=' * 70)


    candidates = [a,b,c,d]            # four candidates
    choice1    = [a,a,b,b,b,c,c,c,d]  # d eleminated in round 1
    choice2    = [c,c,x,x,x,x,x,x,c]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [x,x,x,x,x,x,x,x,x]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate C wins 3rd round w/ 66.67%")

    print('=' * 70)



    # candidate C wins 3rd round w/ all choice2 replacements
    candidates = [a,b,c,d]            # four candidates
    choice1    = [b,b,b,b,b,c,c,c,d]  # d eleminated in round 1
    choice2    = [c,c,x,x,x,x,x,x,c]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [x,x,x,x,x,x,x,x,x]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate B wins 1st round w/ 55.56%")
    # <END> UNCOMMENT THIS BLOCK FOR THE THIRD TESTING PHASE OF simple_rcv
    print('=' * 70)



    # <END> UNCOMMENT THIS BLOCK FOR THE SECOND TESTING PHASE OF simple_rcv



    # <BEGIN> UNCOMMENT THIS BLOCK FOR THE THIRD TESTING PHASE OF simple_rcv

    #candidate C wins 3rd round w/ all choice2 replacements
    candidates = [a,b]            # four candidates
    choice1    = [a,a,b,b,a,a,b,b]  # d eleminated in round 1
    choice2    = [a,a,b,b,a,a,b,b]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [a,a,b,b,a,a,b,b]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate A or B wins 1st round w/ 50.00%")
    print('=' * 70)



    # candidate C wins 3rd round w/ all choice2 replacements
    candidates = [a,b,c]            # four candidates
    choice1    = [a,a,b,c,c,a,b,b]  # d eleminated in round 1
    choice2    = [b,a,a,b,b,c,a,a]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [c,c,c,a,a,b,c,c]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate B wins 2nd round w/ 62.5%")

    print('=' * 70)



    # candidate C wins 3rd round w/ all choice2 replacements
    candidates = [a,b,c]            # four candidates
    choice1    = [a,a,b,c,a,a,b,b]  # d eleminated in round 1
    choice2    = [x,x,x,b,x,x,x,x]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [x,x,x,x,x,x,x,x]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate A or B wins 2nd round w/ 50.00%")

    print('=' * 70)

    candidates = [a,b,c]            # four candidates
    choice1    = [a,a,b,b,b,c,c,c,c]  # d eleminated in round 1
    choice2    = [a,a,x,x,x,x,x,x,x]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [c,c,x,x,x,x,x,x,x]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate C wins 3rd round w/ 66.67%")

    print('=' * 70)

    candidates = [a,b,c,d]            # four candidates
    choice1    = [a,a,b,b,b,c,c,c,d,d]  # d eleminated in round 1
    choice2    = [a,a,x,x,x,x,x,x,d,d]  # choice2[-1] replaces choice1[-1] --> still no winner in round 2
    choice3    = [c,b,x,x,x,x,x,x,b,c]  # choice2[0:2] replaces choice1[0:2] --> c wins round 3
    simple_rcv(candidates, choice1, choice2, choice3, debug = True)  # use after debugging added
    print("\t Expected: Candidate C or B wins 3rd round w/ 50.00%")

main_rcv_testing()# UNCOMMENT THIS TO USE YOUR TESTS IN YOUR main
# main_rcv_testing()   # UNCOMMENT THIS TO USE THE PROVIDED TESTS FOR simple_rcv
