"""
Fake settings object
~~~~~~~~~~~~~~~~~~~~
"""
class FakeSettings(object):
    def __init__(self, network=None, mac_range=None):
        self.network = network
        self.mac_range = mac_range
