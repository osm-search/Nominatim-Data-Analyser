from typing import Any, cast
from ..dynamic_value.switch import Switch
from ..dynamic_value.variable import Variable
from ..assembler import PipelineAssembler
from .. import Pipe
from ...logger.logger import LOG
from pathlib import Path
import yaml

base_rules_path = Path(__file__, '..', '..', '..', 'rules_specifications').resolve()

def load_yaml_rule(file_name: str) -> dict[str, Any]:
    """
        Load the YAML specification file.
        YAML constructors are added to handle custom types in the YAML.
    """
    def _sub_pipeline(loader: yaml.SafeLoader, node: yaml.Node) -> Pipe:
        if not isinstance(node, yaml.MappingNode):
            raise RuntimeError("!switch expects mapping.")
        return sub_pipeline_constructor(loader, node, file_name)

    yaml.add_constructor(u'!sub-pipeline', _sub_pipeline, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!variable', variable_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!switch', switch_constructor, Loader=yaml.SafeLoader)

    path = Path(base_rules_path / Path(file_name + '.yaml')).resolve()
    with open(str(path), 'r') as file:
        try:
            loaded = cast(dict[str, Any], yaml.safe_load(file))
        except yaml.YAMLError as exc:
            LOG.error('Error while loading the YAML rule file %s: %s',
                      file_name, exc)
            raise

    return loaded

def sub_pipeline_constructor(loader: yaml.SafeLoader, node: yaml.MappingNode,
                             rule_name: str) -> Pipe:
    """
        Loads the pipeline specification from the YAML node and
        assembles a pipeline with the PipelineAssembler.

        This constructor is used for the !sub-pipeline custom type.
    """
    pipeline_specification = cast(dict[str, Any], loader.construct_mapping(node, deep=True))
    return PipelineAssembler(pipeline_specification, rule_name).assemble()

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
