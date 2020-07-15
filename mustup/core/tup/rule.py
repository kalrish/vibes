import logging

logger = logging.getLogger(
    __name__,
)


class Rule:
    def __init__(
                self,
                inputs,
                command,
                outputs,
                caret_flags = [
                ],
                order_only_inputs = [
                ],
                pretty_command = None,
            ):
        self.caret_flags = caret_flags
        self.command = command
        self.inputs = inputs
        self.order_only_inputs = order_only_inputs
        self.outputs = outputs
        self.pretty_command = pretty_command

    def serialize(
                self,
            ):
        inputs = ' '.join(
            self.inputs,
        )

        order_only_inputs = ' '.join(
            self.order_only_inputs,
        )

        command = ' '.join(
            self.command,
        )

        outputs = ' '.join(
            self.outputs,
        )

        if self.caret_flags:
            joined_caret_flags = ''.join(
                self.caret_flags,
            )

            include_caret_part = True
        else:
            joined_caret_flags = None

            include_caret_part = bool(
                self.pretty_command,
            )

        if include_caret_part:
            caret_part = '^'

            if joined_caret_flags:
                caret_part = caret_part + joined_caret_flags

            if self.pretty_command:
                caret_part = caret_part + ' ' + self.pretty_command

            caret_part = caret_part + '^'
        else:
            caret_part = ''

        rule = f': { inputs } | { order_only_inputs } |> { caret_part } { command } |> { outputs }'

        return rule

    def output(
                self,
            ):
        serialization = self.serialize(
        )

        print(
            serialization,
        )
