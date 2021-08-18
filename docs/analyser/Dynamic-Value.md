# The DynamicValue type

## DynamicValue class

A DynamicValue is an object which should be resolved at runtime to return a concrete value.

Data extracted by the query in a rule can have different fields values which should be handled differently by the pipes. The DynamicValue class was introduced to allow this while keeping a static [YAML Rule Specification](YAML-Rule-Specification.md).

There is multiple type of dynamic value but each of them inherits from the DynamicValue base class.

This class contains one important abstract method which is implemented by each subclasses, the `resolve` method:

```python
@abstractmethod
def resolve(self, data: Dict) -> Any:
    """
        Assigns a concrete value to the dynamic value
        based on the input data dictionnary.
    """
    return
```

The input data dictionnary are the data which will be used to resolve the dynamic value.

We can take the [Variable](../analyser/core/dynamic_value/variable.py) class as an example. The resolve method basically searchs for the `name` key in the input data dictionnary where `name` is the variable name given in the YAML Specification. The value corresponding to this key is then returned.

## Resolver

The `resolver` is used to easily resolve DynamicValue classes even when there are nested DynamicValue:

```yaml
- !switch
    expression: osm_type
    cases:
        'N': 
        node_id: !variable osm_id
        'W': 
        way_id: !variable osm_id
        'R': 
        relation_id: !variable osm_id
```

In this specification we can see that there is `!variable` types nested inside a `!switch` type. When the switch will be resolved, a `Variable` object will be returned, hence it needs to also be resolved.

The [resolver](../analyser/core/dynamic_value/resolver.py) can handle this easily when we call the `resolve_all` function:

```python
def resolve_all(data_to_resolve: Any, resolver_data: Dict, ) -> Any:
    """
        Resolves the given data_to_resolve by resolving all data inside which are of type DynamicValue. The resolved data are resolved again if they also contain DynamicValue.

        Parameter resolver_data is the data dictionnary used to resolve the dynamic values.
    """
```

This function is for example used in the `process` method of the [GeoJSONFeatureConverter](../analyser/core/pipes/output_formatters/geojson_feature_converter.py) to resolve the properties dynamically. This is needed because often we want to create different properties based on the geometry type of the GeoJSON feature (node, way, relation).

## All dynamic values

The dynamic values currently implemented are the following:

* Switch (!switch)
* Variable (!variable)

More explanation on them and especially on their YAML Specification can be found in the [Syntax section (under custom types) of the YAML Rule Specification chapter](YAML-Rule-Specification.md#Syntax).