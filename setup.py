from setuptools import setup, find_packages

setup(
    name='PR_CYBR_DATABASE_AGENT',
    version='0.1.0',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=[
        'notion-client>=2.2.0',
    ],
    author='PR-CYBR',
    author_email='support@pr-cybr.com',
    description='PR-CYBR-DATABASE-AGENT',
    url='https://github.com/PR-CYBR/PR-CYBR-DATABASE-AGENT',
)
