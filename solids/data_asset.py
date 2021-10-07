from dagster import solid, Selector, SolidExecutionContext
import pandas as pd


@solid(
    required_resource_keys={'database_1', 'database_2'},
    config_schema=Selector({
        'query': {
            'sql': str,
            'database': str
        },
        'csv': {
            'path': str
        }
    })
)
def data_asset(context: SolidExecutionContext) -> pd.DataFrame:
    if query_conf := context.solid_config.get('query', None):
        db = context.resources.__getattribute__(query_conf['database'])
        df = pd.read_sql_query(query_conf['sql'], db)
    elif file_conf := context.solid_config.get('csv', None):
        df = pd.read_csv(file_conf['path'])

    return df
