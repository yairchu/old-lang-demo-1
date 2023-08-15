from .BaseClassEdit import BaseClassEdit
from model.pyapi import nf_getattr
from model import class_fields
import pygame

class ClassEdit(BaseClassEdit):
    def drawmore(self, surface):
        cls = self.path[-1].cls
        links = nf_getattr(cls, class_fields.links)
        for dst, src in links.items():
            dst_rect, src_rect = list(map(self.node_rect, [dst, src]))
            if None in [dst_rect, src_rect]:
                continue
            dst_pos = dst_rect.center
            src_pos = src_rect.center
            pygame.draw.line(
                surface, (255, 50, 50), src_pos, dst_pos, 3)
    def graph_node(self, node):
        return node[0]
    def graph(self):
        result = {}
        cls = self.path[-1].cls
        fields = nf_getattr(cls, class_fields.fields)
        links = nf_getattr(cls, class_fields.links)
        for field in fields:
            result[field] = set()
        for dst, src in links.items():
            result[self.graph_node(dst)].add(self.graph_node(src))
        return result
    def calc_rows(self, size):
        graph = self.graph()
        from lib import graphs
        order = graphs.topological_sort(graph)
        self.rows = []
        for node in order:
            last = None
            for row in reversed(self.rows):
                if set(row) & graph[node]:
                    break
                last = row
            if last is None:
                last = []
                self.rows.append(last)
            last.append(node)
