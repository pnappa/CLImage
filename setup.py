# -*- coding: utf-8 -*-
"""
# CLImage

Convert images to beautiful ANSI escape codes for display in command line interfaces.

Available as both a CLI application and a Python library.

![demo](https://raw.github.com/pnappa/CLImage/master/extra/demo.png)

## Features
 - 8/16/256/Truecolor supports
 - Custom system color palettes
 - Toggleable Unicode mode, allowing up to 4x more detail
 - Custom output size

## Example usage
### CLI
`$ climage --unicode --truecolor --cols 80 barney.jpg`

![cliusage](https://raw.github.com/pnappa/CLImage/master/extra/clibarney.png)

For more detail and available options, run `$ climage --help`.

### Python
```python3
import climage

output = climage.convert('image.png', is_unicode=True)
print(output)
```

"""
from setuptools import setup

setup(name='climage',
      version='0.1.2',
      description='Convert images to beautiful ANSI escape codes',
      long_description=__doc__,
      long_description_content_type='text/markdown',
      url='http://github.com/pnappa/CLImage',
      author='Patrick Nappa',
      author_email='patricknappa@gmail.com',
      license='MIT',
      packages=['climage'],
      entry_points={
          'console_scripts': [
              'climage = climage:main',
              ]
          },
      python_requires=">=3.2",
      classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "License :: OSI Approved",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.2",
        "Programming Language :: Python :: 3.3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Topic :: Artistic Software",
        "Topic :: Multimedia :: Graphics",
        "Topic :: System :: System Shells",
        "Topic :: Utilities"
        ],
      install_requires=[
          'Pillow',
          'kdtree'
      ],
      zip_safe=False)
