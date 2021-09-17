"""
"""

from setuptools import setup


setup(
    name="wimp",
    url="https://github.com/cthwaite/wimp",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=["wimp"],
    zip_safe=True,
    entry_points={"console_scripts": ["wimp=wimp.__main__:main"]},
)
