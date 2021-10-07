from dagster import ModeDefinition
from resources import database_1, database_2, exchange_account

default_mode = ModeDefinition(
    name="default",
    resource_defs={
        "database_1": database_1,
        'database_2': database_2,
        'exchange_account': exchange_account
    }
)
