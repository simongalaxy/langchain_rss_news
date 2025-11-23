import sqlite3
import os
from sqlmodel import SQLModel, Field, create_engine, Session, select


# define a SQLModel table.
class RSSItem(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    title: str
    link: str
    content: str
    newsId: str
    publish_date: str
    publish_date_text: str
    
class SQLiteDBHandler:
    def __init__(self, db_path: str, db_filename: str):
        self.engine = create_engine(f"sqlite:///{os.path.join(db_path, db_filename)}")
        SQLModel.metadata.create_all(self.engine)

    def add_rss_item(self, item: RSSItem):
        with Session(self.engine) as session:
            session.add(item)
            session.commit()
        

    def get_rss_items(self, keyword: str = None):
        with Session(self.engine) as session:
            statement = select(RSSItem).where(RSSItem.content.contains(keyword))
            results = session.exec(statement)
            return results.all()
