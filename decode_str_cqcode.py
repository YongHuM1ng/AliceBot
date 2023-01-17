from alicebot.message import Message, MessageSegment


class Tools:
    @staticmethod
    def decode_cqcode(text: str) -> MessageSegment:
        items = text[1:-1].split(',')
        data = [x.split('=', 1) for x in items[1:]]
        data = dict([(x[0], x[1]) if len(x) > 1 else (x[0], '') for x in data])
        return MessageSegment(type=items[0][3:], data=data)

    @staticmethod
    def text_message_segment(text) -> MessageSegment:
        msg = MessageSegment('text')
        msg.data = {'text': text}
        return msg

    @classmethod
    def cq_text_decode(cls, message: Message) -> Message:
        result = Message()
        for msg in message:
            if msg.type != 'text':
                result += msg
            elif '[CQ:' not in (text := msg.data.get('text', '')):
                result += msg
            else:
                text_start_index = 0
                while True:
                    start_index = text.find('[CQ:', text_start_index)
                    end_index = text.find(']', start_index)
                    while True:
                        if '[CQ:' in text[start_index + 2:end_index]:
                            start_index = text.find('[CQ:', start_index + 2)
                        else:
                            break
                    if start_index == -1 or end_index == -1:
                        result += cls.text_message_segment(text[text_start_index:])
                        break
                    if text_start_index != start_index:
                        result += cls.text_message_segment(text[text_start_index:start_index])
                    result += cls.decode_cqcode(text[start_index:end_index + 1])
                    text_start_index = end_index + 1
        return result


if __name__ == '__main__':
    m = MessageSegment('text')
    m.data = {'text': '[CQ:abc[CQ:at,qq=123456]123[CQ:at,qq=123456][CQ:at,qq=565465]'}
    # m.data = {'text': 'aaa[CQ:at,qq=3635055279]1'}
    a = Tools.cq_text_decode(Message(m))
    b = Message(m)
    print(Tools.cq_text_decode(Message(m)).__repr__())
