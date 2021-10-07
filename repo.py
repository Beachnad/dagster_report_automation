from dagster import repository
from pipelines import report_pipeline


@repository
def main_repository():
    return [report_pipeline]
