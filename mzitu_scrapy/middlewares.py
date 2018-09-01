

class MeiZiTu(object):

    def process_request(self, request, spider):
        referer = request.meta.get('referer', None)
        if referer:
            request.headers['referer'] = referer
