import argparse
import logging

import mustup.core.cli.argparsing.types.logging_level

logger = logging.getLogger(
    __name__,
)


def set_up(
        ):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        '-l',
        '--logging-level',
        default='warning',
        dest='logging_level',
        help='logging level',
        type=mustup.core.cli.argparsing.types.logging_level.parser,
        metavar='LEVEL',
    )

    parser.add_argument(
        '-f',
        '--format',
        dest='format',
        help='format',
        metavar='FORMAT',
        required=True,
    )

    return parser
