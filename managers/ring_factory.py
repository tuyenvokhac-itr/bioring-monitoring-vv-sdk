from managers.ring_manager_impl import _RingManagerImpl
from managers.ring_manager import RingManager


def get_ring_manager_instance() -> RingManager:
    return _RingManagerImpl()