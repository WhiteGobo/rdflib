"""Implements nquads dataset serializer for RDFLib.

Implements serialization for [N-Quads](https://www.w3.org/TR/n-quads/),
a line-based, plain text format for encoding
[RDF datasets](https://www.w3.org/TR/rdf11-concepts/#section-dataset).

Additional `args` supported by [`Graph.serialize`][rdflib.graph.Graph.serialize]
are described by
[`NQuadsSerializer.serialize`][rdflib.plugins.serializers.nquads.NQuadsSerializer.serialize].

Example N-Quads document from [w3.org](https://www.w3.org/TR/n-quads/#sec-intro):
    ```nquads
    <http://one.example/subject1> <http://one.example/predicate1> <http://one.example/object1> <http://example.org/graph3> . # comments here
    # or on a line by themselves
    _:subject1 <http://an.example/predicate1> "object1" <http://example.org/graph1> .
    _:subject2 <http://an.example/predicate2> "object2" <http://example.org/graph5> .
    ```
"""
from __future__ import annotations

import warnings
from typing import IO, Any, Optional

from rdflib.graph import DATASET_DEFAULT_GRAPH_ID, ConjunctiveGraph, Graph
from rdflib.plugins.serializers.nt import _quoteLiteral
from rdflib.serializer import Serializer
from rdflib.term import Literal

__all__ = ["NQuadsSerializer"]


class NQuadsSerializer(Serializer):
    """NQuads RDF graph serializer."""

    def __init__(self, store: Graph):
        if not store.context_aware:
            raise Exception(
                "NQuads serialization only makes " "sense for context-aware stores!"
            )

        super(NQuadsSerializer, self).__init__(store)
        self.store: ConjunctiveGraph

    def serialize(
        self,
        stream: IO[bytes],
        base: Optional[str] = None,
        encoding: Optional[str] = None,
        **kwargs: Any,
    ) -> None:
        """Serialize data from connected store as N-Quads and print it to stream.

        Args:
            stream: Print data to this stream.
            base: Base will be ignored in N-Quads.
            encoding: Encoding used for stream.
            kwargs: Ignore the rest of the arguments.
        """
        if base is not None:
            warnings.warn("NQuadsSerializer does not support base.")
        if encoding is not None and encoding.lower() != self.encoding.lower():
            warnings.warn(
                "NQuadsSerializer does not use custom encoding. "
                f"Given encoding was: {encoding}"
            )
        encoding = self.encoding
        for context in self.store.contexts():
            for triple in context:
                stream.write(
                    _nq_row(triple, context.identifier).encode(encoding, "replace")
                )
        stream.write("\n".encode("latin-1"))


def _nq_row(triple, context):
    graph_name = context.n3() if context and context != DATASET_DEFAULT_GRAPH_ID else ""
    if isinstance(triple[2], Literal):
        return "%s %s %s %s .\n" % (
            triple[0].n3(),
            triple[1].n3(),
            _quoteLiteral(triple[2]),
            graph_name,
        )
    else:
        return "%s %s %s %s .\n" % (
            triple[0].n3(),
            triple[1].n3(),
            triple[2].n3(),
            graph_name,
        )
