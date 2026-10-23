from collections import OrderedDict
from collections.abc import Callable
from threading import Lock

from app.core.config import get_settings


class ResultCache[T]:
    """Cache LRU en memoria de resultados de cálculo por función.

    La clave es el id de la función: al editarla se incrementa ``version`` y la entrada
    se renueva en el siguiente cálculo.
    """

    def __init__(self, max_items: int) -> None:
        self._items: OrderedDict[int, T] = OrderedDict()
        self._max_items = max_items
        self._lock = Lock()

    def get_or_compute(self, function_id: int, compute: Callable[[], T]) -> T:
        with self._lock:
            if function_id in self._items:
                self._items.move_to_end(function_id)
                return self._items[function_id]

        value = compute()
        with self._lock:
            self._items[function_id] = value
            self._items.move_to_end(function_id)
            while len(self._items) > self._max_items:
                self._items.popitem(last=False)
        return value

    def invalidate(self, function_id: int) -> None:
        with self._lock:
            self._items.pop(function_id, None)

    def clear(self) -> None:
        with self._lock:
            self._items.clear()

    def __len__(self) -> int:
        return len(self._items)


mesh_cache: ResultCache[bytes] = ResultCache(get_settings().cache_max_items)
volume_cache: ResultCache[object] = ResultCache(get_settings().cache_max_items)
