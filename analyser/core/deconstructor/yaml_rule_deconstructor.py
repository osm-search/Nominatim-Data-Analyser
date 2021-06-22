import yaml
from typing import Callable, Deque, Dict, Set, Tuple
from collections import deque
from pathlib import Path
from analyser.logger.logger import LOG

NEW_NODE_EVENT = 'new_node'
BACKTRACKING_EVENT = 'backtracking'

class YAMLRuleDeconstructor():
    """
        Deconstructs a YAML rule file following a tree
        structure.

        Raises events throughout the entire deconstruction process.
        It uses a backtracking system to go back on upper nodes
        when reaching a leaf.
    """
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name
        self._loaded_data: dict = self._load_yaml(file_name)
        self._init_event_callbacks()

    def deconstruct(self) -> None:
        """
            Explores the YAML loaded data tree.

            Sends each node to subscribers and backtracks
            when a leaf node is reached.
        """
        #Add a root node needed for the exploration of the tree
        self._loaded_data = {'ROOT_NODE': { 'out': self._loaded_data}}
        history_stack: Deque[str] = deque()
        current_node: Tuple[str] = ('ROOT_NODE',)
        nodes_already_sent: Set[Tuple[str]] = set()
        backtrack_count: int = 0

        while current_node or history_stack:
            node_data: dict = self._get_data_from_keys(current_node)

            if current_node not in nodes_already_sent:
                nodes_already_sent.add(current_node)
                if current_node == ('ROOT_NODE',):
                    self.notify_new_node({'type': 'ROOT_NODE'})
                else:
                    self.notify_new_node(node_data)

            if 'out' in node_data:
                if backtrack_count != 0:
                    self.notify_backtracking(backtrack_count)
                    backtrack_count = 0
                history_stack.append(current_node)
                current_node = current_node + ('out', next(iter(node_data['out'])))
            else:
                if history_stack:
                    #backtrack
                    backtrack_count += 1
                    backtrack_node = history_stack.pop()
                    backtrack_data = self._get_data_from_keys(backtrack_node)
                    #Remove the current leaf node from the global data tree
                    backtrack_data['out'].pop(current_node[-1], None)
                    #Remove 'out' key if it became empty
                    if not backtrack_data['out']:
                        backtrack_data.pop('out', None)
                    current_node = backtrack_node
                else:
                    current_node = None

    def subscribe_event(self, event: str, callback: Callable) -> None:
        """
            Registers the given callback to the
            given event.
        """
        self._event_callbacks[event].append(callback)
    
    def notify_new_node(self, node: dict) -> None:
        """
            Notifies all subscribers that we reached a new node.
        """     
        LOG.info('%s | Deconstruction: NEW_NODE %s', self.file_name, node['type'])
        self._raise_event(NEW_NODE_EVENT, node)

    def notify_backtracking(self, backtrack_amount: int) -> None:
        """
            Notifies all subscribers that we are backtracking because
            we reached a leaf.

            The backtrack_amount is how many back hop have been done.
        """
        LOG.info('%s | Deconstruction: BACKTRACK %s', self.file_name, backtrack_amount)
        self._raise_event(BACKTRACKING_EVENT, backtrack_amount)

    def _get_data_from_keys(self, keys: Tuple[str]) -> dict:
        """
            Returns the right node's dictionnary from the 
            loaded data tree following a list of keys.
        """
        if not keys:
            raise ValueError('keys shoudn\'t be empty or None.')

        keys = list(keys)
        current_dict = self._loaded_data[keys.pop(0)]
        while keys:
            current_dict = current_dict[keys.pop(0)]
        return current_dict

    def _load_yaml(self, file_name: str) -> dict:
        """
            Load the YAML specification file into the
            data dictionnary of the deconstructor.
        """
        path = Path(Path('analyser/rules_specifications') / Path(file_name + '.yaml')).resolve()
        with open(str(path), 'r') as file:
            try:
                return yaml.safe_load(file)
            except yaml.YAMLError as exc:
                LOG.error('Error while loading the YAML rule file %s: %s',
                          file_name, exc)
    
    def _raise_event(self, event_name: str, *args: any) -> None:
        """
            Executes all registered callbacks of 
            the given event.
        """
        for callback in self._event_callbacks[event_name]:
            callback(*args)

    def _init_event_callbacks(self) -> None:
        """
            Initializes all events and empty callbacks list.
        """
        self._event_callbacks: Dict[str, Callable] = dict()
        self._event_callbacks[NEW_NODE_EVENT] = []
        self._event_callbacks[BACKTRACKING_EVENT] = []