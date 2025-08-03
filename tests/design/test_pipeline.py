from aguaclara.design.pipeline import *
from aguaclara.core.units import unit_registry as u
import pytest

pipe_20 = Pipe(q=20.0 * u.L / u.s, size=6 * u.inch)
pipe_60 = Pipe(q=60.0 * u.L / u.s, size=6 * u.inch)

elbow_20 = Elbow(q=20.0 * u.L / u.s, size=6 * u.inch)
elbow_60 = Elbow(q=60.0 * u.L / u.s, size=6 * u.inch)

tee_20 = Tee(q=20.0 * u.L / u.s, size=6 * u.inch)
tee_60 = Tee(q=60.0 * u.L / u.s, size=6 * u.inch)

pipeline_20 = Pipe(
    q=20.0 * u.L / u.s,
    size=6 * u.inch,
    next=Elbow(
        size=6 * u.inch,
        next=Pipe(size=6 * u.inch, l=4 * u.m, next=Tee(size=6 * u.inch)),
    ),
)

pipeline_60 = Pipe(
    q=60.0 * u.L / u.s,
    size=6 * u.inch,
    next=Elbow(
        size=6 * u.inch,
        next=Pipe(size=6 * u.inch, l=4 * u.m, next=Tee(size=6 * u.inch)),
    ),
)

pipeline_fp = Pipe(
    size=6 * u.inch,
    next=Elbow(
        size=6 * u.inch,
        next=Pipe(size=6 * u.inch, l=4 * u.m, next=Tee(size=6 * u.inch)),
    ),
)


@pytest.mark.parametrize(
    "actual, expected",
    [
        (pipe_20.headloss, 1.0678779116069842 * u.cm),
        (pipe_60.headloss, 9.078557133328923 * u.cm),
        (elbow_20.headloss, 3.6621361403683412 * u.cm),
        (elbow_60.headloss, 32.95922526331507 * u.cm),
        (tee_20.headloss, 7.3242722807366825 * u.cm),
        (tee_60.headloss, 65.91845052663014 * u.cm),
        (pipeline_20.headloss, 1.0678779116069842 * u.cm),
        (pipeline_60.headloss, 9.078557133328923 * u.cm),
        (pipeline_fp.flow_pipeline(20 * u.cm), 22.162471566281223 * u.L / u.s),
        (pipeline_fp.flow_pipeline(40 * u.cm), 31.45057786475188 * u.L / u.s),
    ],
)
def test_pipeline(actual, expected):
    if type(actual) == u.Quantity and type(expected) == u.Quantity:
        assert actual.units == expected.units
        assert actual.magnitude == pytest.approx(expected.magnitude)
    else:
        assert actual == pytest.approx(expected)
