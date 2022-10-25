from __future__ import annotations

__version__ = '0.0.0' # not functional, do not use

from naritai.dag import DAG

class Step:
    def __init__(self, pipeline_ref: Pipeline):
        self.pipeline_ref = pipeline_ref

    def add_step(self) -> Step:
        return self.pipeline_ref.add_step(self)

    def __repr__(self) -> str:
        return f'<Step {hex(id(self))}>'


class Pipeline:
    def __init__(self):
        self.graph: DAG[Step] = DAG()

    def add_step(self, parent: Step | None = None) -> Step:
        step = Step(self)
        if parent is None:
            self.graph.add_vertex(step)
        else:
            self.graph.add_edge(parent, step)
        return step

    def __repr__(self) -> str:
        return '<Pipeline>'
