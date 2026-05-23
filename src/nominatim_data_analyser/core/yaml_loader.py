from pathlib import Path
import logging

import yaml

from .dynamic_value.switch import Switch
from .dynamic_value.variable import Variable
from .assembler.pipeline_assembler import PipelineAssembler
from . import Pipe


LOG = logging.getLogger()


def load_yaml_rule(rule_file: Path) -> Pipe:
    """
        Load the YAML specification file.
        YAML constructors are added to handle custom types in the YAML.
    """
    def _sub_pipeline(loader: yaml.SafeLoader, node: yaml.Node) -> Pipe:
        if not isinstance(node, yaml.SequenceNode):
            raise RuntimeError("!sub-pipeline expects list.")
        return sub_pipeline_constructor(loader, node, rule_file.stem)

    yaml.add_constructor(u'!sub-pipeline', _sub_pipeline, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!variable', variable_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!switch', switch_constructor, Loader=yaml.SafeLoader)

    with rule_file.open('r') as file:
        try:
            loaded = yaml.safe_load(file)
        except yaml.YAMLError as exc:
            LOG.error('Error while loading the YAML rule file %s: %s',
                      rule_file.stem, exc)
            raise

    if not isinstance(loaded, list):
        raise RuntimeError('Pipeline description must be a list.')

    return PipelineAssembler(rule_file.stem).assemble(loaded)


def sub_pipeline_constructor(loader: yaml.SafeLoader, node: yaml.SequenceNode,
                             rule_name: str) -> Pipe:
    """
        Loads the pipeline specification from the YAML node and
        assembles a pipeline with the PipelineAssembler.

        This constructor is used for the !sub-pipeline custom type.
    """
    pipeline_specification = loader.construct_sequence(node, deep=True)
    assert isinstance(pipeline_specification, list)

    return PipelineAssembler(rule_name).assemble(pipeline_specification)


def variable_constructor(loader: yaml.SafeLoader, node: yaml.Node) -> Variable:
    """
        Creates a Variable object using the node's data.
    """
    if not isinstance(node, yaml.ScalarNode):
        raise RuntimeError("!variable expects scalar value.")

    return Variable(loader.construct_scalar(node))


def switch_constructor(loader: yaml.SafeLoader, node: yaml.Node) -> Switch:
    """
        Creates a Switch object using the node's data.
    """
    if not isinstance(node, yaml.MappingNode):
        raise RuntimeError("!switch expects mapping.")

    data = loader.construct_mapping(node, deep=True)
    return Switch(data['expression'], data['cases'])
