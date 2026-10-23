from app.volumes.cache import ResultCache


def test_cache_computes_once_per_key():
    cache: ResultCache[int] = ResultCache(max_items=2)
    calls: list[int] = []

    def compute() -> int:
        calls.append(1)
        return 42

    assert cache.get_or_compute(1, compute) == 42
    assert cache.get_or_compute(1, compute) == 42
    assert len(calls) == 1


def test_cache_evicts_least_recently_used():
    cache: ResultCache[int] = ResultCache(max_items=2)
    cache.get_or_compute(1, lambda: 1)
    cache.get_or_compute(2, lambda: 2)
    cache.get_or_compute(1, lambda: 1)
    cache.get_or_compute(3, lambda: 3)

    assert len(cache) == 2
    assert cache.get_or_compute(2, lambda: -2) == -2


def test_invalidate_forces_recompute():
    cache: ResultCache[int] = ResultCache(max_items=2)
    cache.get_or_compute(1, lambda: 1)

    cache.invalidate(1)

    assert cache.get_or_compute(1, lambda: 10) == 10
