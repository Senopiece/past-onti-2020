template = """
from aiogram.contrib.fsm_storage.files import JSONStorage
from aiogram import Bot, Dispatcher, executor
from aiogram.dispatcher.filters.state import State, StatesGroup

import actions
from filters import *  # aka signals
from tools import *

BOT_TOKEN = None
PROXY_URL = None
DB_PATH = None

# Entry point
bot = Bot(token=BOT_TOKEN, proxy=PROXY_URL)
storage = JSONStorage(DB_PATH)
dp = Dispatcher(bot, storage=storage)

executor.start_polling(dp, skip_updates=True)


class States(StatesGroup):
{states}

# Default listener
@dp.message_handler(individual_chat, commands='start')
async def start(msg, *args):
    await States.s____.set()


# Listeners
{listeners}
"""

tools_template = """# this is decorator
def next_state(state):
    def decorator(function):
        def wrapper(*args, **kwargs):
            function(*args, **kwargs)
            state.set()
        return wrapper
    return decorator
"""

filters_file_template = """from main import storage

{filters}
"""

state_template = "    {} = State()\n"

listener_template = """@dp.message_handler(lambda msg: {filters_expression}, state=States.{state})
@next_state(States.{next_state})
async def _{action_name}(*args, **kwargs):
    await actions.{action_name}(*args, **kwargs)


"""

filter_template = """
async def {name}(msg, *args, **kwargs):
    \"""
    {description}
    \"""
    pass

"""

action_template = """
async def {name}(*args, **kwargs):
    \"""
    {description}
    \"""
    msg = args[0]
    pass

"""

actions_template = """from main import storage

{}
"""


def generate_code(nodes, signals_description, connections, actions_description, folder):
    # => Generate tools.py file
    with open(folder + 'tools.py', 'w') as file:
        file.write(tools_template)

    # => Generate actions.py file
    actions = ""
    for action, desc in actions_description.items():
        actions += action_template.format(name=action, description=desc)
    with open(folder + 'actions.py', 'w') as file:
        file.write(actions_template.format(actions))

    # => Generate filters.py file
    filters = ""
    for filter, desc in signals_description.items():
        filters += filter_template.format(name=filter, description=desc)

    with open(folder + 'filters.py', 'w') as file:
        file.write(filters_file_template.format(filters=filters))

    # => Generate main.py file
    # states init
    states = ""
    for node in nodes:  # node aka state
        states += state_template.format(node)

    # listeners init
    listeners = ""
    for state, nexts in connections.items():
        if state == 'num':
            continue
        for next_state, transitions in nexts.items():
            for transition in transitions:
                filters_expression = transition['signal_condition']
                items = filters_expression.split()
                for i in range(len(items)):
                    if items[i] in signals_description.keys():
                        items[i] += '(msg)'
                filters_expression = ' '.join(items)
                listeners += listener_template.format(
                    filters_expression=filters_expression,
                    state=state,
                    next_state=next_state,
                    action_name=transition['action']
                )

    with open(folder + 'main.py', 'w') as file:
        file.write(template.format(states=states, listeners=listeners))
