try:
    import unittest2 as unittest
except ImportError:
    import unittest
    for decorator in ('expectedFailure', ):
        if not hasattr(unittest, decorator):
            setattr(unittest, decorator, lambda x : x)

from qqs import *

class QqsTestCase(unittest.TestCase):

    def assertCombinedEqual(self, qqs, **kwargs):
        self.assertEqual(kwargs, qqs.combined_query)

    def test_new_qqs(self):
        """Empty QQS behaves sanely."""
        self.assertCombinedEqual(QuasiQuerySet())
        self.assertCombinedEqual(QuasiQuerySet(foo='bar'), foo=['bar'])

    def test_equals(self):
        """Two QQSes with same parameters are equal."""
        self.assertEqual(QuasiQuerySet(), QuasiQuerySet())
        self.assertEqual(QuasiQuerySet(foo='bar'), QuasiQuerySet(foo='bar'))

    def test_copy(self):
        """QQS.copy() method returns a new, identical instance.

        This instance's combined_query dictionary is not share does not
        share original's lists as values."""
        original = QQS(foo='bar', baz='quux')
        copy = original.copy()
        self.assertFalse(original is copy, 'Original is copy')
        self.assertEqual(original, copy, 'Copy is not equal to original')

        self.assertFalse(original.combined_query is copy.combined_query,
                         'Original and copy share combined_query dict.')

        for k in original.combined_query:
            self.assertFalse(original.combined_query[k] is copy.combined_query[k],
                             "Original and copy share combined_query dict's values")

    def test_update_in_place(self):
        """QQS.update_in_place() works as advertised."""
        a = QQS(foo='bar')
        self.assertCombinedEqual(a, foo=['bar'])
        b = a.update_in_place(baz='quux')
        self.assertTrue(a is b)
        self.assertCombinedEqual(a, foo=['bar'], baz=['quux'])
        c = b.update_in_place(foo='xyzzy', baz='aaa')
        self.assertTrue(a is c)
        self.assertCombinedEqual(a, foo=['bar', 'xyzzy'], baz=['quux', 'aaa'])

    def test_update(self):
        """QQS.update() method behaves sanely."""
        foo = QuasiQuerySet(a='foo')
        bar = foo.update(a='bar')
        baz = bar.update(a='baz')
        baz_quux = baz.update(b='quux')
        foo_xyzzy = foo.update(b='xyzzy')
        baz_xyzzy = baz.update(b='xyzzy')

        for a, b in ((foo, bar), (bar, baz), (baz, baz_quux),
                     (baz_quux, foo_xyzzy), (foo_xyzzy, baz_xyzzy)):
            self.assertFalse(a is b)

        self.assertCombinedEqual(foo, a=['foo'])
        self.assertCombinedEqual(bar, a=['foo', 'bar'])
        self.assertCombinedEqual(baz, a=['foo', 'bar', 'baz'])
        self.assertCombinedEqual(baz_quux, a=['foo', 'bar', 'baz'], b=['quux'])
        self.assertCombinedEqual(foo_xyzzy, a=['foo'], b=['xyzzy'])
        self.assertCombinedEqual(baz_xyzzy, a=['foo', 'bar', 'baz'], b=['xyzzy'])

if __name__ == '__main__':
    unittest.main()
