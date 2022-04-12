from setuptools import find_packages, setup

setup(name='SafeObjectCompiler',
      version='0.1',
      description='safe object compiler',
      url='',
      author='Jingwei Zhang@Secure AI Labs',
      author_email='jingwei@secureailabs.com',
      license='',
      packages=find_packages(),
      package_data={'SafeObjectCompiler':['SafeObjectAPI.so']},
      zip_safe=False)
