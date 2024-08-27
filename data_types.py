class TestCase:
    # __slots__ = ('title', 'step', 'result', 'stepn')

    def __init__(self, title, step, result, stepn=1):
        self.title = title
        self.step = step
        self.result = result
        self.stepn = stepn
