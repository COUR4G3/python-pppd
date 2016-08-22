from setuptools import setup

from pppd import __version__ as version

def long_description():
    description = open('README.rst').read()
    try:
        description += '\n\n' + open('CHANGELOG.rst').read()
    except:
        pass
    return description

setup(
    name='python-pppd',
    version=version,
    url='https://github.com/cour4g3/python-pppd',
    license='MIT',
    author='Michael de Villiers',
    author_email='twistedcomplexity@gmail.com',
    description='Simple library for controlling PPP connections with pppd.',
    long_description=long_description(),
    py_modules=['pppd'],
    provides=['pppd'],
    platforms='any',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Networking',
    ]
)
