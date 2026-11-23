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

if __name__ == '__main__':
    from sys import argv

    def main(arguments: dict, do_print: bool = False):
        try:
            text = minify_file(**arguments)
            if do_print:
                print(text)
        except FileNotFoundError:
            print(f"Cannot find file: \"{argv[1]}\"")

    if len(argv) == 3:
        args = {'file_in': argv[1], 'file_out': argv[2]}
        do_print = False
    elif len(argv) == 2:
        args = {'file_in': argv[1]}
        do_print = True
    else:
        print('minify.py by inimitable\nMinifies an SQF source file.\n\nUsage:\n\tminify.py filename_in [filename_out]')
        quit()

    main(args, do_print)