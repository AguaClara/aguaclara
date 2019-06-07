class SharedConfig(object):
    configs = {}

    def __init__(self, q):
        self.q = q
        
class SubComponent(object):

    def __init__(self, q = 20, foo = "bar"):
        configs = SharedConfig.configs
        hex_code = hex(id(self))
        
        if hex_code not in configs:
            configs[hex_code] = SharedConfig(q)

        self.foo = foo

    @property
    def q(self):
        return SharedConfig.configs[hex(id(self))].q
        
class Component(object):

    def __init__(self, q = 20, sub = SubComponent()):
        configs = SharedConfig.configs
        hex_code = hex(id(self))

        if hex_code not in configs:
            configs[hex_code] = SharedConfig(q)
            
        hex_code_sub = hex(id(sub))
        configs[hex_code_sub] = configs[hex_code]

        self.sub = sub

    @property
    def q(self):
        return SharedConfig.configs[hex(id(self))].q