import os
from setuptools import setup, find_packages

long_desc = open(os.path.join(os.path.dirname(__file__), 'README.rst')).read()

setup(
    name="MorningScraper",
    version="0.1",
    author="Toby Dacre",
    author_email="toby.junk@gmail.com",
    description=('Simple scraper for morningstar.co.uk'),
    license="LGPLv2",
    keywords="morningstar",
    url="https://github.com/tobes/MorningScraper",
    packages=find_packages(),
    long_description=long_desc,
    install_requires=['beautifulsoup4'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Topic :: Utilities",
        "License :: OSI Approved :: "
        "GNU Lesser General Public License v2 (LGPLv2)",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],
)
