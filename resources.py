from dagster import resource, InitResourceContext, StringSource, Field
import exchangelib


class MockDatabase:
    pass


@resource
def database_1(_):
    return MockDatabase()


@resource
def database_2(_):
    return MockDatabase()


@resource({
    'email': Field(StringSource, default_value={'env': 'EXCHANGE_EMAIL'}),
    'username': Field(StringSource, default_value={'env': 'EXCHANGE_USER'}),
    'password': Field(StringSource, default_value={'env': 'EXCHANGE_PASSWORD'}),
    'server': Field(StringSource, default_value={'env': 'EXCHANGE_SERVER'})
})
def exchange_account(init_context: InitResourceContext):
    init_context.log.debug(init_context.resource_config)

    credentials = exchangelib.Credentials(
        username=init_context.resource_config['username'],
        password=init_context.resource_config['password']
    )
    config = exchangelib.Configuration(server=init_context.resource_config['server'], credentials=credentials)

    return exchangelib.Account(
        primary_smtp_address=init_context.resource_config['email'],
        config=config,
        autodiscover=False,
        access_type=exchangelib.DELEGATE
    )
