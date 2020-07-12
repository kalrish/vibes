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
            ):
        self.inputs = inputs

        self.command = command

        self.outputs = outputs

    def serialize(
                self,
            ):
        inputs = ' '.join(
            self.inputs,
        )

        command = ' '.join(
            self.command,
        )

        outputs = ' '.join(
            self.outputs,
        )

        rule = f': { inputs } |> { command } |> { outputs }'

        return rule

    def output(
                self,
            ):
        serialization = self.serialize(
        )

        print(
            serialization,
        )
