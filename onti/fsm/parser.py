#!/usr/bin/env python3


# BUG: s_1^9 != s^9_1, но это эквивалентные выражения, но транслируются в s_1__9, s_9__1

import re
from sys import argv
from termcolor import colored


def format_math_symbols(symbol: str):
    s = re.sub('[\$\\(\)_{}]', '', symbol).strip(' ')
    return s


def formatting(string: str):
    try:
        if string.index('^') < string.index('_'):
            raise RuntimeError('Wrong ^ and _ position')
    except ValueError:
        pass
    string = string.replace('$', '')
    string = string.replace('\\neg', 'not')
    string = string.replace('\parallel', 'or')
    string = string.replace('\prime', 'prime')
    string = string.replace('\&', 'and')
    string = string.replace('{', '')
    string = string.replace('}', '')
    string = string.replace('^', '__')
    string = string.replace('*', 'star')
    string = string.replace('&gt;', '>')
    string = string.replace('&nbsp;', ' ')
    string = string.replace('&lt;', '<')
    return string


# связи
# connections[previous][next][0] = {'signal_condition': 's1 and s2', 'action': 'a_0__j'}
# connections['num'][previous][next] = connection_number # WARNING: ожидается что Колотов не создаст состояние с именем num )
def parse_connections(path, path_to_write_formatted):
    connections = {
        'num': {}}  # connections[previous][next][0] = {'signal_condition': 's_1 and s_2', 'action': 'a_0__j'}
    nodes = []
    connection = []  # connection[connection_number] = {'previous': prev, 'next': next}
    data = ''
    with open(path, 'r') as f:
        data += f.readline()
        data += f.readline()
        for line in f.readlines():
            line = line.strip()[1:-1]
            ___number, state, signal, next_state, action = line.split('|')

            ___number = ___number.strip()
            signal = signal.strip()
            state = state.strip()
            next_state = next_state.strip()
            action = action.strip()

            state = formatting(state)
            signal = formatting(signal)
            next_state = formatting(next_state)
            action = formatting(action)

            if signal == '':
                signal = 'this_is_true'

            if action == '':
                action = 'empty'

            if not (state in nodes):
                nodes.append(state)

            connections.setdefault(state, {})

            connections['num'].setdefault(state, {})
            if not (next_state in connections[state].keys()):
                connections['num'][state][next_state] = len(connection)
                connection.append({'previous': state, 'next': next_state})

            if connections[state].get(next_state) == None:
                connections[state][next_state] = []

            connections[state][next_state].append({'signal_condition': signal, 'action': action})

            data += '|{}|{}|{}|{}|{}|\n'.format(___number, state, signal, next_state, action)

    with open(path_to_write_formatted, 'w') as f:
        f.write(data)

    return nodes, connections, connection


# res = {name: descripion}
def parse_description(path, path_to_write_formatted):
    res = {}
    data = ''
    with open(path, 'r') as f:
        data += f.readline()
        data += f.readline()
        for line in f.readlines():
            line = line.strip()[1:-1]
            elem, desc = line.split('|')

            elem = elem.strip()
            elem = formatting(elem)
            desc = desc.strip()
            desc = formatting(desc)

            res[elem] = desc
            data += "|{}|{}|\n".format(elem, desc)

    with open(path_to_write_formatted, 'w') as f:
        f.write(data)

    return res


responce_template = """
\x1b[34;1m--signals:\x1b[0m
{}
\x1b[34;1m--action:\x1b[0m
{}
"""

if __name__ == '__main__':
    try:
        nodes, connections, connection = parse_connections('input/connections.md',
                                                           path_to_write_formatted='input/connections.md')

        signals_desc = parse_description('input/signals.md', path_to_write_formatted='input/signals.md')
        signals_desc['this_is_true'] = "return True"

        actions_desc = parse_description('input/actions.md', path_to_write_formatted='input/actions.md')
        actions_desc['empty'] = "empty action"

        prev, next = connection[int(argv[2])]['previous'], connection[int(argv[2])]['next']

        print('\x1b[32;1m>>>', prev, '--> ', next, '\x1b[0m')
        for connect in connections[prev][next]:
            signal = ''
            level = ''
            for item in connect['signal_condition'].split():
                if item.find('(') != -1:
                    signal += level + '(\n'
                    level += '  '
                    item = item.replace('(', '')

                close_count = item.count(')')
                item = item.replace(')', '')

                signal += level + '\x1b[33m(' + item.strip() + ')\x1b[0m' + signals_desc[item.strip()].strip() if item in signals_desc else ''
                signal += '\n' + level + colored('AND\n', 'yellow') if item == 'and' else ''
                signal += level + colored('NOT ', 'yellow') if item == 'not' else ''
                signal += '\n' + level + colored('OR\n', 'yellow') if item == 'or' else ''

                for i in range(close_count):
                    level = level[:-2]
                    signal += '\n' + level + ')'

            print(responce_template.format(
                signal,
                '\x1b[33m('+connect['action']+')\x1b[0m'+actions_desc[connect['action']]
            ))
    except Exception as ex:
        raise ex
        print('usage example: ./parser.py --connection 12')
