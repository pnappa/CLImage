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

# Converting downloaded file
from PIL import Image
import requests
response = requests.get('https://www.python.org/static/community_logos/python-logo-master-v3-TM-flattened.png')
# Convert to RGB, as files on the Internet may be greyscale, which are not
# supported.
img = Image.open(BytesIO(response.content)).convert('RGB')
# Convert the image to 80col, in 256 color mode, using unicode for higher def.
converted = climage.convert_pil(img, is_unicode=True)
print(converted)

# Convert the image into 50px * 50px, as the convert_array function does not
# perform resizing.
img = Image.open('image.png').convert('RGB').resize((50, 50))
arr = np.array(img)
output = climage.convert_array(arr, is_unicode=True)
print(output)
```

View additional examples on the [project homepage](https://github.com/pnappa/CLImage).

"""
from setuptools import setup

setup(
    name="climage",
    version="0.2.0",
    description="Convert images to beautiful ANSI escape codes",
    long_description=__doc__,
    long_description_content_type="text/markdown",
    url="http://github.com/pnappa/CLImage",
    author="Patrick Nappa",
    author_email="patricknappa@gmail.com",
    license="MIT",
    packages=["climage"],
    entry_points={
        "console_scripts": [
            "climage = climage:main",
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
        "Topic :: Utilities",
    ],
    install_requires=["Pillow", "kdtree"],
    zip_safe=False,
)
