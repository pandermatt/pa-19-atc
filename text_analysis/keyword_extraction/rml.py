from verbalexpressions import VerEx


class RML:
    def __init__(self):
        self.expression = VerEx()
        self.match_result = None

    def start_of_line(self):
        self.expression = self.expression.start_of_line()
        return self

    def add(self, expression):
        self.expression.add(expression)
        return self

    def find(self, group_name, expression: VerEx):
        self.expression = self.expression.add(f'(?P<{group_name}>{expression.source()})')
        return self

    def maybe_anything(self):
        self.expression = self.expression.add('(.*?)')
        return self

    def maybe(self, group_name, expression: VerEx):
        self.expression = self.expression.add(f'(?P<{group_name}>{expression.source()})')
        return self

    def alternatively(self, expression):
        self.expression.add(f'|{expression.source()}')
        return self

    def end_of_line(self):
        self.expression = self.expression.end_of_line()
        return self

    def source(self):
        return self.expression.source()

    def regex(self):
        return self.expression.regex()

    def match(self, string):
        self.match_result = self.expression.regex().match(string)
        return self.match_result
