from ..dynamic_value.switch import Switch
from ..dynamic_value.variable import Variable
from ..assembler import PipelineAssembler
from ...logger.logger import LOG
from pathlib import Path
import yaml

base_rules_path = Path(__file__, '..', '..', '..', 'rules_specifications').resolve()

def load_yaml_rule(file_name: str) -> dict:
    """
        Load the YAML specification file.
        YAML constructors are added to handle custom types in the YAML.
    """
    sub_pipeline_lambda = lambda loader, node: sub_pipeline_constructor(loader, node, file_name)
    yaml.add_constructor(u'!sub-pipeline', sub_pipeline_lambda, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!variable', variable_constructor, Loader=yaml.SafeLoader)
    yaml.add_constructor(u'!switch', switch_constructor, Loader=yaml.SafeLoader)

    path = Path(base_rules_path / Path(file_name + '.yaml')).resolve()
    with open(str(path), 'r') as file:
        try:
            loaded = yaml.safe_load(file)
            return loaded
        except yaml.YAMLError as exc:
            LOG.error('Error while loading the YAML rule file %s: %s',
                        file_name, exc)
            raise

def sub_pipeline_constructor(loader: yaml.SafeLoader, node: yaml.MappingNode, rule_name):
    """
        Loads the pipeline specification from the YAML node and
        assembles a pipeline with the PipelineAssembler.

        This constructor is used for the !sub-pipeline custom type.
    """
    pipeline_specification = loader.construct_mapping(node, deep=True)
    return PipelineAssembler(pipeline_specification, rule_name).assemble()

def variable_constructor(loader: yaml.SafeLoader, node: yaml.ScalarNode):
    """
        Creates a Variable object using the node's data.
    """
    return Variable(loader.construct_scalar(node))

def switch_constructor(loader: yaml.SafeLoader, node: yaml.MappingNode):
    """
        Creates a Switch object using the node's data.
    """
    data = loader.construct_mapping(node, deep=True)
    return Switch(data['expression'], data['cases'])
