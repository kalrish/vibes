import logging
import os

import mustup.core.cli.argparsing
import mustup.core.cli.logging
import mustup.core.main
import mustup.tup.vardict

logger = logging.getLogger(
    __name__,
)


def entry_point(
        ):
    default_arguments = {
    }

    try:
        vardict = mustup.tup.vardict.load(
        )
    except mustup.tup.errors.NotUnderTup:
        default_logging_level = logging.DEBUG
    else:
        default_logging_level = logging.INFO

        try:
            encoder_name = vardict['ENCODER']
        except KeyError:
            logger.warning(
                'CONFIG_ENCODER not set; --encoder may be specified, but the @-variable would be better',
            )
        else:
            default_arguments['default_encoder'] = encoder_name

    parser = mustup.core.cli.argparsing.set_up(
        default_logging_level=default_logging_level,
        **default_arguments,
    )

    args = parser.parse_args(
    )

    logging_level = args.logging_level
    encoder_name = args.encoder

    mustup.core.cli.logging.set_up(
        level=logging_level,
    )

    logger.debug(
        'encoder name: "%s"',
        encoder_name,
    )

    return_value = mustup.core.main.process_current_directory(
        encoder_name=encoder_name,
    )

    exit_code = int(
        not return_value,
    )

    return exit_code
