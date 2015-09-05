from jinja2 import Markup, escape


def line_breaks_filter(value):
    """ Convert linebreaks to <br/>s and escape each line.  Return value is marked 'safe' """
    escaped_lines = []
    for line in value.split('\n'):
        escaped_lines.append(escape(line))
    escaped = "<br/>".join(escaped_lines)
    # mark as safe
    return Markup(escaped)
