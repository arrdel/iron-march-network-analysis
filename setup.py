"""
Setup configuration for Iron March Network Analysis package.
"""

from setuptools import setup, find_packages
import os

# Read the contents of README file
this_directory = os.path.abspath(os.path.dirname(__file__))
with open(os.path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# Read requirements
with open('requirements.txt') as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name='iron-march-analysis',
    version='1.0.0',
    author='Your Name',
    author_email='your.email@example.com',
    description='Network analysis toolkit for studying far-right forum interactions',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/knowledge_graph',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
    install_requires=requirements,
    include_package_data=True,
    zip_safe=False,
)
