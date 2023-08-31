import pytest
import os


@pytest.fixture
def scroot():
    '''Returns an absolute path to the SC root directory.'''
    mydir = os.path.dirname(__file__)
    return os.path.abspath(os.path.join(mydir, '..', 'siliconcompiler'))


@pytest.fixture
def datadir(request):
    '''Returns an absolute path to the current test directory's local data
    directory.'''
    mydir = os.path.dirname(request.fspath)
    return os.path.abspath(os.path.join(mydir, 'data'))
