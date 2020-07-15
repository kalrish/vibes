import abc
import logging

logger = logging.getLogger(
    __name__,
)


class Encoder(
            metaclass=abc.ABCMeta,
        ):
    def process_directory(
                self,
                metadata,
            ):
        pass

    @abc.abstractmethod
    def process_track(
                self,
                metadata,
                source_basename,
                source_name,
                transformations,
            ):
        pass
