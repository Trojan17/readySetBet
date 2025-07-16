"""
Setup script for Ready Set Bet application.
"""

from setuptools import setup, find_packages

setup(
    name="ready-set-bet",
    version="1.0.0",
    description="Digital betting board for the Ready Set Bet horse racing game",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        # No external dependencies - uses only Python standard library
    ],
    entry_points={
        "console_scripts": [
            "ready-set-bet=main:main",
        ],
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Games/Entertainment :: Board Games",
    ],
    keywords="board-game betting horse-racing ready-set-bet tkinter",
)
