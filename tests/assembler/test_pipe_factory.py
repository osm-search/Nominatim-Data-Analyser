from analyser.core.assembler.pipe_factory import PipeFactory
from analyser.core.exceptions import YAMLSyntaxException
import pytest

def test_assemble_pipe_ok() -> None:
    """
        Test the assemble_pipe() method.
        It should runs whithout any problem.
    """
    node_data = {
        'test': 'oui',
        'type': 'GeometryConverter',
        'geometry_type': 'Node'
    }
    PipeFactory.assemble_pipe(node_data, None)

def test_assemble_pipe_no_type() -> None:
    """
        Test the assemble_pipe() method.
        A YAML exception should be returned if the node_data
        given as parameter doesn't contain the 'type' key.
    """
    node_data = {
        'test': 'oui'
    }
    with pytest.raises(YAMLSyntaxException, match='Each node of the tree \(pipe\) should have a type defined.'):
        PipeFactory.assemble_pipe(node_data, None)

def test_assemble_pipe_wrong_type() -> None:
    """
        Test the assemble_pipe() method.
        A YAML exception should be returned if the node_data
        given as parameter contains a 'type' which doesn't exist.
    """
    node_data = {
        'test': 'oui',
        'type': 'wrongtypewhichdoesntexist'
    }
    with pytest.raises(YAMLSyntaxException, match='The type wrongtypewhichdoesntexist doesn\'t exist.'):
        PipeFactory.assemble_pipe(node_data, None)