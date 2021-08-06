from analyser.core.assembler import PipelineAssembler
from analyser.logger.logger import LOG
from pathlib import Path
import yaml

base_rules_path = Path('analyser/rules_specifications')

def load_yaml_rule(file_name: str) -> dict:
    """
        Load the YAML specification file.
        YAML constructors are added to handle custom types in the YAML.
    """
    sub_pipeline_lambda = lambda loader, node: sub_pipeline_constructor(loader, node, file_name)
    yaml.add_constructor(u'!sub-pipeline', sub_pipeline_lambda, Loader=yaml.SafeLoader)

    path = Path(base_rules_path / Path(file_name + '.yaml')).resolve()
    with open(str(path), 'r') as file:
        try:
            return yaml.safe_load(file)
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