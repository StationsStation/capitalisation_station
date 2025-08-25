"""Token data."""

import json
import functools
from enum import Enum
from pathlib import Path


class SupportedLedgers(Enum):
    """Supported ledgers."""

    ETHEREUM = "ethereum"
    GNOSIS = "gnosis"
    POLYGON = "polygon"
    ARBITRUM = "arbitrum"
    OPTIMISM = "optimism"
    BASE = "base"
    MODE = "mode"
    DERIVE = "derive"


NATIVE_ETH = "0xeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee"

LEDGER_TO_STABLECOINS = {
    SupportedLedgers.ETHEREUM: [
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI,
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
        "0x6b175474e89094c44da98b954eedeac495271d0f",  # DAI
        "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",  # USDC
    ],
    SupportedLedgers.OPTIMISM: [
        "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        "0x94b008aa00579c1307b0ef2c499ad98a8ce58e58",  # USDT
    ],
    SupportedLedgers.BASE: [
        "0x833589fcd6edb6e08f4c7c32d4f71b54bda02913",  # USDC
        "0x50c5725949a6f0c72e6c4a641f24049a917db0cb",  # DAI
        "0xd9aaec86b65d86f6a7b5b1b0c42ffa531710b6ca",  # usdcb
    ],
    SupportedLedgers.GNOSIS: [
        "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",  # wxdai
        "0x2a22f9c3b484c3629090feed35f17ff8f88f76f0",  # USDC.e
        "0xddafbb505ad214d7b80b1f830fccc89b60fb7a83",  # USDC
    ],
    SupportedLedgers.POLYGON: [
        "0x8f3cf7ad23cd3cadbd9735aff958023239c6a063",
        "0x3c499c542cef5e3811e1192ce70d8cc03d5c3359",  # USDC
    ],
    SupportedLedgers.ARBITRUM: [
        "0xDA10009cBd5D07dd0CeCc66161FC93D7c9000da1",
        "0xaf88d065e77c8cc2239327c5edb3a432268e5831",
    ],
    SupportedLedgers.MODE: [
        "0xd988097fb8612cc24eec14542bc03424c656005f",  # USDC on Mode
        "0x3f51c6c5927b88cdec4b61e2787f9bd0f5249138",
    ],
    SupportedLedgers.DERIVE: [],
}

LEDGER_TO_NATIVE_SYMBOL = {
    SupportedLedgers.ETHEREUM: "ETH",
    SupportedLedgers.OPTIMISM: "ETH",
    SupportedLedgers.BASE: "ETH",
    SupportedLedgers.GNOSIS: "xDAI",
    SupportedLedgers.POLYGON: "POL",
    SupportedLedgers.ARBITRUM: "ETH",
    SupportedLedgers.MODE: "ETH",
}

LEDGER_TO_WRAPPER = {
    SupportedLedgers.ETHEREUM: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    SupportedLedgers.OPTIMISM: "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
    SupportedLedgers.BASE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.GNOSIS: "0xe91d153e0b41518a2ce8dd3d7944fa863463a97d",
    SupportedLedgers.POLYGON: "0x0000000000000000000000000000000000001010",
    SupportedLedgers.ARBITRUM: "0x82aF49447D8a07e3bd95BD0d56f35241523fBab1",
    SupportedLedgers.MODE: "0x4200000000000000000000000000000000000006",
}
LEDGER_TO_OLAS = {
    SupportedLedgers.ETHEREUM: "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",
    SupportedLedgers.OPTIMISM: "0xfc2e6e6bcbd49ccf3a5f029c79984372dcbfe527",
    SupportedLedgers.BASE: "0x54330d28ca3357f294334bdc454a032e7f353416",
    SupportedLedgers.GNOSIS: "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f",
    SupportedLedgers.POLYGON: "0xFEF5d947472e72Efbb2E388c730B7428406F2F95",
    SupportedLedgers.ARBITRUM: "0x064f8b858c2a603e1b106a2039f5446d32dc81c1",
    SupportedLedgers.MODE: "0xcfD1D50ce23C46D3Cf6407487B2F8934e96DC8f9",
}

LEDGER_TO_WETH = {
    SupportedLedgers.ETHEREUM: "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
    SupportedLedgers.MODE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.BASE: "0x4200000000000000000000000000000000000006",
    SupportedLedgers.GNOSIS: "0x6a023ccd1ff6f2045c3309768ead9e68f978f6e1",
}


LEDGER_TO_TOKEN_LIST = {
    SupportedLedgers.ETHEREUM: set(
        [
            "0x0001a500a6b18995b03f44bb040a5ffc28e45cb0",  # olas
            "0xa0b86991c6218b36c1d19d4a2e9eb0ce3606eb48",
            "0xc02aaa39b223fe8d0a0e5c4f27ead9083c756cc2",
            "0x8236a87084f8b84306f72007f36f2618a5634494",  # lbtc
            "0xcd5fe23c85820f7b72d0926fc9b05b43e359b7ee",  # wrapped ethena eth
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.ETHEREUM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.ETHEREUM]]
    ),
    SupportedLedgers.OPTIMISM: set(
        [
            "0x0b2c639c533813f4aa9d7837caf62653d097ff85",
            "0xda10009cbd5d07dd0cecc66161fc93d7c9000da1",
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.OPTIMISM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.OPTIMISM]]
    ),
    SupportedLedgers.BASE: set(
        [
            "0x54330d28ca3357f294334bdc454a032e7f353416",  # OLAS
            "0xecac9c5f704e954931349da37f60e39f515c11c1",  # LBTC
            "0x04C0599Ae5A44757c0af6F9eC3b93da8976c150A",  # weETH
            "0x9d0e8f5b25384c7310cb8c6ae32c8fbeb645d083",  # DRV
            "0x4200000000000000000000000000000000000006",  # WETH
            "0xcbB7C0000aB88B473b1f5aFd9ef808440eed33Bf",  # CBBTC
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.BASE]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.BASE]]
    ),
    SupportedLedgers.GNOSIS: set(
        [
            "0xcE11e14225575945b8E6Dc0D4F2dD4C570f79d9f",  # olas
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.GNOSIS]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.GNOSIS]]
        + [LEDGER_TO_WETH[SupportedLedgers.GNOSIS]]
    ),
    SupportedLedgers.POLYGON: set(
        [
            "0xFEF5d947472e72Efbb2E388c730B7428406F2F95",  # olas
            "0x7ceb23fd6bc0add59e62ac25578270cff1b9f619",  # weth
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.POLYGON]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.POLYGON]]
    ),
    SupportedLedgers.ARBITRUM: set(
        [
            "0x064f8b858c2a603e1b106a2039f5446d32dc81c1",  # olas
            "0x35751007a407ca6feffe80b3cb397736d2cf4dbe",  # weETH
            "0x2f2a2543B76A4166549F7aaB2e75Bef0aefC5B0f",  # WBTC
            "0x77b7787a09818502305C95d68A2571F090abb135",  # DRV
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.ARBITRUM]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.ARBITRUM]]
    ),
    SupportedLedgers.MODE: set(
        [
            "0xcfd1d50ce23c46d3cf6407487b2f8934e96dc8f9",  # mode
        ]
        + LEDGER_TO_STABLECOINS[SupportedLedgers.MODE]
        + [LEDGER_TO_WRAPPER[SupportedLedgers.MODE]]
    ),
    SupportedLedgers.DERIVE: set(LEDGER_TO_STABLECOINS[SupportedLedgers.DERIVE]),
}

TOKEN_LIST_PATH = Path(__file__).parent / "token_list.json"
DEFAULT_ENCODING = "utf-8"


@functools.lru_cache
def read_token_list(chain_id: int):
    """Read the token list."""
    with open(TOKEN_LIST_PATH, encoding=DEFAULT_ENCODING) as file:
        token_list = json.loads(file.read())["tokens"]

    tokens = filter(lambda t: str(t["chainId"]) == str(chain_id), token_list)
    token_map = {t["address"]: t for t in tokens}
    if not token_map:
        msg = f"No tokens found for chain {chain_id}"
        raise ValueError(msg)
    return token_map
