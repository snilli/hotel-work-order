from typing import Generic, List, Tuple, TypeVar

T = TypeVar("T")


class BaseStatus(Generic[T]):
    exclude_key = [
        'values',
        'tuples',
        'get_attribute',
        'exclude_key',
        'name',
    ]

    @classmethod
    def tuples(cls) -> List[Tuple[T, str]]:
        return [
            (getattr(cls, attr), attr) for attr in dir(cls) if not attr.startswith('_') and attr not in cls.exclude_key
        ]

    @classmethod
    def values(cls) -> List[T]:
        return [getattr(cls, attr) for attr in dir(cls) if not attr.startswith('_') and attr not in cls.exclude_key]

    @classmethod
    def get_attribute(cls, attribute_name: str) -> T:
        return getattr(cls, attribute_name)
