from nominatim_data_analyser.core.pipes import FillingPipe
from nominatim_data_analyser.core.assembler.pipeline_assembler import PipelineAssembler


def test_assemble_single_item_pipe() -> None:
    spec = [
        {
            'type': 'SQLProcessor',
            'query': 'SELECT 1 FROM foo'
        }
    ]

    pipeline = PipelineAssembler('test_rule').assemble(spec)

    assert isinstance(pipeline, FillingPipe)
