from django.contrib.admin import FieldListFilter


class IsNullFieldListFilter(FieldListFilter):
    def __init__(self, field, request, params, model, model_admin, field_path):
        self.lookup_kwarg = '%s__isnull' % field_path
        self.lookup_val = request.GET.get(self.lookup_kwarg, None)

        super(IsNullFieldListFilter, self).__init__(
            field, request, params, model, model_admin, field_path
        )

    def expected_parameters(self):
        return [self.lookup_kwarg]

    def choices(self, cl):
        for lookup, title in (
            (None, 'All'),
            ('False', 'Yes'),
            ('True', 'No')
        ):

            yield {
                'selected': self.lookup_val == lookup,
                'query_string': cl.get_query_string({
                    self.lookup_kwarg: lookup,
                }),
                'display': title,
            }
