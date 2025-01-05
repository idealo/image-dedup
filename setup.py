import os
import sys
from setuptools import setup, find_packages, Extension

long_description = '''
imagededup is a python package that provides functionality to find duplicates in a collection of images using a variety
of algorithms. Additionally, an evaluation and experimentation framework, is also provided. Following details the
functionality provided by the package:

* Finding duplicates in a directory using one of the following algorithms:
    - Convolutional Neural Network
    - Perceptual hashing
    - Difference hashing
    - Wavelet hashing
    - Average hashing
* Generation of features for images using one of the above stated algorithms.
* Framework to evaluate effectiveness of deduplication given a ground truth mapping.
* Plotting duplicates found for a given image file.

Read the documentation at: https://idealo.github.io/imagededup/

imagededup is compatible with Python 3.8+ and runs on Linux, MacOS X and Windows.
It is distributed under the Apache 2.0 license.
'''

# Cython compilation is not enabled by default
# http://docs.cython.org/en/latest/src/userguide/source_files_and_compilation.html#distributing-cython-modules


try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True

on_mac = sys.platform.startswith('darwin')
on_windows = sys.platform.startswith('win')

MOD_NAME = 'brute_force_cython_ext'
MOD_PATH = 'imagededup/handlers/search/brute_force_cython_ext'
COMPILE_LINK_ARGS = ['-O3', '-march=native', '-mtune=native']
# On Mac, use libc++ because Apple deprecated use of libstdc
COMPILE_ARGS_OSX = ['-stdlib=libc++']
LINK_ARGS_OSX = ['-lc++', '-nodefaultlibs']

# workaround for Cython generated cpp code being compiled with CC,
# not CXX. it causes compilation error with clang/llvm from nixpkgs
os.environ["CC"] = "clang++"

ext_modules = []
if use_cython and on_mac:
    ext_modules += cythonize([
        Extension(
            MOD_NAME,
            [MOD_PATH + '.pyx'],
            language='c++',
            extra_compile_args=COMPILE_LINK_ARGS + COMPILE_ARGS_OSX,
            extra_link_args=COMPILE_LINK_ARGS + LINK_ARGS_OSX,
        )
    ])
elif use_cython and on_windows:
    ext_modules += cythonize([
        Extension(
            MOD_NAME,
            [MOD_PATH + '.pyx'],
            language='c++',
        )
    ])
elif use_cython:
    ext_modules += cythonize([
        Extension(
            MOD_NAME,
            [MOD_PATH + '.pyx'],
            language='c++',
            extra_compile_args=COMPILE_LINK_ARGS,
            extra_link_args=COMPILE_LINK_ARGS,
        )
    ])
else:
    if on_mac:
        ext_modules += [Extension(MOD_NAME,
                                  [MOD_PATH + '.cpp'],
                                  extra_compile_args=COMPILE_ARGS_OSX,
                                  extra_link_args=LINK_ARGS_OSX,
                                  )
                        ]
    else:
        ext_modules += [Extension(MOD_NAME,
                                  [MOD_PATH + '.cpp'],
                                  )
                        ]


setup(
    name='imagededup',
    version='0.3.3',
    author='Tanuj Jain, Christopher Lennan, Zubin John, Dat Tran',
    author_email='tanuj.jain.10@gmail.com, christopherlennan@gmail.com, zrjohn@yahoo.com, datitran@gmail.com',
    description='Package for image deduplication',
    long_description=long_description,
    license='Apache 2.0',
    install_requires=[
        'torch',
        'torchvision',
        'Pillow>=9.0',
        'tqdm',
        'scikit-learn',
        'PyWavelets',
        'matplotlib',
        'pi-heif'
    ],
    extras_require={
        'tests': ['pytest', 'pytest-cov', 'pytest-mock', 'codecov'],
        'docs': ['mkdocs', 'mkdocs-material'],
        'dev': ['bumpversion', 'twine'],
    },
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: POSIX :: Linux',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Programming Language :: Cython',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ],
    packages=find_packages(exclude=('tests',)),
    ext_modules=ext_modules
)
