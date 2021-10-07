from dagster import solid, SolidExecutionContext, StringSource
from openpyxl import Workbook
import exchangelib
from tempfile import TemporaryDirectory
import os


@solid(
    required_resource_keys={'exchange_account'},
    config_schema={
        'subject': str,
        'to': [StringSource],
        'report_name': str
    }
)
def email_report(context: SolidExecutionContext, wb: Workbook):
    # Get the account coded as a resource.
    exchange_account: exchangelib.Account = context.resources.exchange_account

    # Create a message object
    m = exchangelib.Message(
        account=exchange_account,
        subject=context.solid_config['subject'],
        to_recipients=context.solid_config['to']
    )

    # Get a bytes representation of the workbook. My feeling is that there
    # is a better way to do this, but it works.
    with TemporaryDirectory() as tmp_dir:
        temp_path = os.path.join(tmp_dir, 'temp.xlsx')
        wb.save(temp_path)
        with open(temp_path, 'rb') as f:
            content = f.read()

    # Attach report to the message
    m.attach(exchangelib.FileAttachment(
        name=context.solid_config['report_name'],
        content=content
    ))

    # Send it!
    m.send()
