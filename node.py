from rules_example_zookeeper import ZOOKEEPER_RULES, TOURIST_RULES
from  graphviz import Digraph
from random import choice
from icecream import ic
import language_tool_python

class Node:
    def __init__(self, value, parents=None, or_set=None) -> None:
        self.value = value
        self.parents = parents if parents is not None else set()
        self.or_set = or_set if or_set is not None else set()

    def children(self):
        child_nodes = set()
        for and_set in self.or_set:
            for node in and_set:
                child_nodes.add(node)
        return child_nodes

    def __repr__(self):
        return f"Node({self.value})"

class GoalTree:
    def __init__(self, rules) -> None:
        self.nodes = {}
        self.construct(rules)
        self.tool = language_tool_python.LanguageTool('en-US') 

    def visualize_tree(self, output_filename="goal_tree"):
        """
        Visualize the goal tree using graphviz.
        Each AND set in the OR set will have arrows leading into a single point,
        and OR sets are displayed as separate branches.
        """
        dot = Digraph()

        dot.attr(rankdir='LR')

        def add_edges(node):
            """Helper function to add edges to the graph for a given node."""
            # OR-sets are displayed as separate branches
            for or_idx, and_set in enumerate(node.or_set):
                if len(and_set) > 1:
                    # Create a unique AND node for each AND set if there is more than one antecedent
                    and_node_label = f"{node.value}_AND{or_idx}"  
                    dot.node(and_node_label, "AND", shape="circle", style="filled", fillcolor="lightgrey")
                    dot.edge(and_node_label, node.value)  # Connect the AND node to the parent

                    for child_node in and_set:
                        dot.edge(child_node.value, and_node_label)  # Connect each antecedent to the AND node
                else:
                    # If it's a single antecedent, directly connect it to the parent node
                    child_node = list(and_set)[0]
                    dot.edge(child_node.value, node.value)

        # Add nodes and edges to the graph
        for node_value, node in self.nodes.items():
            dot.node(node_value)  # Add the parent node itself
            add_edges(node)  # Add its antecedents and their connections

        # Render the graph
        dot.render(output_filename, format="png", cleanup=True)
        print(f"Tree diagram saved as {output_filename}.png")

    def construct(self, rules):
        for rule in rules:
            consequent = " ".join(rule.consequent()[0].split()[1:])
            antecedents = [" ".join(antecedent.split()[1:]) for antecedent in rule.antecedent()]

            # Create a new node for the consequent if it doesn't exist
            if consequent not in self.nodes:
                self.nodes[consequent] = Node(consequent)

            consequent_node = self.nodes[consequent]
            # Create nodes for each antecedent if they don't exist and add them to the OR-set
            and_set = set()
            for antecedent in antecedents:
                if antecedent not in self.nodes:
                    self.nodes[antecedent] = Node(antecedent)
                and_set.add(self.nodes[antecedent])
            
            consequent_node.or_set.add(frozenset(and_set))

            # Update the parent relationship
            for antecedent_node in and_set:
                antecedent_node.parents.add(consequent_node)

    def display(self):
        """Display the goal tree structure."""
        for node_value, node in self.nodes.items():
            print(f"Node: {node_value}")
            print(f"  Parents: {[parent.value for parent in node.parents]}")
            print(f"  OR-Set:")
            for and_set in node.or_set:
                print(f"    AND-Set: {[n.value for n in and_set]}")
            print()

    def forward_chain(self, data):
        """Forward chaining algorithm."""
        known_facts = set(data)
        inferred_facts = set()

        while True:
            applied_rule = False
            for node in self.nodes.values():
                # Check if the node can be inferred based on known facts
                if node.value not in known_facts:
                    # Check if any AND-Set (in OR-Set) can be satisfied
                    for and_set in node.or_set:
                        if all(antecedent.value in known_facts for antecedent in and_set):
                            known_facts.add(node.value)
                            inferred_facts.add(node.value)
                            applied_rule = True
                            break  # Rule applied, move to next node

            if not applied_rule:
                break  # No more rules can be applied, end forward chaining
        # self.print_inference_graph(data, inferred_facts)
        return inferred_facts
    
    def print_inference_graph(self, data, inferred_facts):
        """Prints a human-readable graph of the inference process."""
        print("=== Forward Chaining ===")
        
        def recursive_print(node, indent=0):
            """Helper recursive function to print the tree-like structure."""
            
            prefix = "  " * indent + ("|- " if indent > 0 else "")
            if node.value in data:
                print(f"{prefix}{node.value} (KNOWN)")
            elif node.value in inferred_facts:
                print(f"{prefix}{node.value} (INFERRED)")
            else:
                print(f"{prefix}{node.value} (Unknown)")
            
            # Recursively print children (antecedents)
            for and_set in node.or_set:
                if all(child in data or child in inferred_facts for child in and_set):
                    if len(node.or_set) > 1:
                        print(f"{"  " * indent + "  "}or")
                for child in and_set:
                    recursive_print(child, indent + 1)
            
            return

        # Start from all inferred facts and print their antecedents
        for fact in inferred_facts:
            if fact in self.nodes:
                print()
                recursive_print(self.nodes[fact])
        print("========================================")

    def recursive_backward_chain(self, hypothesis):
        required_facts = set()
        def recurse(node):
            """
            Recursive function to traverse the goal tree.
            Accumulates required facts in `required_facts`.
            """
            # If the node has no antecedents, it's a fact or a terminal node
            if not node.or_set:
                return {node.value}

            # Accumulate all the antecedents (AND-sets) that need to be satisfied
            facts_needed_for_node = set()
            for and_set in node.or_set:
                facts_for_this_and_set = set()
                for child in and_set:
                    facts_for_this_and_set.update(recurse(child))
                facts_needed_for_node.update(facts_for_this_and_set)

            return facts_needed_for_node

        # Start recursion from the hypothesis node
        hypothesis_node = self.nodes[hypothesis]
        required_facts.update(recurse(hypothesis_node))

        return required_facts
        

        

    def backward_chain(self, hypothesis):
        """
        Perform a backward chaining reasoning process starting from the given hypothesis.
        Displays the reasoning steps using 'Opus' notation, explaining how each fact 
        leads to the next.
        """
        visited = {}
        index = 0
        stack = [(self.nodes[hypothesis], index)]
        while stack:
            node, index = stack.pop()

            # Skip if node already fully visited
            if node.value in visited:
                if visited[node.value][1]:
                    continue

            # If node has not been fully processed, display the current node's reasoning step
            if node.or_set and index is not None:
                print(f"({index}) Opus {node.value}")
                print("-", end="")
                visited[node.value] = (index, True) # Mark the node as fully processed


            j = 0
            for and_set in node.or_set:
                j += 1
                i = 0
                for child in and_set:
                    i += 1
                    if child.or_set:
                        index += 1
                        if (i == len(and_set)):
                            if child.value in visited:
                                print(f" Opus {child.value} ({visited[child.value][0]})")
                            else:
                                print(f" Opus {child.value} ({index})")
                                visited[child.value] = (index, False)
                        else:
                            if child.value in visited:
                                print(f" Opus {child.value} ({visited[child.value][0]}) and", end="")
                            else:
                                print(f" Opus {child.value} ({index}) and",end="")
                                visited[child.value] = (index, False)
                        stack.append((child, index))
                    else:
                        # Leaf node or fact with no further conditions
                        if (i == len(and_set)):
                            print(f" Opus {child.value}")
                        else:
                            print(f" Opus {child.value} and", end="")
                        stack.append((child, None))

                # If the node has multiple OR-sets, print "or" between them
                if len(node.or_set) > 1:
                    if j != len(node.or_set):
                        print("or")
                        print("-", end="")

    def akinator(self, mutually_exclusive):
        known_facts = set()
        possible_hypotheses = set()
        possible_facts = set()
        possible_rules = set()
        asked_facts = set()

        for node in self.nodes:
            if not self.nodes[node].or_set:
                possible_facts.add(node)
            elif not self.nodes[node].parents:
                possible_hypotheses.add(node)
            else:
                possible_rules.add(node)

        def correct_grammar(text):
            matches = self.tool.check(text)
            corrected_text = language_tool_python.utils.correct(text, matches)
            return corrected_text

        def ask_fact_question(fact):
            """Ask a yes/no question about a fact."""
            answer = input(correct_grammar(f"Does it {fact}?") + " (yes/no): ").strip().lower()
            return answer == "yes"

        def ask_mutually_exclusive_question(mutually_exclusive_set):
            """Ask the user to choose which fact from a mutually exclusive set is true."""
            print("Please choose the correct fact from the following options:")
            for idx, fact in enumerate(mutually_exclusive_set, start=1):
                print(f"{idx}. {fact}")
            
            # Get user input
            choice_idx = -1
            while choice_idx < 1 or choice_idx > len(mutually_exclusive_set):
                try:
                    choice_idx = int(input("Enter the number of the correct fact: ").strip())
                except ValueError:
                    print("Invalid input, please enter a valid number.")

            # Return the chosen fact
            chosen_fact = list(mutually_exclusive_set)[choice_idx - 1]
            return chosen_fact
        
        def narrow():
            not_possible_facts = set()
            for fact in asked_facts:
                if fact not in known_facts:
                    not_possible_facts.add(fact)
            # Using forward chaining removing not possible questions
            while True:
                applied_rule = False
                for node in self.nodes.values():
                    n = 0 # This n keeps track how many and sets are false in the or set
                    for and_set in node.or_set:
                        for child in and_set:
                            if child.value in not_possible_facts:
                                n += 1
                                break
                        # if all and_sets in the or set are false that we add the node to the not possible
                        if n == len(node.or_set):
                            if node.value not in not_possible_facts:
                                not_possible_facts.add(node.value)
                                applied_rule = True # This marks changes to the chain

                # if no changes that we can break   
                if not applied_rule:
                    break
            
            # removing hypotheses that are in the not_possible_facts from the forward chain above
            removed_hypotheses = set()
            for fact in not_possible_facts:
                if fact in possible_hypotheses:
                    possible_hypotheses.remove(fact)
                    removed_hypotheses.add(fact)
            ic(possible_hypotheses)
            ic(removed_hypotheses)
            # collecting the facts from removed hypotheses and possible hypotheses using backward chain
            facts = set()
            for possible_hypothesis in possible_hypotheses:
                facts.update(self.recursive_backward_chain(possible_hypothesis))
            facts2 = set()
            for possible_hypothesis in removed_hypotheses:
                facts2.update(self.recursive_backward_chain(possible_hypothesis))
            
            # removing facts that are in removed hypotheses and not in possible hypotheses
            not_possible_facts = set()
            for fact in facts2:
                if fact not in facts:
                    not_possible_facts.add(fact)
            
            for fact in not_possible_facts:
                if fact in possible_facts:
                    possible_facts.remove(fact)
                    ic(f"removing {fact}")
            
            # adding only possible rules
            possible_rules = set()
            for fact in self.forward_chain(list(possible_facts.union(known_facts))):
                if self.nodes[fact].or_set and self.nodes[fact].parents:
                    possible_rules.add(fact)
            
            # removing redundant question that don't add anything new
            deducible_nodes = self.forward_chain(list(known_facts))
            potential_redundant = set()
            for node in deducible_nodes:
                deducible_facts = self.recursive_backward_chain(node)
                for fact in deducible_facts:
                    if fact not in known_facts:
                        potential_redundant.add(fact)
            ic(potential_redundant)
            # Generate all subsets of the potential_redundant (the power set)??
            subsets = {}
            for fact in potential_redundant:
                for parent in self.nodes[fact].parents:
                    if parent.value not in subsets:
                        subsets[parent.value] = set()
                    subsets[parent.value].add(fact)
            
            valid_facts = set()
            for subset in subsets:
                test_set = possible_facts.union(known_facts).difference(subsets[subset])
                chain = self.forward_chain(list(test_set))
                if subset not in chain:
                    valid_facts.update(subsets[subset])
            
            for fact in potential_redundant:
                if fact not in valid_facts and fact in possible_facts:
                    possible_facts.remove(fact)
                    ic(f"removing {fact}")
            ic(possible_facts)

        def choose_question():
            fact = choice(list(possible_facts))
            ic(mutually_exclusive)

            flag = True
            flag2 = False
            mes = None
            for mutually_exclusive_set in mutually_exclusive:
                if fact in mutually_exclusive_set:
                    flag2 = True
                    for item in mutually_exclusive_set:
                        if item not in possible_facts:
                            flag = False
                            break
                    mes = mutually_exclusive_set
                    break

            if flag2 and flag:
                fact = ask_mutually_exclusive_question(mes)
                known_facts.add(fact)
                ic(f"adding to known facts {fact}")
                for item in mes:
                    asked_facts.add(item)
                    ic(f"adding to asked questions {item}")
                    possible_facts.remove(item)
                    ic(f"removing from possible facts {item}")
            elif (flag2 and not flag) or (not flag2):
                possible_facts.remove(fact)
                ic(f"removing from possible facts {fact}")
                if ask_fact_question(fact):
                    known_facts.add(fact)
                    ic(f"adding to known facts {fact}")
                asked_facts.add(fact)
                ic(f"adding to asked questions {fact}")
        
        while len(possible_facts) > 0:
            # check if it can already find something
            choose_question()
            done = False
            for node in self.forward_chain(list(known_facts)):
                if node in possible_hypotheses:
                    print(f"You are thinking of {node}")
                    done = True
            if done:
                break

            narrow()


        


if __name__ == "__main__":
    ic.disable()
    while True:
        print("Options:\n1)Backchain\n2)Akinator\n3)Exit")
        option = int(input())
        if option == 3:
            break
        if option == 1:
            hypothesis = input("Give a valid hypothesis:")
            GoalTree(rules=TOURIST_RULES).backward_chain(hypothesis)
        else:
            GoalTree(rules=TOURIST_RULES).akinator(mutually_exclusive=[{'wears bright flashy clothing', 'wears muted, utilitarian clothing'},
                                                                    {'frequently checks for directions', 'uses tech to navigate efficiently'},
                                                                    {'asks basic questions about lunar history', 'asks in-depth technical questions'},
                                                                    {'wears business attire', 'wears adventure-themed clothing'},
                                                                    {'records videos constantly', 'talks nostalgically about earth'}])