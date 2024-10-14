import pytest
import os


@pytest.fixture
def datadir(request):
    '''Returns an absolute path to the current test directory's local data
    directory.'''
    mydir = os.path.dirname(request.fspath)
    return os.path.abspath(os.path.join(mydir, 'data'))
