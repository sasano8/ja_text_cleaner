class Normalizer(str):
    default = ""

    def __new__(cls, v: object = ""):
        if v is None:
            v = cls.default

        if v is None:
            return None

        if not isinstance(v, str):
            v = str(v)

        v = cls.process(v)
        return str.__new__(cls, v)

    @classmethod
    def process(cls, v: str):
        return v

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        return cls(v)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({super().__repr__()})"


class Finalizer(str):
    default = ""
    pipe = []

    def __new__(cls, v: object = ""):
        if v is None:
            v = cls.default

        if v is None:
            return None

        if not isinstance(v, str):
            v = str(v)

        v = cls.process(v)

        return str.__new__(cls, v)

    @classmethod
    def process(cls, v: str):

        for processor in cls.pipe:
            v = processor(v.__str__())  # cythonなどを利用していると継承されたstrを使用できない
        return v

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v: str):
        return cls(v)

    def __repr__(self):
        cls = self.__class__.__name__
        return f"{cls}({super().__repr__()})"
