static int
check_bipartite(list_graph_t *lg, int *color)
{
	DIE(lg == NULL, "No graph in check_bipartite!");
	// using BFS
	queue_t *q = q_create(sizeof(int), lg->nodes);
	int node = 0;
	q_enqueue(q, &node);
	color[node] = 1;
	while(q_is_empty(q) == 0) {
		int first = *(int *)q_front(q);
		q_dequeue(q);
		ll_node_t *curr_neighbour = lg->neighbors[first]->head;
		// ma plimb prin lista de vecini
		while(curr_neighbour != NULL) {
			if (color[*(int *)curr_neighbour->data] == color[first]) {
				q_free(q);
				return 0;
			}
			if (color[*(int *)curr_neighbour->data] == 0) {
				q_enqueue(q, (int *)curr_neighbour->data);
				if (color[first] == 1)
					color[*(int *)curr_neighbour->data] = 2;
				else 
					color[*(int *)curr_neighbour->data] = 1;
			}
			curr_neighbour = curr_neighbour->next;
		}
	}
	q_free(q);
	return 1;
}