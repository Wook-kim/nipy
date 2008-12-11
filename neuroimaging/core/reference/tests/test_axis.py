import types
import numpy as np
from neuroimaging.testing import *

from neuroimaging.core.reference.axis import Axis, ContinuousAxis, VoxelAxis, RegularAxis

class test_Axis(TestCase):

    def setUp(self):
        self.axis = Axis(name='xspace')

    # FIXME: Persumably we would have a defined set of valid axis
    # names.  There should be a test for setting valid and invalid
    # names.
    @dec.knownfailure    
    def test_init(self):
        # an invalid name shou;d raise an error
        self.fail("the valid names of axes has been removed so this doesn't raise an exception anymore")
        self.assertRaises(ValueError, Axis, name='bad_value')

    def test_eq(self):
        ax1 = Axis(name='xspace')
        ax2 = Axis(name='yspace')
        self.assertTrue(self.axis == ax1)
        self.assertFalse(self.axis == ax2)

    def test_valid(self):
        self.assertRaises(NotImplementedError, self.axis.isvalidvalue, 0)

    def test_max(self):
        assert not hasattr(self.axis, 'max')
#       self.assertRaises(NotImplementedError, self.axis.max)

    def test_min(self):
        assert not hasattr(self.axis, 'min')
#        self.assertRaises(NotImplementedError, self.axis.min)

    def test_range(self):
        assert not hasattr(self.axis, 'min')
#        self.assertRaises(NotImplementedError, self.axis.range)


class test_ContinuousAxis(TestCase):

    def setUp(self):
        self.finite = ContinuousAxis(name='xspace', low=0, high=10)
        self.infinite = ContinuousAxis(name='xspace')

    def test_init(self):
        self.assertTrue(self.finite.low == 0)
        self.assertTrue(self.finite.high == 10)
        self.assertTrue(self.infinite.low == -np.inf)
        self.assertTrue(self.infinite.high == np.inf)
        self.assertRaises(ValueError, ContinuousAxis,
                          name='xspace', low=0,high=0)
        self.assertRaises(ValueError, ContinuousAxis,
                          name='xspace', low=1,high=0)
        
    def test_eq(self):
        fin_ax1 = ContinuousAxis(name='xspace', low=0, high=10)
        fin_ax2 = ContinuousAxis(name='xspace', low=1, high=11)
        self.assertTrue(self.finite == fin_ax1)
        self.assertFalse(self.finite == fin_ax2)

        inf_ax1 = ContinuousAxis(name='xspace')
        inf_ax2 = ContinuousAxis(name='xspace', low=0, high=np.inf)
        self.assertTrue(self.infinite == inf_ax1)
        self.assertFalse(self.infinite == inf_ax2)


    def test_valid(self):
        self.assertFalse(self.finite.isvalidvalue(-1))
        self.assertTrue(self.finite.isvalidvalue(0))
        self.assertTrue(self.finite.isvalidvalue(5))
        self.assertFalse(self.finite.isvalidvalue(10))
        self.assertFalse(self.finite.isvalidvalue(15))

        self.assertTrue(self.infinite.isvalidvalue(-np.inf))
        self.assertTrue(self.infinite.isvalidvalue(-100))
        self.assertTrue(self.infinite.isvalidvalue(0))
        self.assertTrue(self.infinite.isvalidvalue(100))
        self.assertFalse(self.infinite.isvalidvalue(np.inf))

    def test_max(self):
        self.assertEqual(self.finite.max, 10)
        self.assertEqual(self.infinite.max, np.inf)

    def test_min(self):
        self.assertEqual(self.finite.min, 0)
        self.assertEqual(self.infinite.min, -np.inf)

    def test_range(self):
        self.assertEqual(self.finite.range, (0, 10))
        self.assertEqual(self.infinite.range, (-np.inf, np.inf))


class test_RegularAxis(TestCase):

    def setUp(self):
        self.finite = RegularAxis(name='xspace', start=0, step=2, length=10)
        self.infinite = RegularAxis(name='xspace', start=0, step=2)

    def test_init(self):
        self.assertEqual(self.finite.start, 0)
        self.assertEqual(self.finite.step, 2)
        self.assertEqual(self.finite.length, 10)

        self.assertEqual(self.infinite.start, 0)
        self.assertEqual(self.infinite.step, 2)
        self.assertEqual(self.infinite.length, np.inf)

    def test_eq(self):
        fin_ax1 = RegularAxis(name='xspace', start=0, step=2, length=10)
        fin_ax2 = RegularAxis(name='xspace', start=0, step=2, length=11)
        fin_ax3 = RegularAxis(name='xspace', start=0, step=3, length=10)
        fin_ax4 = RegularAxis(name='xspace', start=1, step=2, length=10)
        self.assertTrue(self.finite == fin_ax1)
        self.assertFalse(self.finite == fin_ax2)
        self.assertFalse(self.finite == fin_ax3)
        self.assertFalse(self.finite == fin_ax4)

        inf_ax1 = RegularAxis(name='xspace', start=0, step=2)
        inf_ax2 = RegularAxis(name='xspace', start=0, step=3)
        inf_ax3 = RegularAxis(name='xspace', start=1, step=2)
        inf_ax4 = RegularAxis(name='xspace', start=0, step=2, length=10)

        self.assertTrue(self.infinite == inf_ax1)
        self.assertFalse(self.infinite == inf_ax2)
        self.assertFalse(self.infinite == inf_ax3)
        self.assertFalse(self.infinite == inf_ax4)

    def test_valid(self):
        self.assertFalse(self.finite.isvalidvalue(-2))
        self.assertTrue(self.finite.isvalidvalue(0))
        self.assertTrue(self.finite.isvalidvalue(2))
        self.assertTrue(self.finite.isvalidvalue(18))
        self.assertFalse(self.finite.isvalidvalue(20))
        self.assertFalse(self.finite.isvalidvalue(200))
        self.assertFalse(self.finite.isvalidvalue(2.5))

        self.assertFalse(self.infinite.isvalidvalue(-2))
        self.assertTrue(self.infinite.isvalidvalue(0))
        self.assertTrue(self.infinite.isvalidvalue(2))
        self.assertFalse(self.infinite.isvalidvalue(2.5))
        self.assertTrue(self.infinite.isvalidvalue(2000))
        self.assertFalse(self.infinite.isvalidvalue(np.inf))
        self.assertFalse(self.infinite.isvalidvalue(-np.inf))


    def test_max(self):
        self.assertEqual(self.finite.max, 18)
        self.assertEqual(self.infinite.max, np.inf)

    def test_min(self):
        self.assertEqual(self.finite.min, 0)
        self.assertEqual(self.infinite.min, 0)

    def test_range(self):
        self.assertEqual(self.finite.range, (0, 18))
        self.assertEqual(self.infinite.range, (0, np.inf))

    def test_values(self):
        self.assertTrue((self.finite.values == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18]).all)
        v = self.infinite.values
        self.assertTrue([v.next() for _ in range(10)] == [0, 2, 4, 6, 8, 10, 12, 14, 16, 18])
        self.assertEqual(type(self.infinite.values), types.GeneratorType)




class test_VoxelAxis(TestCase):

    def setUp(self):
        self.finite = VoxelAxis(name='xspace', length=10)
        self.infinite = VoxelAxis(name='xspace')

    def test_init(self):
        self.assertEqual(self.finite.start, 0)
        self.assertEqual(self.finite.step, 1)
        self.assertEqual(self.finite.length, 10)

        self.assertEqual(self.infinite.start, 0)
        self.assertEqual(self.infinite.step, 1)
        self.assertEqual(self.infinite.length, np.inf)






