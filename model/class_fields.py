from .field import PublicField

fields = PublicField({'label': 'fields'}, None)
links = PublicField({'label': 'links'}, None)
computer = PublicField({'label': 'computer'}, None)
format = PublicField({'label': 'format'}, None)

all_fields = [fields, links, computer, format]
