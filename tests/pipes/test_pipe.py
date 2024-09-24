
from nominatim_data_analyser.core.exceptions.yaml_syntax_exception import YAMLSyntaxException
from nominatim_data_analyser.core.pipes.data_processing import GeometryConverter
from nominatim_data_analyser.core.qa_rule import ExecutionContext
from nominatim_data_analyser.core.pipes import FillingPipe
import logging
import pytest

def test_plug_pipe(filling_pipe: FillingPipe, geometry_converter: GeometryConverter) -> None:
    filling_pipe.plug_pipe(geometry_converter)
    assert filling_pipe.next_pipes.pop() == geometry_converter

def test_process_and_next(filling_pipe: FillingPipe, execution_context: ExecutionContext, monkeypatch) -> None:
    """
        Test the process_and_next() method. The process() method of the
        two pipes should be called.
    """
    filling_pipe2 = FillingPipe({}, execution_context)
    filling_pipe.next_pipes.add(filling_pipe2)
    x = 0
    def callback(self, data = None):
        nonlocal x
        x += 1
    monkeypatch.setattr('nominatim_data_analyser.core.pipes.filling_pipe.FillingPipe.process',
                        callback)
    filling_pipe.process_and_next()
    assert x == 2

def test__str__(filling_pipe: FillingPipe) -> None:
    """
        Test the __str__
    """
    assert str(filling_pipe) == type(filling_pipe).__name__ + ' ' + str(filling_pipe.id)

def test_extract_data_basic(filling_pipe: FillingPipe) -> None:
    """
        Test the extract_data() method with no default value provided and
        required = False.
    """
    filling_pipe.data['test_data'] = 'test_data_value'
    assert filling_pipe.extract_data('test_data') == 'test_data_value'
    #The second time the value is None as it has already been extracted (default = None is returned).
    assert filling_pipe.extract_data('test_data') == None

def test_extract_data_with_default(filling_pipe: FillingPipe) -> None:
    """
        Test the extract_data() method with a default value provided and
        required = False.
    """
    assert filling_pipe.extract_data('test_data', 'test_data_value') == 'test_data_value'

@pytest.mark.parametrize("default", [(None), ('test_data_value')])
def test_extract_data_with_required(filling_pipe: FillingPipe, default) -> None:
    """
        Test the extract_data() method with/without a default value provided and
        required = True.
    """
    with pytest.raises(YAMLSyntaxException, match='The field "test_data" is required for the pipe of type FillingPipe'):
        filling_pipe.extract_data('test_data', default, True)

def test_log(filling_pipe: FillingPipe) -> None:
    """
        Test the execution of the log() method.
    """
    filling_pipe.log('test_message', logging.WARN)

@pytest.fixture
def filling_pipe(execution_context: ExecutionContext) -> FillingPipe:
    return FillingPipe({}, execution_context)
