import pytest

from evaluator import Evaluator


@pytest.fixture
def ev():
    return Evaluator()