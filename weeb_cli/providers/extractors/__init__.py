"""Stream URL extractors for various hosting services.

This package contains extractors that parse and decrypt stream URLs
from various video hosting services used by anime providers.

Extractors:
    megacloud: Megacloud stream extractor with AES decryption
    doodstream: Doodstream URL extractor
    filemoon: Filemoon stream extractor
    streamtape: Streamtape URL extractor
    vidoza: Vidoza stream extractor
    voe: VOE stream extractor

Each extractor handles the specific URL patterns and decryption methods
required by its respective hosting service.
"""

__all__ = [
    "megacloud",
    "doodstream",
    "filemoon",
    "streamtape",
    "vidoza",
    "voe",
]
