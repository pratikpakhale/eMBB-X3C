import random
import json

class Node:
    def __init__(self, name, data, power):
        self.name = name
        self.data = data
        self.power = power

class Gateway:
    def __init__(self, name, power_setup, storage_capacity):
        self.name = name
        self.power_setup = power_setup
        self.storage_capacity = storage_capacity

class Link:
    def __init__(self, node, gateway, power):
        self.node = node
        self.gateway = gateway
        self.power = power

DEBUG = False

def exact_cover(nodes, gateways, links):
    
    node_set = set(nodes)
    gateway_set = set(gateways)
    node_gateway_links = {node: set() for node in node_set}
    gateway_capacity = {gateway: gateway.storage_capacity for gateway in gateway_set}
    node_power_budget = {node: node.power for node in node_set}
    selected_gateways = set()
    selected_nodes = set()
    selected_links = set()
    min_power_consumption = float('inf')
    optimal_gateways = None
    optimal_nodes = None
    optimal_links = None
    last_optimal_gateways = None
    last_optimal_nodes = None
    last_optimal_links = None



    for link in links:
        node_gateway_links[link.node].add((link.gateway, link.power))

    exact_solution_found = False

    def dfs(node_set, selected_gateways, selected_nodes, selected_links, total_power):
        nonlocal min_power_consumption, optimal_gateways, optimal_nodes, optimal_links, exact_solution_found
        nonlocal last_optimal_gateways, last_optimal_nodes, last_optimal_links

        if not node_set:
            exact_solution_found = True
            
            if total_power < min_power_consumption:
                min_power_consumption = total_power
                optimal_gateways = selected_gateways.copy()
                optimal_links = selected_links.copy()
                optimal_nodes = selected_nodes.copy()
            
            return
        else:
            if last_optimal_gateways is None or total_power < min_power_consumption:
                last_optimal_gateways = selected_gateways.copy()
                last_optimal_nodes = selected_nodes.copy()
                last_optimal_links = selected_links.copy()

        best_node = max(node_set, key=lambda node: node.data / node_power_budget[node])
        
        if DEBUG:
            print("Current Node Set:", [node.name for node in node_set])
            print("Selected Gateways:", [gateway.name for gateway in selected_gateways])
            print("Selected Nodes:", [node.name for node in selected_nodes])
            print("Selected Links:", [(node.name, gateway.name) for node, gateway in selected_links])
            print("Total Power:", total_power)
            print("------------------------")

        for gateway, power in node_gateway_links[best_node]:
            if power <= node_power_budget[best_node] and gateway_capacity[gateway] >= best_node.data:
                node_set.remove(best_node)
                selected_nodes.add(best_node)
                selected_links.add((best_node, gateway))
                selected_gateways.add(gateway)
                node_power_budget[best_node] -= power
                gateway_capacity[gateway] -= best_node.data
                dfs(node_set, selected_gateways, selected_nodes, selected_links, total_power + gateway.power_setup)
                node_set.add(best_node)
                selected_nodes.remove(best_node)  
                selected_links.remove((best_node, gateway)) 
                if gateway in selected_gateways:
                    selected_gateways.remove(gateway)
                node_power_budget[best_node] += power
                gateway_capacity[gateway] += best_node.data
        

    dfs(node_set, selected_gateways, selected_nodes, selected_links, 0)

    if optimal_gateways:
        return optimal_gateways, optimal_nodes, optimal_links
    else:
        return last_optimal_gateways, last_optimal_nodes, last_optimal_links


# def nodes_gateways_links(num_nodes, num_gateways, node_data_lock = False, gateway_storage_lock = False):

#     if node_data_lock:
#         data = random.randint(1, 20)
#         nodes = [Node(f'n{i}', data, random.randint(1, 20)) for i in range(1, num_nodes + 1)]
#     else:
#         nodes = [Node(f'n{i}', random.randint(1, 20), random.randint(1, 20)) for i in range(1, num_nodes + 1)]

#     if gateway_storage_lock:
#         storage_capacity = random.randint(20, 100)
#         gateways = [Gateway(f'g{i}', random.randint(1, 20), storage_capacity) for i in range(1, num_gateways + 1)]
#     else:
#         gateways = [Gateway(f'g{i}', random.randint(1, 20), random.randint(20, 100)) for i in range(1, num_gateways + 1)]

#     links = []
#     for node in nodes:
#         for gateway in gateways:
#             # Ensure the link is feasible
#             power_needed = random.randint(1, min(node.power, gateway.power_setup))
#             links.append(Link(node, gateway, power_needed))
#     return nodes, gateways, links

def nodes_gateways_links(num_nodes, num_gateways, node_data_lock=False, gateway_storage_lock=False):
    if node_data_lock:
        # Locking node data at a specific value
        data = 10  # Adjust 10 as needed for the desired locked value
        nodes = [Node(f'n{i}', data, random.randint(1, 20)) for i in range(1, num_nodes + 1)]
    else:
        # Varying node data linearly
        nodes = [Node(f'n{i}', i * (10 / num_nodes), random.randint(1, 20)) for i in range(1, num_nodes + 1)]

    if gateway_storage_lock:
        # Locking gateway storage capacity at a specific value
        storage_capacity = 100  # Adjust 100 as needed for the desired locked value
        gateways = [Gateway(f'g{i}', random.randint(1, 20), storage_capacity) for i in range(1, num_gateways + 1)]
    else:
        # Varying gateway storage capacity linearly
        gateways = [Gateway(f'g{i}', random.randint(1, 20), i * (100 / num_gateways)) for i in range(1, num_gateways + 1)]

    links = []
    for node in nodes:
        for gateway in gateways:
            power_needed = random.randint(1, min(node.power, gateway.power_setup))
            links.append(Link(node, gateway, power_needed))
    return nodes, gateways, links


def simulate(total_nodes, total_gateways, data_lock = False, storage_lock = False):
    nodes, gateways, links = nodes_gateways_links(total_nodes, total_gateways, data_lock, storage_lock)
    selected_solution = exact_cover(nodes, gateways, links)
    if selected_solution is None:
        print("No solution exists.")
    else:
        selected_gateways, selected_nodes, selected_links = selected_solution
        total_power = sum(gateway.power_setup for gateway in selected_gateways)
        print("------------------------------")
        print("Selected Gateways:", [gateway.name for gateway in selected_gateways])
        print("Total Power Consumption:", total_power)
        print("Total Selected Gateways:", len(selected_gateways))
        print("Total Selected Nodes:", len(selected_nodes))
        print("Total Selected Links:", len(selected_links))
        print("------------------------------")
        
    if selected_solution is not None:
        selected_gateways, selected_nodes, selected_links = selected_solution
        total_power = sum(gateway.power_setup for gateway in selected_gateways)
    
    return total_power
      

def simulate_varying_nodes(max_nodes, total_gateways, data_lock=False, storage_lock=False, filename='results/varying_nodes.json'):
    results = []
    for total_nodes in range(1, max_nodes + 1):
        result = simulate(total_nodes, total_gateways, data_lock, storage_lock)
        results.append((total_nodes, result))
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    return results

def simulate_varying_gateways(total_nodes, max_gateways, data_lock=False, storage_lock=False, filename='results/varying_gateways.json'):
    results = []
    for total_gateways in range(1, max_gateways + 1):
        result = simulate(total_nodes, total_gateways, data_lock, storage_lock)
        results.append((total_gateways, result))
        with open(filename, 'w') as f:
            json.dump(results, f, indent=4)
    return results

def main():
    simulate_varying_nodes(10, 6)
    simulate_varying_gateways(6, 10)
    simulate_varying_nodes(10,6, True, False, 'results/varying_nodes_data_lock.json')
    simulate_varying_nodes(10,6, False, True, 'results/varying_nodes_storage_lock.json')
    simulate_varying_nodes(10,6, True, True, 'results/varying_nodes_data_storage_lock.json')

    simulate_varying_gateways(6, 10, True, False, 'results/varying_gateways_data_lock.json')
    simulate_varying_gateways(6, 10, False, True, 'results/varying_gateways_storage_lock.json')
    simulate_varying_gateways(6, 10, True, True, 'results/varying_gateways_data_storage_lock.json')
    


if __name__ == "__main__":
    main()