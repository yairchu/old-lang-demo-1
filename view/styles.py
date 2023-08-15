from Style import Style

import view.default, view.flow, view.literal
flow = Style([view.default.widget_for, view.flow.widget_for])
literal = view.literal.literal_style

styles = [flow, literal]
