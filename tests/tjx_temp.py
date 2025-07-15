import array
import pytest

class TJXTemp:
    #
    def _test02(self):
        assert 1 + 1 == 2

    #
    def _test04(self):
        assert 1 + 1 == 2

    #
    def _test05(self):
        assert 1 + 1 == 2

    #
    def _test06(self):
        assert 1 + 1 == 3

    #
    def test(self, case: array = None):
        if case is None:
            for name in dir(self):
                if name.startswith('_test') and not name.endswith('__'):
                    method = getattr(self, name)
                    if callable(method):
                        method()
        else:
            for item in case:
                try:
                    method = getattr(self, '_test' + item)
                    if callable(method):
                        method()
                except AttributeError as e:
                    pass
                    # logger.error(e)
                except Exception as e:
                    pass
                    # logger.error(e)

if __name__ == '__main__':
    pass
    # unittest.main()