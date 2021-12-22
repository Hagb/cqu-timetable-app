from typing import Optional, List
import dataclasses
import pickle
from . import app
from requests import session, Session
from mycqu.user import User


@dataclasses.dataclass
class Record():
    username: str = ""
    password: str = ""
    user_info: Optional[User] = None
    session: Session = dataclasses.field(default_factory=session)
    event_ids: List[int] = dataclasses.field(default_factory=list)

    @classmethod
    def read(record_class) -> "Record":
        path = app.data_path.joinpath("data.pickle")
        if path.exists():
            with open(path, 'br') as file:
                return record_class(**dataclasses.asdict(pickle.load(file)))
        return record_class()

    def write(self) -> None:
        app.data_path.mkdir(parents=True, exist_ok=True)
        with open(app.data_path.joinpath("data.pickle"), 'bw') as file:
            pickle.dump(self, file)
