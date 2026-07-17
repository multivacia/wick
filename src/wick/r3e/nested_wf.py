"""Nested walk-forward splits — strictly temporal, no random splits."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fold:
    train_idx: list[int]
    test_idx: list[int]


@dataclass(frozen=True)
class NestedFold:
    outer: Fold
    inner_folds: list[Fold]


def development_cutoff(n: int, holdout_frac: float = 0.30) -> int:
    """Last holdout_frac excluded (R3D holdout). R3E develops only on [0, cut)."""
    if n <= 0:
        return 0
    cut = int(n * (1.0 - holdout_frac))
    return max(cut, 0)


def expanding_folds(
    n: int,
    *,
    min_train: int = 80,
    test_size: int = 40,
) -> list[Fold]:
    """Strictly temporal expanding folds on indices 0..n-1."""
    folds: list[Fold] = []
    start_test = min_train
    while start_test + test_size <= n:
        train = list(range(0, start_test))
        test = list(range(start_test, start_test + test_size))
        folds.append(Fold(train_idx=train, test_idx=test))
        start_test += test_size
    return folds


def nested_walk_forward(
    n_dev: int,
    *,
    outer_min_train: int = 80,
    outer_test_size: int = 40,
    inner_val_frac: float = 0.25,
) -> list[NestedFold]:
    """Outer expanding WF; inner temporal val for hyperparam/threshold selection."""
    outers = expanding_folds(n_dev, min_train=outer_min_train, test_size=outer_test_size)
    nested: list[NestedFold] = []
    for outer in outers:
        n_tr = len(outer.train_idx)
        if n_tr < 20:
            continue
        cut = int(n_tr * (1.0 - inner_val_frac))
        cut = max(cut, 10)
        if cut >= n_tr:
            continue
        nested.append(
            NestedFold(
                outer=outer,
                inner_folds=[Fold(train_idx=outer.train_idx[:cut], test_idx=outer.train_idx[cut:])],
            )
        )
    return nested


def assert_no_future_in_train(fold: Fold) -> None:
    if not fold.train_idx or not fold.test_idx:
        return
    if max(fold.train_idx) >= min(fold.test_idx):
        raise AssertionError("temporal leakage: train max >= test min")
