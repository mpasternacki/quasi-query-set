class QuasiQuerySet(object):
    """General-use class imitating Django's lazy QuerySet API.

    This class deals only with lazily combining parameters into
    `combined_query' attribute, containing dictionary of lists.
    Interpretation of combined_query ('evaluating the queryset') is up
    to user or subclass.
    """

    def __eq__(self, other):
        return self.combined_query == other.combined_query

    def __init__(self, **kwargs):
        self.combined_query = dict((k, [v]) for k, v in kwargs.iteritems())

    def copy(self):
        rv = self.__class__()
        rv.combined_query = dict((k, v[:]) for k, v in self.combined_query.iteritems())
        return rv

    def update_in_place(self, **kwargs):
        """Update QQS in-place (destructively) with keyword arguments."""
        for k, v in kwargs.iteritems():
            if k in self.combined_query:
                self.combined_query[k].append(v)
            else:
                self.combined_query[k] = [v]
        return self

    def update(self, **kwargs):
        """Return new QQS, with current QQS's contents updated with kwargs."""
        return self.copy().update_in_place(**kwargs)
        

QQS = QuasiQuerySet
