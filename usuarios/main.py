import sys
import uvicorn

from pathlib import Path

from constructors.app_constructor import app_constructor

current_dir = Path(__file__).resolve().parent
sys.path.append(str(current_dir))


app = app_constructor()


if __name__ == '__main__':
    uvicorn.run("main:app", host="0.0.0.0", reload=True, port=8001)