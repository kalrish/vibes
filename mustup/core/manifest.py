import logging

logger = logging.getLogger(
    __name__,
)


class Manifest:
    def __init__(
                self,
            ):
        self.manifests = [
        ]

    def add_manifest(
                self,
                manifest,
            ):
        self.manifests.append(
            manifest,
        )

    def get(
                self,
                key,
            ):
        iterator = reversed(
            self.manifests,
        )

        for manifest in iterator:
            try:
                value = manifest[key]
            except KeyError:
                pass
            else:
                return value
