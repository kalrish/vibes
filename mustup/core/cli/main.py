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
    encoder_name = None

    try:
        vardict_path = os.environ['tup_vardict']
    except KeyError:
        under_tup = False
    else:
        under_tup = True

    if under_tup:
        logging_level = logging.INFO
    else:
        parser = mustup.core.cli.argparsing.set_up(
        )

        args = parser.parse_args(
        )

        logging_level = args.logging_level
        encoder_name = args.encoder

    mustup.core.cli.logging.set_up(
        level=logging_level,
    )

    if under_tup:
        vardict = mustup.tup.vardict.load(
            path=vardict_path,
        )

        try:
            encoder_name = vardict['ENCODER']
        except KeyError:
            logger.error(
                'CONFIG_ENCODER not set',
            )

    if encoder_name:
        return_value = mustup.core.main.process_current_directory(
            encoder_name=encoder_name,
        )

        exit_code = int(
            not return_value,
        )
    else:
        exit_code = 1

    return exit_code
