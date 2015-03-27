class HostUtils(object):

    @classmethod
    def host_selectors(self, all_selectors, host):
        selectors = all_selectors[host]
        if type(selectors) is dict:
            selectors = all_selectors[selectors['reference']]
        return selectors
