from pathlib import Path
from enum import Enum
from pydantic import BaseModel
from balpy.graph.graph import Client, BALANCER_API_ENDPOINT, RequestsHTTPTransport, gql


BALANCER_SWAP_QUERY = gql((Path(__file__).parent / "balancer.graphql").read_text())


class GqlChain(Enum):
    ARBITRUM = "ARBITRUM"
    AVALANCHE = "AVALANCHE"
    BASE = "BASE"
    FANTOM = "FANTOM"
    FRAXTAL = "FRAXTAL"
    GNOSIS = "GNOSIS"
    HYPEREVM = "HYPEREVM"
    MAINNET = "MAINNET"
    MODE = "MODE"
    OPTIMISM = "OPTIMISM"
    POLYGON = "POLYGON"
    SEPOLIA = "SEPOLIA"
    SONIC = "SONIC"
    ZKEVM = "ZKEVM"


class GqlPoolEventType(Enum):
    ADD = "ADD"
    REMOVE = "REMOVE"
    SWAP = "SWAP"


class GqlPoolEventsDataRange(Enum):
    SEVEN_DAYS = "SEVEN_DAYS"
    THIRTY_DAYS = "THIRTY_DAYS"
    NINETY_DAYS = "NINETY_DAYS"


class GqlPoolEventsFilter(BaseModel, use_enum_values=True):
    chainIn: list[GqlChain] | None = None
    poolIdIn: list[str] | None = None
    range: GqlPoolEventsDataRange | None = None
    typeIn: list[GqlPoolEventType] | None = None
    userAddress: str | None = None
    valueUSD_gt: float | None = None
    valueUSD_gte: float | None = None


def get_trades_balancer(
    address: str,
    chain: GqlChain,
    first: int = 1,
    skip: int = 0,
) -> list[dict]:

    transport = RequestsHTTPTransport(
        url=BALANCER_API_ENDPOINT,
        verify=True,
        retries=3,
    )

    client = Client(
        transport=transport,
        fetch_schema_from_transport=True,
    )

    flt = GqlPoolEventsFilter(
        chainIn    = [chain],
        typeIn     = [GqlPoolEventType.SWAP],
        userAddress= address,
    )

    variables = {
        "filter": flt.model_dump(exclude_none=True),
        "first":  first,
        "skip":   skip,
    }

    all_events = []
    with client as session:
        # while True:
        for _ in range(2):
            result = session.execute(BALANCER_SWAP_QUERY, variable_values=variables)
            batch = result.get("poolEvents", [])
            if not batch:
                break
            all_events.extend(batch)
            variables["skip"] += len(batch)

    return all_events



if __name__ == "__main__":
    address = "0xafecd96c59b253427317be597cde368ae8395884"
    chain = GqlChain.BASE
    trades = get_trades_balancer(
        address=address,
        chain=chain,
    )
    breakpoint()
