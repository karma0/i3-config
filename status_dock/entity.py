# -*- coding: utf-8 -*-

from status_dock.util import camel2snake


class EntityFactory(list): pass


class ModClassicMixin:
    def register(*a, **kw): pass

class ETypeMixin:
    def set_etype(self):
        if not hasattr(self, 'etype'):
            self.etype = camel2snake(self.__class__.__name__)


class NetTypeMixin:
    def gen_ent(self, cls, itr, conf=None):
        c = conf if conf else {}

        if not hasattr(self, '_list'):
            self._list = []

        for i in itr:
            ent = cls(self.conf)
            ent.conf.update({"interface": i})
            ent.conf.update(c)
            #print(ent.conf)
            self._list.append(ent)


class Entity(ETypeMixin):
    def __init__(self, conf):
        self.set_etype()
        try:
            self.conf = conf[self.etype]
        except KeyError:
            self.conf = {}

    def register(self, bar):
        bar.register(self.etype, **self.conf)
