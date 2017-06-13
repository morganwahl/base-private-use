from setuptools import setup

setup(
    name='base_private',
    version='0.5',
    description='Encode arbitrary bits in private-use codepoints.',
    url='https://github.com/morganwahl/base-private-use',
    author='Morgan Wahl',
    author_email='morgan.wahl@gmail.com',
    license='GPLv3',
    packages=['base_private'],
    test_suite='base_private.tests',
    tests_require=['hypothesis'],
    zip_safe=False,
)
