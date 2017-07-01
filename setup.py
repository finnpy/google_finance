from setuptools import setup

setup(name='google_finance',
      version='0.1',
      description='Stock quotes API',
      url='http://github.com/finnpy/google_finance',
      author='Tom Paoletti',
      author_email='zommaso@gmail.com',
      license='MIT',
      packages=['google_finance'],
      install_requires=[
          'requests',
      ],
      test_suite='nose.collector',
      tests_require=['nose'],
      zip_safe=False)
