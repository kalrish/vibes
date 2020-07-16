import argparse
import logging

import mustup.core.cli.argparsing.types.logging_level

logger = logging.getLogger(
    __name__,
)


def set_up(
            default_logging_level,
            default_encoder=None,
        ):
    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    arg_encoder_kwargs = {
    }

    if default_encoder:
        arg_encoder_kwargs['default'] = default_encoder

    encoder_arg_required = not bool(
        default_encoder,
    )

    parser.add_argument(
        '-e',
        '--encoder',
        dest='encoder',
        help='encoder module to use',
        metavar='ENCODER',
        required=encoder_arg_required,
        **arg_encoder_kwargs,
    )

    parser.add_argument(
        '-l',
        '--logging-level',
        default=default_logging_level,
        dest='logging_level',
        help='logging level',
        type=mustup.core.cli.argparsing.types.logging_level.parser,
        metavar='LEVEL',
    )

    return parser
