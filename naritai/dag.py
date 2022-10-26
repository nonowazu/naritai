from __future__ import annotations

from collections.abc import Iterable, Iterator
from typing import Generic, TypeVar
from graphlib import TopologicalSorter

V = TypeVar('V')

class DAG(Generic[V]):
    """Creates a directed acyclic graph of type view

    :param initial_vertexes: A list of initial edges
    :type initial_vertexes: list[tuple[V, V] | tuple[V]]
    """
    def __init__(self, initial_vertexes: list[tuple[V, V] | tuple[V]] | None = None):
        self._graph: dict[V, set[V]] = {}
        # TODO: The typing for this is horrible and I don't like it
        if initial_vertexes is not None:
            for edge in initial_vertexes:
                if len(edge) == 1:
                    self.add_vertex(edge[0])
                else:
                    self.add_edge(*edge)

    def __contains__(self, vertex: V) -> bool:
        """Determines if an item is in the graph

        :param item: The item to search for
        :return: True if the item is in the graph, False otherwise
        """
        return vertex in self._graph

    def __getitem__(self, key: V) -> set[V]:
        """Returns the set of nodes that this node points to

        :raises KeyError: On invalid key, a KeyError is raised
        :param key: The node to get the children for
        :return: A set of nodes this node points to
        """
        if key not in self._graph:
            raise KeyError(key)
        return self._graph[key]

    def items(self):
        """Returns a set-like object which has key/value pairs of the graph's structure

        :return: a set-like object providing a view on the graph's items
        """
        return self._graph.items()

    def __len__(self) -> int:
        """Returns the number of nodes in the graph

        :return: The number of nodes in the graph
        """
        return len(self._graph)

    def __delitem__(self, key: V):
        """Deletes a node from the graph, including children and add edges that link to the node

        :param key: The node to remove
        """
        to_delete = self[key].copy()
        for vertex in self._graph:
            if key in self._graph[vertex]:
                self._graph[vertex].remove(key)
        for node in to_delete:
            # Is recursive delete the right thing to do here?
            del self[node]
        del self._graph[key]

    def __iter__(self) -> Iterator[V]:
        """Returns an iterator of the graph

        :return: An iterator of the graph's nodes
        """
        return iter(self._graph)

    def add_vertex(self, vertex: V):
        """Add a node to the graph

        :param node: The node to add
        """
        if vertex not in self._graph:
            self._graph[vertex] = set()

    def add_edge(self, u: V, v: V):
        """Adds an edge between two nodes (creating them if needed)

        :param parent: The parent node
        :param node: The node to point to
        """
        if u not in self._graph:
            self.add_vertex(u)
        if v not in self._graph:
            self.add_vertex(v)
        self._graph[u].add(v)

    def subgraph(self, node: V) -> DAG[V]:
        """Return a new dag object from the provided node downward

        :param node: The node to act as the new 'head' of the graph

        :return: A new graph centered at ``node``
        """
        if node not in self:
            # not sure this is great - might be better to raise an exception
            return DAG([(node,)])
        # TODO: check if graph is cyclic prior to starting, and bail out if so

        vertices_to_visit: list[V] = [node]
        edges: list[tuple[V, V] | tuple[V]] = [(node,)]

        while len(vertices_to_visit) > 0:
            next_node = vertices_to_visit.pop(0)
            child_nodes = self[next_node]
            vertices_to_visit.extend(child_nodes)
            edges.extend([(next_node,n) for n in child_nodes])

        return DAG(edges)

    def static_order(self) -> Iterable[V]:
        """Returns the nodes as an iterator topologicaly sorted

        :return: An iterator of nodes
        """
        ts = TopologicalSorter(self)
        return ts.static_order()

    def __str__(self) -> str:
        description = ''
        for node in self._graph:
            description += f'{repr(node)} -> [{", ".join([repr(x) for x in self._graph[node]])}]\n'
        return description

