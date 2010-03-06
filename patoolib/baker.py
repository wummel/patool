#===============================================================================
# Copyright 2010 Matt Chaput
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#===============================================================================

import re, sys
from inspect import getargspec
from textwrap import wrap


def normalize_docstring(docstring):
    """Normalizes whitespace in the given string.
    """
    return re.sub(r"[\r\n\t ]+", " ", docstring).strip()


param_exp = re.compile(r"^([\t ]*):param (.*?): ([^\n]*\n(\1[ \t]+[^\n]*\n)*)",
                       re.MULTILINE)

def find_param_docs(docstring):
    """Finds ReStructuredText-style ":param:" lines in the docstring and
    returns a dictionary mapping param names to doc strings.
    """

    paramdocs = {}
    for match in param_exp.finditer(docstring):
        name = match.group(2)
        value = match.group(3)
        paramdocs[name] = value
    return paramdocs

def remove_param_docs(docstring):
    """Finds ReStructuredText-style ":param:" lines in the docstring and
    returns a new string with the param documentation removed.
    """
    return param_exp.sub("", docstring)


def process_docstring(docstring):
    """Takes a docstring and returns a list of strings representing
    the paragraphs in the docstring.
    """

    lines = docstring.split("\n")
    paras = [[]]
    for line in lines:
        if not line.strip():
            paras.append([])
        else:
            paras[-1].append(line)
    paras = [normalize_docstring(" ".join(ls))
             for ls in paras if ls]
    return paras


def format_paras(paras, width, indent=0):
    """Takes a list of paragraph strings and formats them into a word-wrapped,
    optionally indented string.
    """

    output = []
    for para in paras:
        lines = wrap(para, width-indent)
        if lines:
            for line in lines:
                output.append((" " * indent) + line)
            output.append("")
    return "\n".join(output)


def totype(v, default):
    """Tries to convert the value 'v' into the same type as 'default'.
    """

    t = type(default)
    if t is int:
        return int(v)
    elif t is float:
        return float(v)
    elif t is long:
        return long(v)
    elif t is bool:
        lv = v.lower()
        if lv in ("true", "yes", "on", "1"):
            return True
        elif lv in ("false", "no", "off", "0"):
            return False
        else:
            raise TypeError
    else:
        return v


class CommandError(Exception): pass


class Cmd(object):
    """Stores metadata about a command.
    """

    def __init__(self, name, fn, argnames, keywords, shortopts,
                 has_varargs, has_kwargs, docstring, paramdocs):
        self.name = name
        self.fn = fn
        self.argnames = argnames
        self.keywords = keywords
        self.shortopts = shortopts
        self.has_varargs = has_varargs
        self.has_kwargs = has_kwargs
        self.docstring = docstring
        self.paramdocs = paramdocs


class Baker(object):
    def __init__(self):
        self.commands = {}
        self.defaultcommand = None

    def command(self, fn=None, name=None, default=False,
                params=None, shortopts=None):
        """Registers a command with the bakery. This does not call the
        function, it simply adds it to the list of functions this Baker
        knows about.

        This method is usually used as a decorator::

            b = Baker()

            @b.command
            def test():
                pass

        :param fn: the function to register.
        :param name: use this argument to register the command under a
            different name than the function name.
        :param default: if True, this command is used when a command is not
            specified on the command line.
        :param params: a dictionary mapping parameter names to docstrings. If
            you don't specify this argument, parameter annotations will be used
            (Python 3.x only), or the functions docstring will be searched for
            Sphinx-style ':param' blocks.
        :param shortopts: a dictionary mapping parameter names to short
            options, e.g. {"verbose": "v"}.
        """

        # This method works as a decorator with or without arguments.
        if fn is None:
            # The decorator was given arguments, e.g. @command(default=True),
            # so we have to return a function that will wrap the function when
            # the decorator is applied.
            return lambda fn: self.command(fn, default=default,
                                           params=params,
                                           shortopts=shortopts)
        name = name or fn.__name__

        # Inspect the argument signature of the function
        arglist, vargsname, kwargsname, defaults = getargspec(fn)
        has_varargs = bool(vargsname)
        has_kwargs = bool(kwargsname)

        # Get the function's docstring
        docstring = fn.__doc__ or ""

        # If the user didn't specify parameter help in the decorator
        # arguments, try to get it from parameter annotations (Python 3.x)
        # or RST-style :param: lines in the docstring
        if params is None:
            if hasattr(fn, "func_annotations") and fn.func_annotations:
                params = fn.func_annotations
            else:
                params = find_param_docs(docstring)
                docstring = remove_param_docs(docstring)

        # If the user didn't specify
        shortopts = shortopts or {}

        if defaults:
            # Zip up the keyword argument names with their defaults
            keywords = dict(zip(arglist[0-len(defaults):], defaults))
        elif has_kwargs:
            # allow keyword arguments specified by params
            keywords = dict(zip(params.keys(), [""]*len(params)))
        else:
            keywords = {}

        # If this is a method, remove 'self' from the argument list
        if arglist and arglist[0] == "self":
            arglist.pop(0)

        # Create a Cmd object to represent this command and store it
        cmd = Cmd(name, fn, arglist, keywords, shortopts,
                  has_varargs, has_kwargs,
                  docstring, params)
        self.commands[cmd.name] = cmd

        # If default is True, set this as the default command
        if default: self.defaultcommand = cmd

        return fn

    def print_top_help(self, scriptname, file=sys.stdout):
        """Prints the documentation for the script and exits.

        :param scriptname: the name of the script being executed (argv[0]).
        :param file: the file to write the help to. The default is stdout.
        """

        # Get a sorted list of all command names
        cmdnames = sorted(self.commands.keys())

        # Calculate the indent for the doc strings by taking the longest
        # command name and adding 3 (one space before the name and two after)
        rindent = max(len(name) for name in cmdnames) + 3

        # Print the basic help for running a command
        file.write("\nUsage: %s COMMAND <options>\n\n" % scriptname)

        print("Available commands:\n\n")
        for cmdname in cmdnames:
            # Get the Cmd object for this command
            cmd = self.commands[cmdname]

            # Calculate the padding necessary to fill from the end of the
            # command name to the documentation margin
            tab = " " * (rindent - (len(cmdname)+1))
            file.write(" " + cmdname + tab)

            # Get the paragraphs of the command's docstring
            paras = process_docstring(cmd.docstring)
            if paras:
                # Print the first paragraph
                file.write(format_paras([paras[0]], 76, indent=rindent).lstrip())

        file.write("\n")
        file.write('Use "%s <command> --help" for individual command help.\n' % scriptname)
        sys.exit(0)

    def print_command_help(self, scriptname, cmd, file=sys.stdout):
        """Prints the documentation for a specific command and exits.

        :param scriptname: the name of the script being executed (argv[0]).
        :param cmd: the Cmd object representing the command.
        :param file: the file to write the help to. The default is stdout.
        """

        # Print the usage for the command
        file.write("\nUsage: %s %s" % (scriptname, cmd.name))

        # Print the required and "optional" arguments (where optional
        # arguments are keyword arguments with default None).
        for name in cmd.argnames:
            if name not in cmd.keywords:
                # This is a positional argument
                file.write(" <%s>" % name)
            else:
                # This is a keyword argument, so skip it unless the default is
                # None, in which case treat it like an optional argument.
                if cmd.keywords[name] is None:
                    file.write(" [<%s>]" % name)

        if cmd.has_varargs:
            # This command accepts a variable number of positional arguments
            file.write(" [...]")
        file.write("\n\n")

        # Print the documentation for this command
        paras = process_docstring(cmd.docstring)
        if paras:
            # Print the first paragraph with no indent (usually just a summary
            # line)
            file.write(format_paras([paras[0]], 76))

            # Print subsequent paragraphs indented by 4 spaces
            if len(paras) > 1:
                file.write("\n")
                file.write(format_paras(paras[1:], 76, indent=4))
            file.write("\n")

        # Get a sorted list of keyword argument names
        keynames = sorted([key for key, value in cmd.keywords.items() if value is not None])
        # Print documentation for keyword options
        if keynames:
            file.write("Options:\n\n")

            # Make formatted headings, e.g. " -k --keyword  ", and put them in
            # a list like [(name, heading), ...]
            heads = []
            for keyname in keynames:
                if cmd.keywords[keyname] is None: continue

                head = " --" + keyname
                if keyname in cmd.shortopts:
                    head = " -" + cmd.shortopts[keyname] + head
                head += "  "
                heads.append((keyname, head))

            if heads:
                # Find the length of the longest formatted heading
                rindent = max(len(head) for keyname, head in heads)
                # Pad the headings so they're all as long as the longest one
                heads = [(keyname, head + (" " * (rindent - len(head))))
                         for keyname, head in heads]

                # Print the option docs
                for keyname, head in heads:
                    # Print the heading
                    file.write(head)

                    # If this parameter has documentation, print it after the
                    # heading
                    if keyname in cmd.paramdocs:
                        paras = process_docstring(cmd.paramdocs.get(keyname, ""))
                        file.write(format_paras(paras, 76, indent=rindent).lstrip())
                    else:
                        file.write("\n")
            file.write("\n")

            if any((cmd.keywords.get(a) is None) for a in cmd.argnames):
                file.write("(specifying a single hyphen (-) in the argument list means all\n")
                file.write("subsequent arguments are treated as bare arguments, not options)\n")
                file.write("\n")

        sys.exit(0)

    def parse_args(self, scriptname, cmd, argv):
        keywords = cmd.keywords
        shortopts = cmd.shortopts

        # shortopts maps long option names to characters. To look up short
        # options, we need to create a reverse mapping.
        shortchars = dict((v, k) for k, v in shortopts.iteritems())

        # The *vargs list and **kwargs dict to build up from the command line
        # arguments
        vargs = []
        kwargs = {}

        while argv:
            # Take the next argument
            arg = argv.pop(0)

            if arg == "-":
                # All arguments following a single hyphen are treated as
                # positional arguments
                vargs.extend(argv)
                break

            elif arg == "--":
                # What to do with a bare --? Right now, it's ignored.
                continue

            elif arg.startswith("--"):
                # Process long option

                value = None
                if "=" in arg:
                    # The argument was specified like --keyword=value
                    name, value = arg[2:].split("=", 1)
                    default = keywords.get(name)
                    try:
                        value = totype(value, default)
                    except TypeError:
                        pass
                else:
                    # The argument was not specified with an equals sign...
                    name = arg[2:]
                    default = keywords.get(name)

                    if type(default) is bool:
                        # If this option is a boolean, it doesn't need a value;
                        # specifying it on the command line means "do the
                        # opposite of the default".
                        value = not default
                    else:
                        # The next item in the argument list is the value, i.e.
                        # --keyword value
                        if not argv or argv[0].startswith("-"):
                            # Oops, there isn't a value available... just use
                            # True, assuming this is a flag.
                            value = True
                        else:
                            value = argv.pop(0)

                        try:
                            value = totype(value, default)
                        except TypeError:
                            pass

                # Store this option
                kwargs[name] = value

            elif arg.startswith("-") and cmd.shortopts:
                # Process short option(s)

                # For each character after the '-'...
                for i in xrange(1, len(arg)):
                    char = arg[i]
                    if char not in shortchars:
                        continue

                    # Get the long option name corresponding to this char
                    name = shortchars[char]

                    default = keywords[name]
                    if type(default) is bool:
                        # If this option is a boolean, it doesn't need a value;
                        # specifying it on the command line means "do the
                        # opposite of the default".
                        kwargs[name] = not default
                    else:
                        # This option requires a value...
                        if i == len(arg)-1:
                            # This is the last character in the list, so the
                            # next argument on the command line is the value.
                            value = argv.pop(0)
                        else:
                            # There are other characters after this one, so
                            # the rest of the characters must represent the
                            # value (i.e. old-style UNIX option like -Nname)
                            value = totype(arg[i+1:], default)

                        try:
                            kwargs[name] = totype(value, default)
                        except ValueError:
                            raise CommandError("Couldn't convert %s value %r to type %s" % (name, value, type(default)))
                        break
            else:
                # This doesn't start with "-", so just add it to the list of
                # positional arguments.
                vargs.append(arg)

        return vargs, kwargs

    def parse(self, argv=None):
        """Parses the command and parameters to call from the list of command
        line arguments. Returns a tuple of (Cmd object, position arg list,
        keyword arg dict).

        :param argv: the list of options passed to the command line (sys.argv).
        """

        if argv is None: argv = sys.argv

        scriptname = argv[0]

        if (len(argv) < 2) or (argv[1] == "-h" or argv[1] == "--help"):
            # Print the documentation for the script
            self.print_top_help(scriptname)

        if argv[1] == "help":
            if len(argv) > 2 and argv[2] in self.commands:
                cmd = self.commands[argv[2]]
                self.print_command_help(scriptname, cmd)
            self.print_top_help(scriptname)

        if len(argv) > 1 and argv[1] in self.commands:
            # The first argument on the command line (after the script name
            # is the command to run.
            cmd = self.commands[argv[1]]

            if len(argv) > 2 and (argv[2] == "-h" or argv[2] == "--help"):
                # Print the help for this command and exit
                self.print_command_help(scriptname, cmd)

            options = argv[2:]
        else:
            # No known command was specified. If there's a default command,
            # use that.
            cmd = self.defaultcommand
            if cmd is None:
                raise CommandError("unknown command `%s' specified" % argv[1])

            options = argv[1:]

        # Parse the rest of the arguments on the command line and use them to
        # call the command function.
        args, kwargs = self.parse_args(scriptname, cmd, options)
        return (cmd, args, kwargs)

    def apply(self, cmd, args, kwargs):
        """Calls the command function.
        """

        # Create a list of positional arguments: arguments that are either
        # required (not in keywords), or where the default is None (taken to be
        # an optional positional argument). This is different from the Python
        # calling convention, which will fill in keyword arguments with extra
        # positional arguments.
        posargs = [a for a in cmd.argnames if cmd.keywords.get(a) is None]

        if len(args) > len(posargs) and not cmd.has_varargs:
            raise CommandError("Too many arguments to %s: %s" % (cmd.name, " ".join(args)))

        if not cmd.has_kwargs:
            for k in sorted(kwargs.iterkeys()):
                if k not in cmd.keywords:
                    raise CommandError("Unknown option --%s" % k)

        # Rearrange the arguments into the order Python expects
        newargs = []
        newkwargs = dict(kwargs)
        for name in cmd.argnames:
            if args and cmd.keywords.get(name) is None:
                # This argument is required or optional and we have a bare arg
                # to fill it
                newargs.append(args.pop(0))
            elif name not in cmd.keywords and not args:
                # This argument is required but we don't have a bare arg to
                # fill it
                raise CommandError("Required argument '%s' not given" % name)
            else:
                # This is a keyword argument
                newkwargs[name] = kwargs.get(name, cmd.keywords[name])
        newargs.extend(args)

        return cmd.fn(*newargs, **newkwargs)

    def run(self, argv=None):
        """Takes a list of command line arguments, parses it into a command
        name and options, and calls the function corresponding to the command
        with the given arguments.

        :param argv: the list of options passed to the command line (sys.argv).
        """

        return self.apply(*self.parse(argv))

    def test(self, argv=None):
        """Takes a list of command line arguments, parses it into a command
        name and options, and prints what the resulting function call would
        look like. This may be useful for testing how command line arguments
        would be passed to your functions.

        :param argv: the list of options passed to the command line (sys.argv).
        """

        cmd, args, kwargs = self.parse(argv)
        result = "%s(%s" % (cmd.name, ",".join(repr(a) for a in args))
        if kwargs:
            kws = ", ".join("%s=%r" % (k, v) for k, v in kwargs.iteritems())
            result += ", " + kws
        result += ")"
        print result


_baker = Baker()
command = _baker.command
run = _baker.run
test = _baker.test
