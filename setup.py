import re


try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


version = ''
with open('osscache/__init__.py', 'r') as fd:
    version = re.search(r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]',
                        fd.read(), re.MULTILINE).group(1)

if not version:
    raise RuntimeError('Cannot find version information')

setup(
    name='scrapy-oss-cache',
    version=version,
    description='Use aliyun oss as a cache backend in Scrapy projects',
    packages=['osscache'],
    include_package_data=True,
    url='https://github.com/congeebrother/scrapy-oss-cache',
    author='daniel liu',
    author_email='daniel_001@126.com',
    install_requires=[
        'scrapy>1.0.0',
        'oss2',
    ],
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)