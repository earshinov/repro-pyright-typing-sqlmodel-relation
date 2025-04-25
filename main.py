# pyright: strict
from sqlmodel import SQLModel


class A(SQLModel):
    a: str


class B(SQLModel):
    b: A


def func(m: B):
    reveal_type(m.b)
