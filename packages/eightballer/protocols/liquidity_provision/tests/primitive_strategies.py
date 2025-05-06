"""Module containing hypothesis strategies for the custom primitives."""

from hypothesis import strategies as st

from packages.eightballer.protocols.liquidity_provision.primitives import (
    Float,
    Int32,
    Int64,
    Double,
    SInt32,
    SInt64,
    UInt32,
    UInt64,
    Fixed32,
    Fixed64,
    SFixed32,
    SFixed64,
)


st.register_type_strategy(
    Double, st.floats(min_value=Double.min(), max_value=Double.max(), allow_nan=False, allow_infinity=False).map(Double)
)
st.register_type_strategy(
    Float, st.floats(min_value=Float.min(), max_value=Float.max(), allow_nan=False, allow_infinity=False).map(Float)
)

st.register_type_strategy(Int32, st.integers(min_value=Int32.min(), max_value=Int32.max()).map(Int32))

st.register_type_strategy(Int64, st.integers(min_value=Int64.min(), max_value=Int64.max()).map(Int64))

st.register_type_strategy(UInt32, st.integers(min_value=UInt32.min(), max_value=UInt32.max()).map(UInt32))

st.register_type_strategy(UInt64, st.integers(min_value=UInt64.min(), max_value=UInt64.max()).map(UInt64))

st.register_type_strategy(SInt32, st.integers(min_value=SInt32.min(), max_value=SInt32.max()).map(SInt32))

st.register_type_strategy(SInt64, st.integers(min_value=SInt64.min(), max_value=SInt64.max()).map(SInt64))

st.register_type_strategy(Fixed32, st.integers(min_value=Fixed32.min(), max_value=Fixed32.max()).map(Fixed32))

st.register_type_strategy(Fixed64, st.integers(min_value=Fixed64.min(), max_value=Fixed64.max()).map(Fixed64))

st.register_type_strategy(SFixed32, st.integers(min_value=SFixed32.min(), max_value=SFixed32.max()).map(SFixed32))

st.register_type_strategy(SFixed64, st.integers(min_value=SFixed64.min(), max_value=SFixed64.max()).map(SFixed64))
