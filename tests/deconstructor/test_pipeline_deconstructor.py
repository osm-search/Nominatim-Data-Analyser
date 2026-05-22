import pytest
from itertools import count

from nominatim_data_analyser.core.deconstructor.pipeline_deconstructor import (
    BACKTRACKING_EVENT,
    NEW_NODE_EVENT,
    PipelineDeconstructor)


def test_deconstruct_basic() -> None:
    """
        Test the deconstruct() method with a basic pipeline specification.
        Checks for the right values in new_nodes received by the deconstructor and the
        backtrack amount.
    """
    node3 = {
        'type': 'TEST_TYPE3'
    }
    node2 = {
        'type': 'TEST_TYPE2',
        'out': {
            'OUT_NODE_3': node3
        }
    }
    node1 = {
        'NODE1': {
            'type': 'TEST_TYPE1',
            'out': {
                'OUT_NODE_2': node2
            }
        }
    }
    # Store new nodes added
    new_nodes = list()
    backtrack_count = count()

    pipeline_deconstructor = PipelineDeconstructor(node1, 'test_rule')
    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(new_nodes.append)
    pipeline_deconstructor._event_callbacks[BACKTRACKING_EVENT].append(
        lambda: next(backtrack_count))
    pipeline_deconstructor.deconstruct()
    assert new_nodes == [
        {'type': 'ROOT_NODE'},
        {'type': 'TEST_TYPE1'},
        {'type': 'TEST_TYPE2'},
        {'type': 'TEST_TYPE3'}
    ]
    assert next(backtrack_count) == 3


def test_deconstruct_double_out() -> None:
    """
        Test the deconstruct() method with a a more advanced pipeline specification.
        One node contains double node in its 'out' field.
        Checks for the right values in new_nodes received by the deconstructor and the
        backtrack amount.
    """
    node4 = {
        'type': 'TEST_TYPE4'
    }
    node3 = {
        'type': 'TEST_TYPE3'
    }
    node2 = {
        'type': 'TEST_TYPE2',
        'out': {
            'OUT_NODE_3': node3
        }
    }
    node1 = {
        'NODE1': {
            'type': 'TEST_TYPE1',
            'out': {
                'OUT_NODE_2': node2,
                'OUT_NODE_4': node4
            }
        }
    }
    # Store new nodes added
    new_nodes = list()
    backtrack_count = count()

    pipeline_deconstructor = PipelineDeconstructor(node1, 'test_rule')
    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(new_nodes.append)
    pipeline_deconstructor._event_callbacks[BACKTRACKING_EVENT].append(
        lambda: next(backtrack_count))
    pipeline_deconstructor.deconstruct()
    assert new_nodes == [
        {'type': 'ROOT_NODE'},
        {'type': 'TEST_TYPE1'},
        {'type': 'TEST_TYPE2'},
        {'type': 'TEST_TYPE3'},
        {'type': 'TEST_TYPE4'}
    ]
    assert next(backtrack_count) == 4


def test_send_current_node_and_explore(
        pipeline_deconstructor: PipelineDeconstructor, monkeypatch) -> None:
    """
        Test the _send_current_node_and_explore() method.
        Only check that the methods inside are well called.
    """
    x = count()

    monkeypatch.setattr('nominatim_data_analyser.core.deconstructor.pipeline_deconstructor.PipelineDeconstructor._notify_new_node',  # noqa: E501
                        lambda *a, **kw: next(x))
    monkeypatch.setattr('nominatim_data_analyser.core.deconstructor.pipeline_deconstructor.PipelineDeconstructor._explore_deeper_or_backtrack',  # noqa: E501
                        lambda *a, **kw: next(x))
    pipeline_deconstructor.deconstruct()
    assert next(x) == 2


def test_explore_deeper_or_backtrack(
        pipeline_deconstructor: PipelineDeconstructor, monkeypatch) -> None:
    """
        Test the _explore_deeper_or_backtrack() method.
        the node in 'out' should be popped out and if is_new_node
        is equal to True it should be sent to the new node event callback.
    """
    node3 = {
        'type': 'TEST_TYPE3'
    }
    node2 = {
        'type': 'TEST_TYPE2',
        'out': {
            'OUT_NODE_3': node3
        }
    }
    node1 = {
        'type': 'TEST_TYPE1',
        'out': {
            'OUT_NODE_2': node2
        }
    }
    # Store new nodes added
    new_nodes = list()
    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(new_nodes.append)

    # Mock a dumb _backtrack method.
    monkeypatch.setattr('nominatim_data_analyser.core.deconstructor.pipeline_deconstructor.PipelineDeconstructor._backtrack',  # noqa: E501
                        lambda self: 1)

    pipeline_deconstructor.current_node = node1
    pipeline_deconstructor._explore_deeper_or_backtrack()
    assert new_nodes == [node2, node3]
    assert not node1['out'] and not node2['out']

    assert len(pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT]) == 1


def test_backtrack(pipeline_deconstructor: PipelineDeconstructor, monkeypatch) -> None:
    """
        Test the _backtrack() method. It should set the current node to the top node
        of the nodes_history and this node should be removed from the nodes_history.

        If there is nothing left in the 'out' of the node, the field should be removed.
    """
    node = {
        'type': 'TEST_TYPE',
        'out': {
            'OUT_NODE_1': {},
            'OUT_NODE_2': {}
        }
    }
    pipeline_deconstructor.nodes_history.append(node)

    # Mock a dumb _explore_deeper_or_backtrack method to not launch the recursion.
    monkeypatch.setattr('nominatim_data_analyser.core.deconstructor.pipeline_deconstructor.PipelineDeconstructor._explore_deeper_or_backtrack',  # noqa: E501
                        lambda self: 1)

    pipeline_deconstructor._backtrack()
    assert pipeline_deconstructor.current_node == node
    assert not pipeline_deconstructor.nodes_history
    # Test that if out it empty it gets removed.
    node['out'] = {}
    pipeline_deconstructor.nodes_history.append(node)
    pipeline_deconstructor._backtrack()
    assert 'out' not in pipeline_deconstructor.current_node


def test_subscribe_event(pipeline_deconstructor: PipelineDeconstructor) -> None:
    """
        Test the subscribe_event() method.
    """
    pipeline_deconstructor.subscribe_event(NEW_NODE_EVENT, None)
    assert len(pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT]) == 1


def test_notify_new_node(pipeline_deconstructor: PipelineDeconstructor) -> None:
    """
        Test the _notify_new_node() method.
        Checks that the callback is called as it should.
    """
    node = {
        'type': 'GeometryConverter',
        'geometry_type': 'Node'
    }
    x = []
    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(x.append)
    pipeline_deconstructor._notify_new_node(node)
    assert x == [node]


def test_notify_backtracking(pipeline_deconstructor: PipelineDeconstructor) -> None:
    """
        Test the _notify_backtracking() method.
        Checks that the callback is called as it should.
    """
    x = count()
    pipeline_deconstructor._event_callbacks[BACKTRACKING_EVENT].append(lambda: next(x))
    pipeline_deconstructor._notify_backtracking()
    assert next(x) == 1


def test_raise_event(pipeline_deconstructor: PipelineDeconstructor) -> None:
    """
        Test the _raise_event() method.
        Checks that the callbacks are called as they should.
    """
    x = count()
    y = count()

    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(lambda: next(x))
    pipeline_deconstructor._event_callbacks[NEW_NODE_EVENT].append(lambda: next(y))
    pipeline_deconstructor._raise_event(NEW_NODE_EVENT)
    assert next(x) == 1
    assert next(y) == 1


def test_init_event_callbacks(pipeline_deconstructor: PipelineDeconstructor) -> None:
    """
        Test the initialization of the _event_callbacks dictionnary
        through the _init_event_callbacks() method.
    """
    # the _init_event_callbacks() is initally called in the constructor.
    pipeline_deconstructor.__dict__.pop('_event_callbacks', None)
    assert '_event_callbacks' not in pipeline_deconstructor.__dict__

    pipeline_deconstructor._init_event_callbacks()
    assert '_event_callbacks' in pipeline_deconstructor.__dict__
    assert NEW_NODE_EVENT in pipeline_deconstructor._event_callbacks
    assert BACKTRACKING_EVENT in pipeline_deconstructor._event_callbacks


@pytest.fixture
def pipeline_deconstructor() -> PipelineDeconstructor:
    return PipelineDeconstructor({}, 'test_rule')
