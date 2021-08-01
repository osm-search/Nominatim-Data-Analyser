from analyser.database.connection import connect

def test_connect() -> None:
    with connect() as conn:
        assert conn.status == 1