from analyser.core.deconstructor import YAMLRuleDeconstructor
from analyser.core.data_fetching import SQLProcessor
from analyser.core.output_formatters import GeoJSONFormatter
from analyser.core.output_formatters import GeoJSONFeatureConverter
from analyser.core.output_formatters import LayerFormatter
from analyser.core.pipe import Pipe

class RuleAssembler():
    """
        Get data from the YAML deconstructor and
        assembles the rule's pipeline.
    """
    def __init__(self, yaml_name: str) -> None:
        self.deconstructor = YAMLRuleDeconstructor(yaml_name)
        self.first_pipe = None
        self.current_pipe = None

    def assemble(self) -> Pipe:
        """
            Assembles the rule's pipeline
        """
        sql_fetcher = self.deconstructor.get_next_sql_fetcher()
        while sql_fetcher:
            self.add_pipe(SQLProcessor(sql_fetcher['query'], sql_fetcher['outputs_types']))
            sql_fetcher = self.deconstructor.get_next_sql_fetcher()

        osmoscope_output = self.deconstructor.get_osmoscope_output()
        if osmoscope_output:
            self.add_pipe(GeoJSONFeatureConverter())
            if 'geojson' in osmoscope_output:
                self.add_pipe(GeoJSONFormatter(osmoscope_output['geojson']['file_name']))
            if 'layer_file' in osmoscope_output:
                layer_data = osmoscope_output['layer_file']
                layer_formatter = LayerFormatter(layer_data['layer_name'], layer_data['file_name'], layer_data['updates'])
                if 'docs' in layer_data:
                    for k, v in layer_data['docs'].items():
                        layer_formatter.add_doc(k, v)
                self.add_pipe(layer_formatter)

        return self.first_pipe

    def add_pipe(self, pipe: Pipe) -> None:
        """
            Add a pipe to the pipeline. This method is
            an assurance that the pipeline order is respected.
        """
        if self.first_pipe is None:
            self.first_pipe = pipe
        elif self.current_pipe is None:
            self.first_pipe.plug_pipe(pipe)
            self.current_pipe = pipe
        else:
            self.current_pipe = self.current_pipe.plug_pipe(pipe)
