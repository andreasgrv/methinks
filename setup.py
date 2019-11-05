from setuptools import setup, find_packages

setup(
      name='methinks',
      packages=find_packages(include=['methinks', 'methinks.*']),
      version='0.0.1',
      author='Andreas Grivas',
      author_email='andreasgrv@gmail.com',
      description='Keep track of your reading, your todos and your notes. Whatever thinketh you.',
      license='BSD',
      keywords=['self reporting'],
      scripts=['bin/methinks',
               'bin/methought',
               # 'bin/recap'
               ],
      classifiers=[],
      python_requires='>=3.5',
      tests_require=['pytest']
)
