from setuptools import setup

setup(
    name='jdesigner',
    version='0.0.1',
    packages=['jdesigner'],
    url='https://github.com/jakaspeh/JDesigner',
    license='MIT',
    author='Jaka Speh',
    author_email='jaka@jakascorner.com',
    description='XKCD designer for mathematicians',
    install_requires=[
        'matplotlib>=1.3.1',
        'pyqtgraph>=0.9.10',
        'numpy>=1.8.2'],
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Environment :: X11 Applications :: Qt',
        'Intended Audience :: End Users/Desktop',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Desktop Environment']
    )
