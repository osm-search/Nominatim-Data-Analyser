from typing import Any, Callable, Deque, Dict, List
from collections import deque
from ...logger.logger import LOG

NEW_NODE_EVENT = 'new_node'
BACKTRACKING_EVENT = 'backtracking'

class PipelineDeconstructor():
    """
        Deconstructs a pipeline specification following a tree
        structure.

        Raises events throughout the entire deconstruction process.
        It uses a backtracking system to go back on upper nodes
        when reaching a leaf.
    """
    def __init__(self, pipeline_specification: Dict, rule_name: str) -> None:
        #Add a root node needed for the exploration of the tree
        self._pipeline_specification = {
            'ROOT_NODE': { 
                    'type': 'ROOT_NODE',
                    'out': pipeline_specification
                }
        }
        self.rule_name = rule_name
        self.current_node: Dict = None
        self.nodes_history: Deque[Dict] = deque()
        self._init_event_callbacks()

    def deconstruct(self) -> None:
        """
            Explores the pipeline specification tree.
        """
        self.current_node: Dict = self._pipeline_specification['ROOT_NODE']
        self._send_current_node_and_explore()

    def _send_current_node_and_explore(self) -> None:
        """
            Notifies that a new node has been reached and
            keep exploring the tree.
        """
        self._notify_new_node(self.current_node)
        self._explore_deeper_or_backtrack()

    def _explore_deeper_or_backtrack(self) -> None:
        """
            If the current node still has an 'out' field, keep exploring
            deeper. Otherwise backtrack in the tree.
        """
        if 'out' in self.current_node:
            self.nodes_history.append(self.current_node)
            self.current_node = self.current_node['out'].pop(next(iter(self.current_node['out'])))
            self._send_current_node_and_explore()
        else:
            self._backtrack()
    
    def _backtrack(self) -> None:
        """
            Backtracks in the tree by getting the top node in the
            nodes_history deque. 

            If there is no node left in the nodes_history, 
            the exploring process is terminated naturally.

            Then keep exploring.
        """
        if self.nodes_history:
            #backtrack
            self._notify_backtracking()
            self.current_node = self.nodes_history.popleft()
            #Remove 'out' key if it became empty
            if not self.current_node['out']:
                self.current_node.pop('out', None)
            self._explore_deeper_or_backtrack()

    def subscribe_event(self, event: str, callback: Callable) -> None:
        """
            Registers the given callback to the
            given event.
        """
        self._event_callbacks[event].append(callback)
    
    def _notify_new_node(self, node: dict) -> None:
        """
            Notifies all subscribers that we reached a new node.
        """
        LOG.info('<%s> Deconstruction -> NEW_NODE %s', self.rule_name, node['type'])
        self._raise_event(NEW_NODE_EVENT, node)

    def _notify_backtracking(self,) -> None:
        """
            Notifies all subscribers that we are backtracking because
            the deconstructor reached a leaf.
        """
        LOG.info('<%s> Deconstruction -> BACKTRACK', self.rule_name)
        self._raise_event(BACKTRACKING_EVENT)

    def _raise_event(self, event_name: str, *args: Any) -> None:
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
        self._event_callbacks: Dict[str, List[Callable]] = dict()
        self._event_callbacks[NEW_NODE_EVENT] = []
        self._event_callbacks[BACKTRACKING_EVENT] = []
