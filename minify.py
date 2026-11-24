#!/usr/bin/env python3
# -*- coding: UTF-8 -*-
"""Minifies an SQF file."""
from pathlib import Path
from re import sub, compile, DOTALL

INLINE_COMMENT = compile(r'//+[^\n]+')
BLOCK_COMMENT = compile(r'/\*.*?\*/', DOTALL)
COMBINED_WHITESPACE = compile(r'/\*(?:(?!\*/)(?:.|\n))*\*/\n| {2,}|\t|\n\n+')

def minify_file(file_in: (Path, str), file_out: (Path, str, bool, None) = False) -> str:
    """Minifies an SQF file, optionally outputting minified text to a file."""
    file_in = Path(file_in)
    if file_out is None:
        file_out = file_in.parent / f"{file_in.stem}-min{file_in.suffix}"

    text = file_in.read_text()

    # Strip comments
    text = INLINE_COMMENT.sub('', text)
    text = BLOCK_COMMENT.sub('', text)

    # Handle preprocessor lines, then strip whitespace in one pass
    parts = text.splitlines()
    output_parts = []
    for line in parts:
        if line[:1] == '#':
            output_parts.append(f'\n{line}\n')
        else:
            output_parts.append(line)

    output = COMBINED_WHITESPACE.sub(
        lambda m: '\n' if m.group() and '\n\n' in m.group() else '',
        ''.join(output_parts)
    ).lstrip('\n')

    if file_out:
        file_out = Path(file_out)
        file_out.write_text(output)

    return output

def format_sizes(file: str, size_before: int, size_after: int, name_width: int = 60) -> str:
    """Returns a fixed-width size report string in KB."""
    saved = size_before - size_after
    percent = (saved / size_before * 100) if size_before else 0.0
    name = file if len(file) <= name_width else '...' + file[-(name_width - 3):]
    return f"{name:<{name_width}} {size_after / 1024:>8.2f} KB | {percent:>6.2f}%"

if __name__ == '__main__':
    from sys import argv, stderr

    def main(arguments: dict, do_print: bool = False, do_report: bool = False):
        try:
            size_before = Path(arguments['file_in']).stat().st_size
            text = minify_file(**arguments)
            size_after = len(text.encode('utf-8'))
            if do_print:
                print(text)
            if do_report and size_after < size_before:
                print(format_sizes(arguments['file_out'], size_before, size_after), file=stderr)
        except FileNotFoundError:
            print(f"Cannot find file: \"{argv[1]}\"")

    if len(argv) == 3:
        args = {'file_in': argv[1], 'file_out': argv[2]}
        do_print = False
        do_report = True
    elif len(argv) == 2:
        args = {'file_in': argv[1]}
        do_print = True
        do_report = False
    else:
        print('minify.py by inimitable\nMinifies an SQF source file.\n\nUsage:\n\tminify.py filename_in [filename_out]')
        quit()

    main(args, do_print, do_report)