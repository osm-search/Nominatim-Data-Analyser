from textwrap import dedent

import pytest
import yaml

from nominatim_data_analyser.core.dynamic_value.resolver import resolve_all
from nominatim_data_analyser.core.yaml_loader import load_yaml_rule
from nominatim_data_analyser.core import Pipe


class PipeModules:

    class AppendString(Pipe):

        def process(self, data):
            data['out'].append(resolve_all(self.data['data'], data))
            return data

    class WithSub(Pipe):

        def process(self, data):
            data['out'].append(self.data['sub'].process_and_next({'out': []})['out'])
            return data


@pytest.fixture
def yaml_file(tmp_path, monkeypatch):
    ruledir = tmp_path / 'rules'
    ruledir.mkdir()
    monkeypatch.setattr('nominatim_data_analyser.core.assembler.pipe_factory.pipes_module',
                        PipeModules)

    def _mkfile(rule, content):
        outfile = ruledir / f"{rule}.yaml"
        outfile.write_text(dedent(content), encoding='utf-8')
        return outfile

    return _mkfile


def test_load_yaml_rule(yaml_file) -> None:
    """
        Test the load_yaml_rule() function with a test yaml file.
    """
    rule = yaml_file('test_load_yaml', """\
        - type: AppendString
          data: Foo
        - type: AppendString
          data: Bar
        """)

    pipe = load_yaml_rule(rule)

    assert pipe.process_and_next({'out': []})['out'] == ['Foo', 'Bar']


def test_load_wrong_yaml(yaml_file) -> None:
    rule = yaml_file('test_bad_yaml', """\
        - >>>>type: AppendString
          data: Foo
        - type: AppendString
          data: Bar
        """)
    with pytest.raises(yaml.YAMLError):
        load_yaml_rule(rule)


def test_construct_sub_pipeline(yaml_file) -> None:
    rule = yaml_file('test_load_yaml', """\
        - type: WithSub
          sub: !sub-pipeline
            - type: AppendString
              data: Bar
        - type: AppendString
          data: Foo
        """)

    pipe = load_yaml_rule(rule)

    assert pipe.process_and_next({'out': []})['out'] == [['Bar'], 'Foo']


def test_construct_switch(yaml_file) -> None:
    rule = yaml_file('test_load_yaml', """\
        - type: AppendString
          data: !switch
            expression: inval
            cases:
              A: alpha
              B: beta
        """)
    pipe = load_yaml_rule(rule)

    assert pipe.process_and_next({'inval': 'A', 'out': []})['out'] == ['alpha']
    assert pipe.process_and_next({'inval': 'B', 'out': []})['out'] == ['beta']


def test_construct_variable(yaml_file) -> None:
    rule = yaml_file('test_load_yaml', """\
        - type: AppendString
          data: !variable inval
        """)
    pipe = load_yaml_rule(rule)

    assert pipe.process_and_next({'inval': 'A', 'out': []})['out'] == ['A']
