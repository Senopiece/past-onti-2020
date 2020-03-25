from graphviz import Digraph

def build_graph(connections, folder):
    graph = Digraph('finite_state_machine', filename=folder+'fsm', format='svg')
    graph.attr(rankdir='LR')

    for prev, nexts in connections.items():
        if prev != 'num':
            for next, content in nexts.items():
                graph.node(prev)
                graph.node(next)
                graph.edge(prev, next, label = str(connections['num'][prev][next]))

    graph.render(view = True)

    return folder+'fsm.svg'
