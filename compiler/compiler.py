#!/usr/bin/env python3

"""
NAME: compiler.py

When run as a script, the compiler will compile all static content ('static/') and all uncompiled
content ('content/') into the output directory ('output/'). It will process markdown, using
python's built-in markdown library, as well as a few custom markdown extensions, which are
described in the markdown_ext.py file.

The files may contain yaml frontmatter, which will be scanned for additional attributes, such as
templates to be used, additional scripts, and page-specific CSS.

The argument --test-mode will compile links to the project level, rather than the output directory
level.

When imported as a module, this file will have the same composure and attitude as if it were run
as a script, however it will not run immediately. To compile the site, call the main function.
After main is called, the site will compile as described above.
"""

# pylint: disable=wrong-import-order,C0413

# Logging to console
import logging
from logging import log, INFO, WARN, ERROR, CRITICAL, DEBUG # pylint: disable=unused-import
# cspell: ignore levelname
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Text management tools
import re
import yaml

# File management tools
import os
import shutil

# Compilation tools
import html
import markdown
from sys import argv as sys_argv

try:
    from compiler.markdown_ext import extensions as custom_extensions
except (ModuleNotFoundError, ImportError):
    try:
        log(WARN, "Custom markdown extensions were not where expected. Trying again.")
        from markdown_ext import extensions as custom_extensions
    except (ModuleNotFoundError, ImportError):
        log(WARN, "Custom markdown extensions were not loaded...")
        custom_extensions = []

def main(test_mode: bool, dryrun: bool=False) -> None:
    """
    The main function orchestrates the entire site compilation process.

    This function performs the following tasks:
    1. Clears and recreates the 'output' directory.
    2. Logs a message indicating the start of the compilation process.
    3. Iterates over all files in the 'content' directory.
    4. Compiles each markdown (.md) or HTML (.htm, .html) file found.
    5. Logs a message indicating the completion of each file compilation.
    6. Logs a message indicating the completion of the compilation process.
    7. Copies the 'static' directory to the 'output' directory.
    8. Logs a message indicating the completion of the static content copying process.
    9. Logs a success message indicating the successful compilation of the site.

    Parameters:
    None

    Returns:
    None
    """
    if dryrun:
        log(INFO, 'would recursively delete ./output/')
    else:
        # Clear /output
        shutil.rmtree('output', ignore_errors=True)
    if dryrun:
        log(INFO, 'would mkdir ./output/')
    else:
        # Make /output
        os.mkdir('output')
    log(INFO, 'Emptied and replaced output directory')

    # Iterate over all files in content
    log(INFO, 'Iterating to compile....')
    for root, dirs, files in os.walk('content'): # pylint: disable=unused-variable
        root_parts = os.path.normpath(root).split(os.sep)
        rel_dir = os.path.join(*root_parts[1:]) if len(root_parts) > 1 else ''
        for filename in files:
            root_f = os.path.join(root, filename)
            rel_f = os.path.join(rel_dir, filename)
            compile_type = (
                'md'   if filename.endswith('.md'  ) else (
                'html' if filename.endswith('.html') else (
                'html' if filename.endswith('.htm' ) else (
                'raw' if filename.split('.')[-1] in ['txt', 'htaccess', 'json']
                else ( None
            )))))
            if compile_type is None:
                continue
            log(INFO, f'Compiling {rel_f}')
            compile_doc(root_f, kind=compile_type, test_mode=test_mode, dryrun=dryrun)
            log(INFO, f'Compiled  {rel_f}')

    # Copy static
    log(INFO, 'Compilation done. Copying static content...')
    if dryrun:
        log(INFO, 'Would recursively copy ./static/ to ./output/s/')
    else:
        shutil.copytree('static', os.path.join('output', 's'))
    log(INFO, 'Static content copied!')
    log(INFO, 'Site compiled successfully!!!')


def compile_doc(filename: str, kind: str, test_mode: bool, dryrun: bool) -> None:
    """
    Compiles a markdown or HTML document into HTML, applying a template and handling frontmatter.

    This function reads the contents of a markdown or HTML file, extracts the frontmatter
        (if present),
    processes the document contents based on the specified kind ('md' or 'html'), applies a
        template,
    and writes the resulting HTML to a new file in the 'output' directory.

    Parameters:
    filename (str): The path to the markdown or HTML file to be compiled.
    kind (str): The type of document to be compiled.
        If 'md', the document is processed as markdown.
        If 'html', the document is treated as plain HTML.
        If neither, the document is processed as plain text, and html-escaped.
    test_mode (bool): Weather to prepend /output/ to all internal links.
        This allows tools like VSCode Live Server to operate on the project level.

    Returns:
    None
    """
    # Read the file contents
    with open(filename, 'r', encoding='UTF-8') as f:
        doc_contents = f.read()

    # Extract the frontmatter
    frontmatter_regex = re.compile(r'^---\n(.*?)\n---(?:\n|$)', re.DOTALL)
    frontmatter = re.match(frontmatter_regex, doc_contents)
    if frontmatter:
        doc_contents = doc_contents[frontmatter.end():]
        # Parse the frontmatter as YAML
        data = parse_frontmatter(frontmatter, filename=filename)
    else: data={}

    if kind == 'md':
        # Process the markdown
        output = parse_doc_contents(doc_contents)
    elif kind == 'html':
        output = doc_contents
    elif kind == 'raw':
        output = doc_contents
    else:
        output = html.escape(doc_contents)

    if kind != 'raw':
        output = apply_template(output)

    if 'title' in data.keys():
        output = output.replace("{{{TITLE}}}", data['title'])
    if test_mode:
        output = output.replace("\"/", "\"/output/")
    new_directory = os.path.dirname(filename).replace('content','output')
    file = os.path.basename(filename).replace('md','html')
    if dryrun:
        log(INFO, f'Would ensure directory {new_directory} exists')
    else:
        os.makedirs(new_directory, exist_ok=True)

    if dryrun:
        log(INFO, f'Would write {os.path.join(new_directory, filename)}')
    else:
        with open(os.path.join(new_directory, file), 'w', encoding='utf-8') as f:
            f.write(output)

def parse_frontmatter(frontmatter: re.Match, filename) -> dict:
    """
    Parses the YAML frontmatter from a markdown document.

    This function extracts the YAML frontmatter from a given match object,
    representing the frontmatter in the markdown document. It then attempts to
    parse the YAML frontmatter using the `yaml.safe_load` function. If the YAML
    frontmatter is invalid, it logs a warning message and returns an empty dictionary.

    Parameters:
    frontmatter (re.Match): A match object representing the frontmatter in the markdown document.
        The frontmatter should be enclosed within triple dashes (---) at the beginning
        and end of the document.
    filename (str): The name of the markdown file being processed. This parameter is used in the
        warning message if the YAML frontmatter is invalid.

    Returns:
    dict: A dictionary containing the parsed YAML frontmatter. If the YAML frontmatter is invalid,
        an empty dictionary is returned.
    """
    real_frontmatter = frontmatter.group(1)
    try:
        data = yaml.safe_load(real_frontmatter)
    except yaml.YAMLError as e:
        log(WARN, f"Invalid YAML frontmatter in {filename} ----\n{e}")
        data = {}
    return data

def parse_doc_contents(markdown_text: str) -> str:
    """
    Processes the given markdown text and converts it into HTML.

    This function uses the Python-Markdown library to parse the markdown text.
    It applies the 'fenced_code', 'codehilite', and all custom extensions specified
        in the 'custom_extensions' list.
    The 'codehilite' extension is configured to not guess the language and to use
        the 'code-highlight' CSS class.

    Parameters:
    markdown_text (str): The markdown text to be processed.

    Returns:
    str: The resulting HTML after processing the markdown text.
    """
    # Process the markdown
    # Use fenced code, codehilite, and all custom extensions
    exts = ['fenced_code', 'codehilite']
    exts.extend(custom_extensions)
    result = markdown.markdown(
         markdown_text,
        extensions=exts,
        extension_configs = {
            'codehilite': {
                'guess_language': False,
                'css_class': 'code-highlight'
            }
        })

    return result

def apply_template(original: str) -> str:
    """
    Applies a template to the given original content.

    The function reads the main template file located at 'templates/main.html',
    replaces the placeholder '{{{CONTENT}}}' with the provided original content,
    and returns the resulting string.

    Parameters:
    original (str): The original content to be inserted into the template.

    Returns:
    str: The resulting string after applying the template.
    """
    with open('templates/main.html', 'r', encoding='utf-8') as f:
        template = f.read()

    # Replace '{{{CONTENT}}}' with the markdown result
    result = template.replace('{{{CONTENT}}}', original)
    return result


if __name__ == '__main__':
    main(
        test_mode = '--test-mode' in sys_argv
        )
