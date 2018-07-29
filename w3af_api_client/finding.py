from .utils.details import Details
from .traffic import Traffic


class Finding(Details):
    """
    A wrapper around the finding, initially it's a shallow object but when
    one of the attributes is accessed it will connect to the REST API and
    retrieve the information
    """
    def __init__(self, conn, finding_href):
        super(Finding, self).__init__(conn, finding_href)

    def get_traffic(self):
        return [Traffic(self.conn, traffic_href) for traffic_href in self.traffic_hrefs]

    def __repr__(self):
        return '<Finding for href="%s">' % self.resource_href