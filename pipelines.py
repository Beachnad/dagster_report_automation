from dagster import pipeline, PresetDefinition
from modes import default_mode
from solids.data_asset import data_asset
from solids.excel_report import excel_report
from solids.email_report import email_report


@pipeline(
    mode_defs=[default_mode],
    preset_defs=[
        PresetDefinition(
            name='example',
            run_config={
                'solids': {
                    'data_asset': {
                        'config': {
                            'csv': {
                                'path': 'https://gist.githubusercontent.com/netj/8836201/raw/6f9306ad21398ea43cba4f7d537619d0e07d5ae3/iris.csv'
                            }
                        }
                    },
                    'excel_report': {
                        'config': {
                            'subtitle': 'Common Introductory Dataset for Machine Learning',
                            'title': 'Iris Dataset'
                        }
                    },
                    'email_report': {
                        'config': {
                            'report_name': 'Iris Dataset.xlsx',
                            'subject': 'Iris Dataset Report',
                            'to': [{'env': 'EXCHANGE_EMAIL'}]
                        }
                    }
                }
            }
        )
    ]
)
def report_pipeline():
    df = data_asset()
    wb = excel_report(df)
    email_report(wb)
