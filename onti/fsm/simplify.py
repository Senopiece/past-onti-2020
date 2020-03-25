#!/usr/bin/env python3

import parser
import graph_builder
import code_generator

if __name__ == "__main__":
    nodes, connections, _ = parser.parse_connections('input/connections.md', path_to_write_formatted='input/connections.md')

    actions_description = parser.parse_description('input/actions.md', path_to_write_formatted='input/actions.md')
    actions_description['empty'] = "empty action"

    signals_description = parser.parse_description('input/signals.md', path_to_write_formatted='input/signals.md')
    signals_description['this_is_true'] = "return True"

    code_generator.generate_code(nodes, signals_description, connections, actions_description, folder='output/autogeneration/')

    graph_path = graph_builder.build_graph(connections, folder='output/graph/')
