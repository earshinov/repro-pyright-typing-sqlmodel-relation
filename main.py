from typing import Optional, cast
from sqlalchemy.engine import Engine
from sqlmodel import SQLModel, Field, create_engine, Session, select, Relationship  # pyright: ignore[reportUnknownVariableType]


class AssetCollection(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    assets: list["Asset"] = Relationship(back_populates="collection")


class Asset(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    url: str
    collection_id: Optional[int] = Field(default=None, foreign_key="assetcollection.id")
    collection: AssetCollection = Relationship(back_populates="assets")


def main():
    engine = init_memory_db()
    write_asset(engine=engine)
    read_asset(engine=engine)


def init_memory_db() -> Engine:
    engine = create_engine("sqlite:///:memory:")
    SQLModel.metadata.create_all(engine)
    return engine


def write_asset(*, engine: Engine):
    collection = AssetCollection(name="My Collection")
    asset = Asset(name="My Asset", url="https://example.com", collection=collection)
    with Session(engine) as session:
        session.add(collection)  # pyright: ignore[reportUnknownMemberType]
        session.add(asset)  # pyright: ignore[reportUnknownMemberType]
        session.commit()


def read_asset(*, engine: Engine):
    with Session(engine) as session:
        statement = select(Asset)
        asset = cast(Asset, session.exec(statement).first())  # pyright: ignore[reportUnknownMemberType]
        # 👇 [pyright] Type of "collection" is unknown
        print(f"Got asset {asset.name!r} from collection {asset.collection.name!r}")
        # 👇 Same goes for the `Asset.collection` class field, even though it is explicitly declared to be of type `AssetCollection`
        _collection_field = Asset.collection


if __name__ == "__main__":
    main()
