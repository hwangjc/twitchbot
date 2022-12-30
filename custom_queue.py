from collections import deque
from typing import Any, List, Optional

from twitchio.ext import commands

from errors import QueueItemDNEError, QueueItemNotUniqueError


class QueueItem:
    def __init__(self, id: str, data: Any):
        self.id = id
        self.data = data


class Queue:
    def __init__(self, is_unique: bool):
        # Whether or not the queue is open
        self.is_open = False 
        # Whether or not the queue can only contain unique items
        self.is_unique = is_unique 

        self.queue = deque()

    def open(self) -> None:
        self.is_open = True

    def close(self) -> None:
        self.is_open = False

    def clear(self) -> None:
        self.queue = deque()

    def next(self) -> Optional[QueueItem]:
        try:
            return self.queue.popleft()
        except IndexError as e:
            return None

    def join(self, queue_item: QueueItem) -> None:
        if self.is_unique:
            for item in self.queue:
                if item.id == queue_item.id:
                    raise QueueItemNotUniqueError(
                        f"Queue item \'{item.id}\' already exists"
                    )
        self.queue.append(queue_item)

    def leave(self, queue_item_id: str) -> None:
        # Find items to remove
        to_remove = []
        for item in self.queue:
            if item.id == queue_item_id:
                to_remove.append(item)
        # Raise exception if no items to remove
        if len(to_remove) == 0:
            raise QueueItemDNEError(
                f"Queue item with id \'{queue_item_id}\' does not exist."
            )
        # Remove all instances of the to_remove items.
        # Here we use a "while true" loop to remove items from the queue because
        # deque.remove() only removes the first instance of an item. In the case of
        # non-unique queues, it's possible for the queue to contain multiple
        # instances of the same item.
        for item in to_remove:
            while True:
                try:
                    self.queue.remove(item)
                except ValueError as e:
                    break

    def list(self) -> List[QueueItem]:
        return [item for item in self.queue]

