from setuptools import setup

setup(
    name='lastweet',
    version='0.0.1',
    url='http://github.com/edsu/lastweet',
    author='Ed Summers',
    author_email='ehs@pobox.com',
    py_modules=['lastweet'],
    scripts=['lastweet.py'],
    description='Send Twitter/Mastodon updates about LastFM activity',
    install_requires=[
        "pylast",
        "tweepy",
        "requests",
        "Mastodon.py"
    ]
)
