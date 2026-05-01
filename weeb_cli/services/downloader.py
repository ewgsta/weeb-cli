"""Download service (backward compatibility wrapper).

This module maintains backward compatibility by re-exporting
the refactored download components from the new package structure.
"""

from weeb_cli.services.download.queue import QueueManager, queue_manager

__all__ = ['QueueManager', 'queue_manager']
