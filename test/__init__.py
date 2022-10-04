import unittest
import graphlib

from naritai.dag import DAG


class TestDAG(unittest.TestCase):
    def test_initial_set(self):
        """You can create a dag from a list of edges"""
        initial_set = [
            (1,),
            (1, 2),
            (1, 3),
            (2, 4),
        ]
        #     1
        #    / \
        #   2   3
        #  /
        # 4
        # 4 vertices, 3 edges total
        dag: DAG[int] = DAG(initial_set)
        self.assertEqual(len(dag), 4)
        self.assertEqual(len(dag[1]), 2)
        self.assertEqual(len(dag[2]), 1)
        self.assertEqual(len(dag[3]), 0)

    def test_add_vertex(self):
        """You should be able to add a vertex by itself, or via association with an edge"""
        dag: DAG[int] = DAG()
        dag.add_vertex(2)
        self.assertEqual(len(dag), 1)
        self.assertEqual(len(dag[2]), 0) # should have no links
        self.assertEqual(dag[2], set()) # should be an empty set
        dag.add_edge(2, 3)
        self.assertEqual(len(dag), 2)
        self.assertEqual(len(dag[2]), 1) # should have one link
        self.assertEqual(dag[2], {3,}) # should be equal to a set that has one value
        dag.add_edge(2, 4)
        self.assertEqual(len(dag), 3)
        self.assertEqual(len(dag[2]), 2) # two links now
        self.assertCountEqual(dag[2], {3, 4}) # should have two links

    def test_len(self):
        """Using `len` on the DAG should return the number of vertices in the graph"""
        dag: DAG[int] = DAG()
        dag.add_vertex(1)
        self.assertEqual(len(dag), 1)
        dag.add_vertex(2)
        self.assertEqual(len(dag), 2)
        dag.add_edge(1, 2) # shouldn't increase, since both nodes exist
        self.assertEqual(len(dag), 2)
        dag.add_edge(1, 3)
        self.assertEqual(len(dag), 3)

    def test_contains(self):
        """Using `a in b` should be possible with the DAG object to test for existence of
        vertices in the graph"""
        first = 'first'
        dag: DAG[str] = DAG()
        dag.add_vertex(first)
        self.assertIn(first, dag)

    def test_iterator(self):
        """The DAG can be iterated on like an object"""
        dag: DAG[int] = DAG()
        # since the internal dictionary struct makes a guarantee that
        # the elements are in order, this should suffice for testing
        dag.add_vertex(1)
        dag.add_vertex(3)
        dag.add_vertex(2)
        dag_iterator = iter(dag)
        self.assertEqual(next(dag_iterator), 1)
        self.assertEqual(next(dag_iterator), 3)
        self.assertEqual(next(dag_iterator), 2)

    def test_delete_vertex(self):
        """It should be possible to delete a vertex using the keyword"""
        dag: DAG[int] = DAG()
        dag.add_vertex(1)
        self.assertEqual(len(dag), 1)
        del dag[1]
        self.assertEqual(len(dag), 0)
        with self.assertRaises(KeyError):
            _vertices = dag[1]

    def test_cycles(self):
        """This should be compatible with graphlib's topological sorting"""
        dag: DAG[int] = DAG()
        dag.add_edge(1, 2)
        dag.add_edge(1, 3)
        #   1
        #  / \
        # 2   3
        # 👍 no cycle
        ts = graphlib.TopologicalSorter(dag)
        self.assertCountEqual(list(ts.static_order()), [3, 2, 1])
        self.assertCountEqual(list(dag.static_order()), [2, 3, 1])
        dag.add_edge(3, 1)
        #   1 ---┒
        #  / \   │
        # 2   3 -┘
        # 👎 cycle
        ts = graphlib.TopologicalSorter(dag)
        with self.assertRaises(graphlib.CycleError):
            busted_order = list(ts.static_order())
        with self.assertRaises(graphlib.CycleError):
            busted_order = list(dag.static_order())