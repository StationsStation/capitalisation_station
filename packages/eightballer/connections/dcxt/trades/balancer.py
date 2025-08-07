from balpy.graph.graph import Client, BALANCER_API_ENDPOINT, Chain, RequestsHTTPTransport, gql


BALANCER_SWAP_QUERY = gql("""
query GetSwapsForAddress(
  $address: String!
  $chain: [GqlChain!]!
  $first: Int!
  $skip: Int!
) {
  poolEvents(
    first: $first
    skip: $skip
    where: {
      typeIn: [SWAP]
      chainIn: $chain
      userAddress: $address
    }
  ) {
    __typename
    ... on GqlPoolSwapEventV3 {
      id
      type
      timestamp
      poolId
      userAddress
      valueUSD
      chain
      logIndex
      tx
      tokenIn {
        address
      }
      tokenOut {
        address
      }
    }
  }
}
"""
)

def get_trades_balancer(
    address: str,
    chain: Chain,
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

    variables = {
        "address": address,
        "first": first,
        "skip": skip,
        "chain": chain.name,
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
    chain = Chain.BASE
    trades = get_trades_balancer(
        address=address,
        chain=chain,
    )
    breakpoint()
