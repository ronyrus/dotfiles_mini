"""
Very minimal CLI library wrapper
"""

import argparse
import os
import sys

class Argument(object):
    def __init__(self, *args, **kwargs):
        self._args = args, kwargs
        self._dest = self._name = None

    def bind(self, parser):
        args, kwargs = self._args
        self._dest = getattr(parser.add_argument(*args, **kwargs), 'dest', None)

    def __call__(self, parser):
        self.bind(parser)
        return parser

    def __get__(self, instance, owner):
        if instance is None:
            return self
        return getattr(instance.__args__, self._dest, None)

class Command(object):
    def __init__(self, func):
        self._instance = None
        self._func = func
        self._name = func.__name__
        self._args = []
        self._dest = []

    def add_argument(self, *args, **kwargs):
        self._args.append((args, kwargs))

    def bind(self, group, instance=None):
        doc = (self._func.__doc__ or '')
        help = doc.splitlines()[0]
        parser = group.add_parser(self._name, help=help, description = doc)
        for args, kwargs in self._args:
            self._dest.append(parser.add_argument(*args, **kwargs).dest)
        parser.set_defaults(_subcommand=self)
        self._instance = instance

    def __call__(self, args):
        self._func(self._instance, **{d: getattr(args, d, None) for d in self._dest})

class CommandLineApp(object):
    """ Class for creating simple command-line applications.
    Subclass me and call via run().

    Example:

        class MyApp(CommandLineApp):
            test = Argument("-t", "--test", help="a test argument")

            @Command
            def foo(self):
                " do foo "
                print 'foo!'

            @Argument("files", help="Positional argument")
            @Argument("--verbose", action="count", help="be more verbose")
            @Command
            def bla(self, files, verbose):
                " Do stuff..."

        MyApp.run()

    """
    @classmethod
    def run(cls, args=None):
        commands = []
        arguments = {}
        for k, v in vars(cls).items():
            if isinstance(v, Command):
                commands.append(v)
            elif isinstance(v, Argument):
                arguments[k] = v
        name = getattr(cls, 'APPNAME', os.path.basename(sys.modules[cls.__module__].__file__))
        ap = argparse.ArgumentParser(name, description=cls.__doc__ or '')
        for k, v in arguments.items():
            v.bind(ap)

        ins = cls.__new__(cls)

        if commands:
            sub = ap.add_subparsers(help="The subcommand to execute, one of:", metavar="subcommand")
            for cmd in commands:
                cmd.bind(sub, ins)

        args = ap.parse_args(args)
        ins.__args__ = args

        if getattr(args, '_subcommand', None) is not None:
            try:
                ins.__init__()
                sys.exit(args._subcommand(args))
            except Exception as e:
                sys.exit("Error: %s" % e)

