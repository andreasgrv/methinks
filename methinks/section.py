import re


class Section(object):
    """A section in a methinks journal entry"""
    def __init__(self):
        super().__init__()

    def propagate(self):
        raise NotImplementedError()

    @classmethod
    def from_text(self, text):
        """Propagate to next entry"""
        raise NotImplementedError()


class PersistentSection(Section):
    """A section that propagates along time unaltered"""
    def __init__(self, text):
        super().__init__()
        self.text = text

    def propagate(self):
        return self.text

    @classmethod
    def from_text(cl, text):
        return cl(text)


class VolatileSection(Section):
    """A section that drops its contents"""

    RE_TITLE_CONTENT = r'(?P<title>^#+.*?)\n(?P<content>.*)'

    def __init__(self, title, content):
        super().__init__()
        self.title = title
        self.content = content

    def propagate(self):
        return '%s\n' % self.title

    @classmethod
    def from_text(cl, text):
        regex = re.compile(cl.RE_TITLE_CONTENT, re.MULTILINE | re.DOTALL)
        match = next(regex.finditer(text))
        title, content = match['title'], match['content']
        return cl(title, content)


class TodosSection(Section):
    """A section including todos as [ ] style lists"""

    RE_TITLE_CONTENT = r'(?P<title>^#+.*?)\n(?P<content>.*)'
    RE_TODO = r'(?P<todo>\[ \].*?)(?=(\[ \]|\Z))'

    def __init__(self, title, todos):
        super().__init__()
        self.title = title
        self.todos = todos

    def propagate(self):
        todo_str = ''.join(self.todos)
        return '%s\n%s' % (self.title, todo_str)

    @classmethod
    def from_text(cl, text):
        regex = re.compile(cl.RE_TITLE_CONTENT, re.MULTILINE | re.DOTALL)
        match = next(regex.finditer(text))
        todo_regex = re.compile(cl.RE_TODO, re.MULTILINE | re.DOTALL)
        title, content = match['title'], match['content']
        todos = [m['todo'] for m in todo_regex.finditer(content)]
        return cl(title, todos)
