# Auto-generated by tool

"""Test dialogues module for the spot_asset protocol."""

from unittest.mock import MagicMock

from pydantic import BaseModel
from hypothesis import HealthCheck, given, settings, strategies as st
from aea.configurations.data_types import PublicId

from packages.eightballer.protocols.spot_asset.message import SpotAssetMessage
from packages.eightballer.protocols.spot_asset.dialogues import (
    SpotAssetDialogues,
)
from packages.eightballer.protocols.spot_asset.tests.performatives import (
    GetSpotAsset,
    GetSpotAssets,
)


def shallow_dump(model: BaseModel) -> dict:
    """Shallow dump pydantic model."""

    return {name: getattr(model, name) for name in model.__class__.model_fields}


def validate_dialogue(performative, model):
    """Validate successful dialogue instantiation."""

    skill_context = MagicMock()
    skill_context.skill_id = PublicId(
        name="mock_name",
        author="mock_author",
    )

    dialogues = SpotAssetDialogues(
        name="test_spot_asset_dialogues",
        skill_context=skill_context,
    )

    dialogue = dialogues.create(
        counterparty="dummy_counterparty",
        performative=performative,
        **shallow_dump(model),
    )

    assert dialogue is not None


@settings(deadline=1000, suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(GetSpotAsset))
def test_get_spot_asset_dialogues(model):
    """Test for the 'GET_SPOT_ASSET' protocol."""
    validate_dialogue(SpotAssetMessage.Performative.GET_SPOT_ASSET, model)


@settings(deadline=1000, suppress_health_check=[HealthCheck.too_slow])
@given(st.from_type(GetSpotAssets))
def test_get_spot_assets_dialogues(model):
    """Test for the 'GET_SPOT_ASSETS' protocol."""
    validate_dialogue(SpotAssetMessage.Performative.GET_SPOT_ASSETS, model)
