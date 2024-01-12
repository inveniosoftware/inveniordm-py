class SimplePagination:
    def __init__(self, data_list, factory, prev_page, next_page):
        self._factory = factory
        self._hits = data_list.hits
        self._total = data_list.total
        self._aggregations = data_list.aggregations
        self._prev_page = prev_page
        self._next_page = next_page

    def __iter__(self):
        for h in self._hits:
            yield self._factory(h)

    def __len__(self):
        return len(self._hits)

    def next_page(self):
        return self._next_page()

    def prev_page(self):
        return self._prev_page()
