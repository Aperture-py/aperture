from .command import Command


class Hello(Command):
    """
    'hello' command.
    """

    def run(self):
        """Says hello to the user when 'aperture hello' is executed."""
        print("Hello from aperture.")
