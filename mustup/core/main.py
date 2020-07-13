import importlib
import logging
import pathlib
import os
import re

import yaml

import mustup.core.tup.rule

logger = logging.getLogger(
    __name__,
)

tracknumber_regex = re.compile(
    pattern='^(\d+)-.+$',
)


def process_current_directory(
            format_name,
        ):
    return_value = False

    formatter = get_formatter(
        name=format_name,
    )

    if formatter:
        build_instructions = load_build_instructions(
        )

        if build_instructions:
            metadata = load_metadata(
            )

            iterator = build_instructions.items(
            )

            for track_source_name, instructions in iterator:
                track_source_path = pathlib.PurePath(
                    track_source_name,
                )

                extension = track_source_path.suffix

                supported_source_type = extension in formatter.supported_extensions

                if supported_source_type:
                    track_metadata = instructions['metadata']

                    match = tracknumber_regex.search(
                        track_source_name,
                    )

                    if match:
                        track_number = match.group(
                            1,
                        )

                        try:
                            track_metadata_track_number = track_metadata['track number']
                        except KeyError:
                            track_metadata['track number'] = track_number
                        else:
                            inferred_and_specified_are_equal = track_metadata_track_number == track_number

                            if inferred_and_specified_are_equal:
                                logger.info(
                                    '%s: specifying the track number is not necessary when it is part of the track\'s file name',
                                    track_source_name,
                                )
                            else:
                                logger.warning(
                                    '%s: the specified track number differs from the one inferred from the track\'s file name',
                                    track_source_name,
                                )

                    transformations = instructions.get(
                        'transformations',
                        {
                        },
                    )

                    if 'trim' not in formatter.supported_transformations:
                        try:
                            transformation_trim = transformations['trim']
                        except KeyError:
                            pass
                        else:
                            processed_track_source_name = f'{track_source_path.stem}-processed.wave'
                            rule = mustup.core.tup.rule.Rule(
                                inputs=[
                                    track_source_name,
                                ],
                                command=[
                                    'ffmpeg',
                                    '-i',
                                    track_source_name,
                                    '-ss',
                                    '00:00:20',
                                    '-to',
                                    '00:00:40',
                                    '-f',
                                    'wav',
                                    '-c',
                                    'copy',
                                    processed_track_source_name,
                                ],
                                outputs=[
                                    processed_track_source_name,
                                ],
                            )

                            rule.output(
                            )

                    merge(
                        destination=track_metadata,
                        source=metadata,
                    )

                    logger.debug(
                        '%s: metadata: %s',
                        track_source_name,
                        track_metadata,
                    )

                    rule = formatter.process(
                        metadata=track_metadata,
                        source_basename=track_source_path.stem,
                        source_name=track_source_name,
                        transformations=transformations,
                    )

                    rule.output(
                    )

                    return_value = True
                else:
                    logger.error(
                        '%s: not supported by format %s',
                        track_source_name,
                        format_name,
                    )

                    return_value = False
        else:
            return_value = True

    return return_value


def get_formatter(
            name,
        ):
    try:
        format_module = importlib.import_module(
            name=f'.{name}',
            package='mustup.formats',
        )
    except ModuleNotFoundError:
        logger.error(
            'could not find module for format %s',
            name,
        )

        return_value = None
    else:
        formatter_class = getattr(
            format_module,
            'Format',
        )

        formatter = formatter_class(
        )

        return_value = formatter

    return return_value


def load_build_instructions(
        ):
    try:
        f = open(
            'mustup-manifest.yaml',
            'r',
        )
    except FileNotFoundError:
        logger.debug(
            'no build manifest found',
        )

        return_value = None
    else:
        logger.debug(
            'build manifest found',
        )

        build_instructions = yaml.safe_load(
            f,
        )

        return_value = build_instructions

    return return_value


def load_metadata(
        ):
    metadata = {
    }

    should_continue = True

    path = pathlib.Path.cwd(
    )

    level = 0

    while should_continue:
        tup_directory_path = path.joinpath(
            '.tup',
        )

        top_reached = tup_directory_path.exists(
        )

        if top_reached:
            logger.debug(
                'top reached at %s',
                path.as_posix(
                ),
            )

        should_continue = not top_reached

        manifest = load_metadata_manifest(
            path,
        )

        if manifest:
            try:
                pictures = manifest['pictures']['APIC']
            except KeyError:
                pass
            else:
                iterator = pictures.values(
                )

                for picture_details in iterator:
                    picture_path = picture_details['path']
                    up_levels = os.path.relpath(
                        path,
                    )
                    picture_path = up_levels + '/' + picture_path
                    picture_details['path'] = picture_path

            merge(
                destination=metadata,
                source=manifest,
            )

        path = path.parent

        level = level + 1

    logger.debug(
        'metadata: %s',
        metadata,
    )

    return metadata


def load_metadata_manifest(
            path,
        ):
    complete_path = path.joinpath(
        'mustup-metadata.yaml',
    )

    try:
        f = complete_path.open(
            mode='r',
        )
    except FileNotFoundError:
        logger.debug(
            '%s: no metadata manifest found',
            path.as_posix(
            ),
        )

        return_value = None
    else:
        complete_path_representation = complete_path.as_posix(
        )

        logger.debug(
            '%s: metadata manifest found',
            complete_path_representation,
        )

        metadata = yaml.safe_load(
            f,
        )

        logger.debug(
            '%s: metadata: %s',
            complete_path_representation,
            metadata,
        )

        return_value = metadata

    return return_value


def merge(
            destination,
            source,
        ):
    iterator = source.items(
    )

    for key, source_value in iterator:
        try:
            destination_value = destination[key]
        except KeyError:
            destination[key] = source_value
        else:
            source_value_is_dict = isinstance(
                source_value,
                dict,
            )

            if source_value_is_dict:
                destination_value_is_dict = isinstance(
                    destination_value,
                    dict,
                )

                assert destination_value_is_dict

                merge(
                    destination=destination_value,
                    source=source_value,
                )
