  
class Topic:
    def __init__(self, data):
        self.data = data
       

    def topic_filtering(self):
        pass


class TopicRestricted(Topic):
    def __init__(self, data):
        super().__init__(data)
        self.words = ['forbidden', 'top-secret', 'dangerous','restricted']

    def topic_filtering(self):
        filter_result = super().topic_filtering(self)
        if filter_result:
            session =None;#vor trebui initializate aici
            topic = None;
            if topic:
                if session.username != 'admin' and topic in self.words:
                    return False
                return True
            else:
                return False
        return filter_result


class TopicAccess(Topic):
    def __init__(self, data):
        super().__init__(data)

    
    def topic_acces(topic_type, topic_info):
        split1 = topic_type.split('/')
        split2 = topic_info.split('/')
        result = True
        for i in range(min(len(split1), len(split2))):
            if  split2[i] == '#':
                break
            elif ( split2[i] == '+') or ( split2[i] == split1[i]):
                continue
            else:
                result = False
                break
        return result

    
    