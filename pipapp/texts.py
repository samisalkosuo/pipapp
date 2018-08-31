# -*- coding: utf-8 -*-

# The MIT License (MIT)

# Copyright (c) 2016 Sami Salkosuo

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

import datetime
import textwrap
import string
import ast


def get_license_txt(author):
    license_text_template = string.Template(textwrap.dedent("""\
        The MIT License (MIT)

        Copyright (c) ${year} ${author}
        
        Permission is hereby granted, free of charge, to any person obtaining a copy
        of this software and associated documentation files (the "Software"), to deal
        in the Software without restriction, including without limitation the rights
        to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
        copies of the Software, and to permit persons to whom the Software is
        furnished to do so, subject to the following conditions:
        
        The above copyright notice and this permission notice shall be included in all
        copies or substantial portions of the Software.
        
        THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
        IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
        FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
        AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
        LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
        OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
        SOFTWARE."""))
    return license_text_template.substitute(
        year=datetime.date.today().strftime("%Y"),
        author=author
    )


def get_readme_txt(project_name="PROJECTNAME"):
    header = "=" * len(project_name)
    readme_template = string.Template(textwrap.dedent("""\
        ${project_name}
        ${header}
        
        Project description
        
        Requirements
        ------------
        
        Python 3.
        
        Install
        -------
        
        Install latest version: **pip install ${project_name}**.
        
        Usage
        -----
        
        Execute *${project_name}*.
        
        
        About
        -----
        
        """))
    return readme_template.substitute(
        project_name=project_name,
        header=header
    )


def get_setup_cfg_txt():
    text = "[bdist_wheel]\nuniversal = 0"
    return text


def get_runner_txt(project_name):
    text_template = string.Template(textwrap.dedent('''\
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        
        
        """Convenience wrapper for running ${project_name} directly from source tree."""
        
        
        from ${project_name}.${project_name} import main
        
        
        if __name__ == '__main__':
            main()
        '''))
    return text_template.substitute(
        project_name=project_name
    )


def get_manifest_in(project_name):
    txt = textwrap.dedent(
        '''\
        # Include the license file
        include LICENSE 
        '''
    )
    return txt


def get_setup_py(project_name, config):

    # The classifiers list is stored as a single string, like: "['a', 'b']". Convert back into a list.
    classifiers_list = ast.literal_eval(config['classifiers'])
    formatted_classifiers = textwrap.indent(
        "\n".join("'{}',".format(classifier) for classifier in classifiers_list),
        " " * 8
    )

    setup_py_template = string.Template(textwrap.dedent('''\
        # -*- coding: utf-8 -*-
        
        """setup.py: setuptools control."""
        
        
        import re
        from setuptools import setup, find_packages
        
        project_name = "${project_name}"
        script_file = "{project_name}/{project_name}.py".format(project_name=project_name)
        description = "Setuptools setup.py for ${project_name}."
        
        with open(script_file, "r", encoding="utf-8") as opened_script_file:
            version = re.search(
                r"""^__version__\s*=\s*"(.*)"\s*""",
                opened_script_file.read(),
                re.M
                ).group(1)
        
        
        with open("README.rst", "r", encoding="utf-8") as f:
            long_description = f.read()
        
        
        setup(
            name=project_name,
            packages=find_packages(),
            # add required packages to install_requires list
            # install_requires=["package", "package2"],
            entry_points={
                "console_scripts": [
                    "{project_name} = {project_name}.{project_name}:main".format(project_name=project_name)
                ]
            },
            version=version,
            description=description,
            long_description=long_description,
            author="${author}",
            author_email="${author_email}",
            url="${url}",
            license="${license}",
            # list of classifiers: https://pypi.python.org/pypi?%3Aaction=list_classifiers
            classifiers=[
        ${classifiers}
            ],
        )
        '''))
    # The classifiers are indented manually at level 2. Thus the template is at the base level, so that all lines are
    # indented equally.
    return setup_py_template.substitute(
        project_name=project_name,
        author=config['author'],
        author_email=config['author_email'],
        url=config['url'],
        license=config['license'],
        classifiers=formatted_classifiers
    )


def get_init_py(project_name):
    # empty __init__.py is enough
    return ""  


def get_main_py(project_name):
    main_py_template = string.Template(textwrap.dedent('''\
        # -*- coding: utf-8 -*-
        
        """${project_name}.__main__: executed when ${project_name} directory is called as script."""
        
        from .${project_name} import main
        
        main()
        '''))
    
    return main_py_template.substitute(
        project_name=project_name
    )


def get_main_source(project_name, license_text, config):

    # Does not need to be indented, because it will be substituted in after textwrap.dedent finished the pre-processing.
    escaped_license_text = "\n".join("# {line:s}".format(line=line) for line in license_text.split("\n"))

    main_template = string.Template(textwrap.dedent('''\
        #!/usr/bin/env python3
        # -*- coding: utf-8 -*-
        
        ${license_text}
        
        # add correct version number here
        __version__ = "0.0.1"
        
        
        PROGRAMNAME = "${project_name}"
        VERSION = __version__
        COPYRIGHT = "(C) ${current_year} ${author}"
        
        
        def main():
            # program logic here
            print("TODO: the application")
            pass
        
        
        if __name__ == "__main__": 
            main()
        '''))
    
    return main_template.substitute(
        license_text=escaped_license_text,
        project_name=project_name,
        current_year=datetime.date.today().strftime("%Y"),
        author=config['author']
    )
