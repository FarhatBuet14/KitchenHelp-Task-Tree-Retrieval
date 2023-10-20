import pickle
import json
from FOON_class import Object

# -----------------------------------------------------------------------------------------------------------------------------#

# Checks an ingredient exists in kitchen


def check_if_exist_in_kitchen(kitchen_items, ingredient):
    """
        parameters: a list of all kitchen items,
                    an ingredient to be searched in the kitchen
        returns: True if ingredient exists in the kitchen
    """

    for item in kitchen_items:
        if item["label"] == ingredient.label \
                and sorted(item["states"]) == sorted(ingredient.states) \
                and sorted(item["ingredients"]) == sorted(ingredient.ingredients) \
                and item["container"] == ingredient.container:
            return True

    return False


# -----------------------------------------------------------------------------------------------------------------------------#

# Iterative Deepening Search


def depth_limited_search(node, goal, depth_limit):
    
    if hasattr(node, "output_nodes"): 
        if depth_limit == 0 and goal.label in [output for output in node.output_nodes]: return True
    else:
        if depth_limit == 0 and goal.label == node.label : return True
    

    if depth_limit > 0:
        if hasattr(node, "output_nodes"): 
            for output_node in node.output_nodes:
                if depth_limited_search(output_node, goal, depth_limit + 1):
                    return True
        else: return True

    return False


# -----------------------------------------------------------------------------------------------------------------------------#


def search_taskTREE(kitchen_items=[], goal_node=None, algorithm = "success_rate"):
    # list of indices of functional units
    reference_task_tree = []

    # list of object indices that need to be searched
    items_to_search = []

    # find the index of the goal node in object node list
    items_to_search.append(goal_node.id)

    # list of item already explored
    items_already_searched = []

    while len(items_to_search) > 0:
        current_item_index = items_to_search.pop(0)  # pop the first element
        if current_item_index in items_already_searched:
            continue

        else:
            items_already_searched.append(current_item_index)

        current_item = foon_object_nodes[current_item_index]

        if not check_if_exist_in_kitchen(kitchen_items, current_item):

            candidate_units = foon_object_to_FU_map[current_item_index]
            
            if algorithm == "success_rate": # Greedy BFS with SR
                candidate_motionSR = [motion_sr[foon_functional_units[candidate].motion_node] for candidate in candidate_units]
                selected_candidate_idx = candidate_units[candidate_motionSR.index(max(candidate_motionSR))]
            
            elif algorithm == "input_objects": # Greedy BFS with number of input objects
                candidate_inputNodes = []
                for candidate in candidate_units:
                    num_inputNodes = 0
                    for inputNode in foon_functional_units[candidate].input_nodes:
                        if len(inputNode.ingredients) == 0: num_inputNodes += 1
                        else: num_inputNodes += len(inputNode.ingredients)
                    candidate_inputNodes.append(num_inputNodes)
                selected_candidate_idx = candidate_units[candidate_inputNodes.index(min(candidate_inputNodes))]
            
            else: # Iterative Deepening Search
                
                depth_limit = 0
                while True:
                    for candidate in candidate_units:
                        if depth_limited_search(foon_functional_units[candidate], goal_node, depth_limit):
                            
                            break
                        else: continue
                    break
                    depth_limit += 1
                
                selected_candidate_idx = candidate
            
            # if an fu is already taken, do not process it again
            if selected_candidate_idx in reference_task_tree:
                continue

            reference_task_tree.append(selected_candidate_idx)

            # all input of the selected FU need to be explored
            for node in foon_functional_units[
                    selected_candidate_idx].input_nodes:
                node_idx = node.id
                if node_idx not in items_to_search:

                    # if in the input nodes, we have bowl contains {onion} and onion, chopped, in [bowl]
                    # explore only onion, chopped, in bowl
                    flag = True
                    if node.label in utensils and len(node.ingredients) == 1:
                        for node2 in foon_functional_units[
                                selected_candidate_idx].input_nodes:
                            if node2.label == node.ingredients[
                                    0] and node2.container == node.label:

                                flag = False
                                break
                    if flag:
                        items_to_search.append(node_idx)

    # reverse the task tree
    reference_task_tree.reverse()

    # create a list of functional unit from the indices of reference_task_tree
    task_tree_units = []
    for i in reference_task_tree:
        task_tree_units.append(foon_functional_units[i])

    return task_tree_units




def save_paths_to_file(task_tree, path):

    print('writing generated task tree to ', path)
    _file = open(path, 'w')

    _file.write('//\n')
    for FU in task_tree:
        _file.write(FU.get_FU_as_text() + "\n")
    _file.close()


# -----------------------------------------------------------------------------------------------------------------------------#

# creates the graph using adjacency list
# each object has a list of functional list where it is an output


def read_universal_foon(filepath='FOON.pkl'):
    """
        parameters: path of universal foon (pickle file)
        returns: a map. key = object, value = list of functional units
    """
    pickle_data = pickle.load(open(filepath, 'rb'))
    functional_units = pickle_data["functional_units"]
    object_nodes = pickle_data["object_nodes"]
    object_to_FU_map = pickle_data["object_to_FU_map"]

    return functional_units, object_nodes, object_to_FU_map


# -----------------------------------------------------------------------------------------------------------------------------#

if __name__ == '__main__':
    foon_functional_units, foon_object_nodes, foon_object_to_FU_map = read_universal_foon(
    )

    utensils = []
    with open('utensils.txt', 'r') as f:
        for line in f:
            utensils.append(line.rstrip())

    kitchen_items = json.load(open('kitchen.json'))

    goal_nodes = json.load(open("goal_nodes.json"))
    
    # Read the TXT file line by line and extract success rate of motions
    motion_sr = {}
    with open('motion.txt', 'r') as file:
        for line in file:
            parts = line.strip().split('\t')
            if len(parts) == 2:
                action = parts[0].strip()
                probability = float(parts[1])
                motion_sr[action] = probability

    for node in goal_nodes:
        print("----------------------------------------------------------------------------")
        node_object = Object(node["label"])
        node_object.states = node["states"]
        node_object.ingredients = node["ingredients"]
        node_object.container = node["container"]

        for object in foon_object_nodes:
            if object.check_object_equal(node_object):
                for algorithm in ["success_rate", "input_objects", "ids"]:
                    print(f'algo ---- {algorithm}')
                    start_time = time.time()
                    output_task_tree = search_taskTREE(kitchen_items, object, algorithm)
                    end_time = time.time()
                    print(f'length - {len(output_task_tree)}')
                    print(sys.getsizeof(output_task_tree) / (1024))
                    time_taken = end_time - start_time
                    print("Time taken:", time_taken, "seconds")
                    save_paths_to_file(output_task_tree,
                                    'output_{}_{}.txt'.format(algorithm, node["label"]))
                break

