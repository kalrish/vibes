import ctypes
import logging
import sys

logger = logging.getLogger(
    __name__,
)


def load(
            path,
        ):
    config_variables = {
    }

    try:
        f = open(
            path,
            'rb',
        )
    except FileNotFoundError:
        pass
    else:
        c_unsigned_int_size = ctypes.sizeof(
            ctypes.c_uint,
        )

        count_bytes = f.read(
            c_unsigned_int_size,
        )

        count = int.from_bytes(
            byteorder=sys.byteorder,
            bytes=count_bytes,
            signed=False,
        )

        logger.debug(
            'amount of @-variables: %i',
            count,
        )

        index_size = count * c_unsigned_int_size

        f.seek(
            index_size,
            1,
        )

        rest = f.read(
        )

        logger.debug(
            '@-variables section: %s',
            rest,
        )

        lines = rest.split(
            sep=b'\0',
        )

        for line_bytes in lines:
            # split() returns empty parts
            if line_bytes:
                line = line_bytes.decode(
                    'ascii',
                )

                logger.debug(
                    'line: %s',
                    line,
                )

                parts = line.split(
                    maxsplit=1,
                    sep='=',
                )

                variable = parts[0]

                logger.debug(
                    'variable: %s',
                    variable,
                )

                value = parts[1]

                logger.debug(
                    'value: %s',
                    value,
                )

                config_variables[variable] = value

    return config_variables
