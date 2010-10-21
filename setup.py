__author__    = 'Viktor Kerkez <alefnula@gmail.com>'
__contact__   = 'alefnula@gmail.com'
__date__      = '21 October 2010'
__copyright__ = 'Copyright (c) 2010 Viktor Kerkez'

from distutils.core import setup

setup(
    name             = 'Panda',
    version          = '0.0.1',
    description      = 'Panda is a Scheme implementation in Python',
    long_description = 'Panda (abbreviated from Python Lambda) if a full Scheme implementation in Python language.',
    platforms        = ['Windows', 'POSIX', 'MacOS'],
    author           = 'Viktor Kerkez',
    author_email     = 'alefnula@gmail.com',
    maintainer       = 'Viktor Kerkez',
    maintainer_email = 'alefnula@gmail.com',
    url              = 'http://bitbucket.org/alefnula/panda/',
    license          = 'GPLv3',
    package_dir      = {'' : 'src'},
    packages         = [
                        'panda',
                       ],
    scripts          = [
                        'scripts/panda.py',
                       ],
)
