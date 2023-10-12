import pytest
from algokit_utils import (
    ApplicationClient,
    ApplicationSpecification,
    get_localnet_default_account,
)
from algosdk.v2client.algod import AlgodClient

from smart_contracts.board_name import contract as board_name_contract


@pytest.fixture(scope="session")
def board_name_app_spec(algod_client: AlgodClient) -> ApplicationSpecification:
    return board_name_contract.app.build(algod_client)


@pytest.fixture(scope="session")
def board_name_client(
    algod_client: AlgodClient, board_name_app_spec: ApplicationSpecification
) -> ApplicationClient:
    client = ApplicationClient(
        algod_client,
        app_spec=board_name_app_spec,
        signer=get_localnet_default_account(algod_client),
    )
    client.create()
    return client


def test_says_hello(board_name_client: ApplicationClient) -> None:
    result = board_name_client.call(board_name_contract.hello, name="World")

    assert result.return_value == "Hello, World"
