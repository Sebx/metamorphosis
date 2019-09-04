import click
from functools import update_wrapper


@click.group(chain=True)
def cli():
    """This script manages mm operation. One commands feeds into the next.

    Example:

    \b
        mm push -code mycode1.py -code mycode2.py push start
        mm open start publish ""
    """


@cli.resultcallback()
def process_commands(processors):
    """This result callback is invoked with an iterable of all the chained
    subcommands.  As in this example each subcommand returns a function
    we can chain them together to feed one into the other, similar to how
    a pipe on unix works.
    """
    # Start with an empty iterable.
    stream = ()

    # Pipe it through all stream processors.
    for processor in processors:
        stream = processor(stream)

    # Evaluate the stream and throw away the items.
    for _ in stream:
        pass


def processor(f):
    """Helper decorator to rewrite a function so that it returns another
    function from it.
    """
    def new_func(*args, **kwargs):
        def processor(stream):
            return f(stream, *args, **kwargs)
        return processor
    return update_wrapper(new_func, f)


def generator(f):
    """Similar to the :func:`processor` but passes through old values
    unchanged and does not pass through the values as parameter.
    """
    @processor
    def new_func(stream, *args, **kwargs):
        for item in stream:
            yield item
        for item in f(*args, **kwargs):
            yield item
    return update_wrapper(new_func, f)


@cli.command("push")
@click.option("-f", " -- file", "files", type=click.Path(), multiple=True, help="The code file to push to kafka.")
@generator
def push_cmd(files):
    """Loads one or multiple code file for push to kafka. The input parameter
    can be specified multiple times to load more than one files.
    """
    for file in files:
        try:
            click.echo("Opening "%s"" % files)
            if files == "-":
                img = files.open(click.get_binary_stdin())
                img.filename = "-"
            else:
                img = files.open(files)
            yield img
        except Exception as e:
            click.echo("Could not open file "%s": %s" % (file, e), err=True)


@cli.command("logs")
@click.option(" -- filename", default="logs-%04d.txt", type=click.Path(), help="The format for the filename.", show_default=True)
@processor
def logs_cmd(filess, filename):
    """Saves all processed filess to a series of files."""
    for idx, files in enumerate(filess):
        try:
            fn = filename % (idx + 1)
            click.echo("Saving "%s" as "%s"" % (files.filename, fn))
            yield files.save(fn)
        except Exception as e:
            click.echo("Could not save files "%s": %s" %
                       (files.filename, e), err=True)


@cli.command("display")
@processor
def display_cmd(filess):
    """Opens all filess in an files viewer."""
    for files in filess:
        click.echo("Displaying "%s"" % files.filename)
        files.show()
        yield files


@cli.command("publish")
@click.option("-m", " -- message", type=str, help="The message to publish.")
@click.option("-t", " -- topic", type=str, help="The topics where publish the message.")
@processor
def resize_cmd(filess, width, height):
    """Resizes an files by fitting it into the box without changing
    the aspect ratio.
    """
    for files in filess:
        w, h = (width or files.size[0], height or files.size[1])
        click.echo("Resizing "%s" to %dx%d" % (files.filename, w, h))
        files.thumbnail((w, h))
        yield files


@cli.command("crop")
@click.option("-b", " -- border", type=int, help="Crop the files from all "
              "sides by this amount.")
@processor
def crop_cmd(filess, border):
    """Crops an files from all edges."""
    for files in filess:
        box = [0, 0, files.size[0], files.size[1]]

        if border is not None:
            for idx, val in enumerate(box):
                box[idx] = max(0, val - border)
            click.echo("Cropping "%s" by %dpx" % (files.filename, border))
            yield copy_filename(files.crop(box), files)
        else:
            yield files


@cli.command("transpose")
@click.option("-r", " -- rotate", callback=convert_rotation,
              help="Rotates the files (in degrees)")
@click.option("-f", " -- flip", callback=convert_flip,
              help="Flips the files  [LR / TB]")
@processor
def transpose_cmd(filess, rotate, flip):
    """Transposes an files by either rotating or flipping it."""
    for files in filess:
        if rotate is not None:
            mode, degrees = rotate
            click.echo("Rotate "%s" by %ddeg" % (files.filename, degrees))
            files = copy_filename(files.transpose(mode), files)
        if flip is not None:
            mode, direction = flip
            click.echo("Flip "%s" %s" % (files.filename, direction))
            files = copy_filename(files.transpose(mode), files)
        yield files


@cli.command("blur")
@click.option("-r", " -- radius", default=2, show_default=True,
              help="The blur radius.")
@processor
def blur_cmd(filess, radius):
    """Applies gaussian blur."""
    blur = filesFilter.GaussianBlur(radius)
    for files in filess:
        click.echo("Blurring "%s" by %dpx" % (files.filename, radius))
        yield copy_filename(files.filter(blur), files)


@cli.command("smoothen")
@click.option("-i", " -- iterations", default=1, show_default=True,
              help="How many iterations of the smoothen filter to run.")
@processor
def smoothen_cmd(filess, iterations):
    """Applies a smoothening filter."""
    for files in filess:
        click.echo("Smoothening "%s" %d time%s" %
                   (files.filename, iterations, iterations != 1 and "s" or "", ))
        for x in xrange(iterations):
            files = copy_filename(files.filter(filesFilter.BLUR), files)
        yield files


@cli.command("emboss")
@processor
def emboss_cmd(filess):
    """Embosses an files."""
    for files in filess:
        click.echo("Embossing "%s"" % files.filename)
        yield copy_filename(files.filter(filesFilter.EMBOSS), files)


@cli.command("sharpen")
@click.option("-f", " -- factor", default=2.0,
              help="Sharpens the files.", show_default=True)
@processor
def sharpen_cmd(filess, factor):
    """Sharpens an files."""
    for files in filess:
        click.echo("Sharpen "%s" by %f" % (files.filename, factor))
        enhancer = filesEnhance.Sharpness(files)
        yield copy_filename(enhancer.enhance(max(1.0, factor)), files)


@cli.command("paste")
@click.option("-l", " -- left", default=0, help="Offset from left.")
@click.option("-r", " -- right", default=0, help="Offset from right.")
@processor
def paste_cmd(filess, left, right):
    """Pastes the second files on the first files and leaves the rest
    unchanged.
    """
    filesiter = iter(filess)
    files = next(filesiter, None)
    to_paste = next(filesiter, None)

    if to_paste is None:
        if files is not None:
            yield files
        return

    click.echo("Paste "%s" on "%s"" % (to_paste.filename, files.filename))
    mask = None
    if to_paste.mode == "RGBA" or "transparency" in to_paste.info:
        mask = to_paste
    files.paste(to_paste, (left, right), mask)
    files.filename += "+" + to_paste.filename
    yield files

    for files in filesiter:
        yield files


@click.command()
@click.option("-c", " -- configure",
              type=click.Choice(["upper", "lower"]),
              prompt=True)
@click.argument("person", default="you")
def hello(case, person):
    response = "Hello World! Also, hey {} ☺️".format(person)
    if case == "upper":
        click.echo(response.upper())
    elif case == "lower":
        click.echo(response.lower())
    else:
        click.echo(response)
