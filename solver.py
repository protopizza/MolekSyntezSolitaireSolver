import copy
from game_api import GameApi
from queue import PriorityQueue

USE_SAMPLE = False
TIMES_TO_SOLVE = 10
STATES_SEARCH_LIMIT = 50000

# Cheated card represented by negative equivalents, e.g. -6 is a cheated 6
CARD_TO_NUMBER = {
    "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "v": 11, "d": 12, "k": 13, "t": 14
}
NUMBER_TO_CARD = {v: k for k, v in CARD_TO_NUMBER.items()}

CARD_ORDER = ["t", "k", "d", "v", "10", "9", "8", "7", "6"]
NUMBER_ORDER = [CARD_TO_NUMBER[x] for x in CARD_ORDER]

SAMPLE_STACKS = [['6', '10', 'v', '9', '8', 't'], ['10', 'd', 'v', 'k', '7', 'k'], ['6', 't', '9', '7', '6', 'd'], ['d', 'k', '10', 't', 't', '8'], ['8', '9', 'v', '9', '7', '10'], ['v', '8', 'd', '6', 'k', '7']]

class GameState:
    def __init__(self, stacks, moves_taken = []):
        self.stacks = stacks
        self.moves_taken = moves_taken

    def __str__(self):
        return '\n'.join(' '.join(map(str, x)) for x in self.stacks)

    def __lt__(self, other):
        return isinstance(other, GameState) and self.get_score() < other.get_score()

    def __hash__(self):
        new_stacks = copy.deepcopy(self.stacks)
        new_stacks.sort()

        return hash(str(new_stacks))

    def __eq__(self, other):
        return isinstance(other, GameState) and self.__hash__() == other.__hash__()

    def is_won(self):
        for stack in self.stacks:
            if not stack or self.is_stack_complete(stack):
                continue
            return False
        return True

    def is_no_legal_moves(self):
        return len(self.find_legal_moves()) == 0

    def is_stack_complete(self, stack):
        return stack == NUMBER_ORDER

    def is_cards_ordered(self, cards):
        for index, item in enumerate(cards):
            if index == len(cards) - 1:
                break
            if cards[index + 1] != item - 1:
                return False

        return True

    def find_max_substack(self, stack):
        if stack[-1] < 0:
            return stack[-1:], len(stack) - 1

        for index, item in enumerate(stack):
            substack = stack[index:]
            if self.is_cards_ordered(substack):
                return substack, index
        return [], 0

    def get_num_complete_stacks(self):
        return len([stack for stack in self.stacks if self.is_stack_complete(stack)])

    def get_num_empty_stacks(self):
        return len([stack for stack in self.stacks if not stack])

    def is_stack_cheated(self, stack):
        if not stack:
            return False
        if stack[-1] < 0:
            return True
        return False

    def get_num_stacks_cheated(self):
        return [self.is_stack_cheated(stack) for stack in self.stacks].count(True)

    '''
    A legal move contains a tuple of (source move, target move, is_cheated)
    Each move element consists of a tuple of (stack index, card index)
    '''
    def find_legal_moves(self):
        legal_moves = []
        for index, stack in enumerate(self.stacks):
            if not stack:
                continue
            if self.is_stack_complete(stack):
                continue
            max_substack = self.find_max_substack(stack)

            # Could also consider moving the smaller stacks within a substack ?

            destinations = self.find_destinations(max_substack[0], index, self.stacks)
            for destination in destinations:
                source_move = (index, max_substack[1])
                target_move = (destination[0], max(len(self.stacks[destination[0]]) - 1, 0))
                legal_moves.append(((source_move, target_move), destination[1]))

        return legal_moves

    '''
    Destinations are a tuple of destination stack index, and True if it's a cheated placement
    '''
    def find_destinations(self, source_stack, source_stack_index, all_stacks):
        destinations = []

        for index, destination_stack in enumerate(all_stacks):
            # Same as source stack
            if index == source_stack_index:
                continue
            # Stack is collapsed
            if self.is_stack_complete(destination_stack):
                continue
            # Destination stack is cheated, ignore
            if self.is_stack_cheated(destination_stack):
                continue

            # Check moving cheated card to valid position
            if source_stack[0] < 0:
                # We use 'True' to also uncheat a cheated card
                # Can uncheat a card into an empty stack
                if not destination_stack:
                    destinations.append((index, True))
                    continue

                # Normal method of freeing up a cheated card
                if destination_stack[-1] == (-1 * source_stack[0]) + 1:
                    destinations.append((index, True))
                    continue

            # Empty stack always legal
            if not destination_stack:
                destinations.append((index, False))
                continue

            # Normal legal destination
            if destination_stack[-1] == source_stack[0] + 1:
                destinations.append((index, False))
                continue

            # Cheated card movement (can only move non-cheated card)
            if source_stack[0] > 0 and len(source_stack) == 1:
                destinations.append((index, True))

        return destinations


    '''
    Generate a new stacks with what the result of a move looks like.
    '''
    def get_move_end_state(self, move):
        new_stacks = copy.deepcopy(self.stacks)
        source_move = move[0][0]
        target_move = move[0][1]
        is_cheated = move[1]

        stack_to_move = new_stacks[source_move[0]][source_move[1]:]
        new_stacks[target_move[0]].extend(stack_to_move)
        new_stacks[source_move[0]] = new_stacks[source_move[0]][:source_move[1]]

        if is_cheated:
            new_stacks[target_move[0]][-1] = new_stacks[target_move[0]][-1] * -1

        new_moves = copy.deepcopy(self.moves_taken)
        new_game_state = GameState(new_stacks, new_moves)
        new_game_state.moves_taken.append((source_move, target_move))

        return new_game_state

    def get_score(self):
        num_complete_stacks = self.get_num_complete_stacks()
        num_empty_stacks = self.get_num_empty_stacks()
        num_cheated_stacks = self.get_num_stacks_cheated()
        max_stack_size = max([len(x) for x in self.stacks])
        # Priority prefers lower score, so we just use negative values. We'll do any logging with a multiplied -1.
        score = -1 * ((num_complete_stacks * 100.0) + (num_empty_stacks * 50.0) + (num_cheated_stacks * -15.0) + (max_stack_size * 2.0))

        return score

class Solver:
    def __init__(self, initial_state):
        self.initial_state = initial_state

    def solve(self):
        move_list = []

        print("Initial game state:")
        print(self.initial_state)
        print()

        visited = set()
        queue = PriorityQueue()
        states_checked = 0
        winning_state = None
        highest_scoring_state = self.initial_state

        queue.put(self.initial_state)

        # Traverse the state space and search for a winning state.
        while not queue.empty() and not winning_state:
            current_state = queue.get()

            if current_state in visited:
                continue

            states_checked += 1
            if states_checked >= STATES_SEARCH_LIMIT:
                break

            print("Currently checking state with score (" + str(current_state.get_score() * -1) + ")")

            if current_state < highest_scoring_state:
                highest_scoring_state = current_state

            visited.add(current_state)

            legal_moves = current_state.find_legal_moves()

            for move in legal_moves:
                move_end_state = current_state.get_move_end_state(move)

                if move_end_state.is_won():
                    winning_state = move_end_state
                    break

                if move_end_state.is_no_legal_moves():
                    # Should be a loss state.
                    continue

                queue.put(move_end_state)

        print()
        print("States searched: " + str(states_checked))

        if not winning_state:
            print("No winning state found!")
            return highest_scoring_state, False
        else:
            print("Winning state found!")
            return winning_state, True

        print()

def main():

    print("Will solve " + str(TIMES_TO_SOLVE) + " times.")

    for x in range(TIMES_TO_SOLVE):

        print(str(TIMES_TO_SOLVE - x) + " more times to go.")
        stacks = SAMPLE_STACKS
        if not USE_SAMPLE:
            game_api = GameApi()
            stacks = game_api.stacks

        stacks = card_stacks_to_num_stacks(stacks)
        game_state = GameState(stacks)
        solver = Solver(game_state)

        final_state, is_winning = solver.solve()

        print()
        if is_winning:
            print("Winning state:")
            print(final_state)
            print()
        else:
            print("Highest scoring state:")
            print(final_state)
            print()
            print("Score was: " + str(final_state.get_score() * -1))

        print("Moves taken (" + str(len(final_state.moves_taken)) + "):")
        for move_tuple in final_state.moves_taken:
            print("Source: " + str(move_tuple[0]))
            if not USE_SAMPLE:
                game_api.click_card(move_tuple[0])
            print("Destination: " + str(move_tuple[1]))
            if not USE_SAMPLE:
                game_api.click_card(move_tuple[1])

        print()

    print("Done!")

def card_stacks_to_num_stacks(stacks):
    return [[CARD_TO_NUMBER[x] for x in y] for y in stacks]

def num_stacks_to_card_stacks(self):
    return [[NUMBER_TO_CARD[x] for x in y] for y in stacks]

if __name__ == "__main__":
    main()

