from dataclasses import dataclass
from typing import ClassVar


@dataclass(frozen=True)
class NodeMeta:
    category: str
    description: str = ""



class Node:
    name: ClassVar[str]
    meta: ClassVar[NodeMeta]

