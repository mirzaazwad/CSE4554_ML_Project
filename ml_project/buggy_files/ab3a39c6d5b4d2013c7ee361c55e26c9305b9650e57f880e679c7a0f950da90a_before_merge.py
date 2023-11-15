    def build_tensor_merge_graph(self, tensor_key):
        from ..tensor.expressions.merge.concatenate import TensorConcatenate

        tiled_tensor = self._get_tensor_by_key(tensor_key)
        graph = DAG()
        if len(tiled_tensor.chunks) == 1:
            # only one chunk, just trigger fetch
            c = tiled_tensor.chunks[0]
            op = TensorFetch(dtype=c.dtype)
            fetch_chunk = op.new_chunk(None, c.shape, index=c.index, _key=c.key).data
            graph.add_node(fetch_chunk)
        else:
            fetch_chunks = []
            for c in tiled_tensor.chunks:
                op = TensorFetch(dtype=c.dtype)
                fetch_chunk = op.new_chunk(None, c.shape, index=c.index, _key=c.key).data
                graph.add_node(fetch_chunk)
                fetch_chunks.append(fetch_chunk)
            chunk = TensorConcatenate(dtype=tiled_tensor.op.dtype).new_chunk(
                fetch_chunks, tiled_tensor.shape).data
            graph.add_node(chunk)
            [graph.add_edge(fetch_chunk, chunk) for fetch_chunk in fetch_chunks]

        return serialize_graph(graph)