from matplotlib import pyplot as plt
import json

def plot_results(results, xlabel, ylabel, title):
    
    plt.figure()
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)
    plt.plot([result[0] for result in results], [result[1] for result in results], 'ro-')
    plt.grid(True)
    # plt.show()
    plt.savefig('plots/'+ title + '.png')


with open('results/varying_nodes_storage_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Nodes', 'Total Power Consumed', 'Nodes vs Total Power Consumed (Storage Lock)')

with open('results/varying_nodes_data_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Nodes', 'Total Power Consumed', 'Nodes vs Total Power Consumed (Data Lock)')

with open('results/varying_nodes_data_storage_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Nodes', 'Total Power Consumed', 'Nodes vs Total Power Consumed (Data  & Storage Lock)')

with open('results/varying_gateways_data_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Gateways', 'Total Power Consumed', 'Gateways vs Total Power Consumed (Storage Lock)')

with open('results/varying_gateways_storage_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Gateways', 'Total Power Consumed', 'Gateways vs Total Power Consumed (Storage Lock)')

with open('results/varying_gateways_data_storage_lock.json') as f:
    results = json.load(f)
    plot_results(results, 'Gateways', 'Total Power Consumed', 'Gateways vs Total Power Consumed (Data & Storage Lock)')


with open('results/varying_nodes.json') as f:
    results = json.load(f)
    plot_results(results, 'Nodes', 'Total Power Consumed', 'Nodes vs Total Power Consumed')

with open('results/varying_gateways.json') as f:
    results = json.load(f)
    plot_results(results, 'Gateways', 'Total Power Consumed', 'Gateways vs Total Power Consumed')