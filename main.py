import uvicorn
from fastapi import FastAPI
from starlette.responses import HTMLResponse, JSONResponse


class imports(FastAPI):
    def __init__(self, **extra):
        super().__init__(**extra)

        self.add_api_route("/", self.get_root, methods=["GET"], include_in_schema=False)
        self.add_api_route("/version", self.get_version, methods=["GET"])

    @staticmethod
    async def get_root() -> HTMLResponse:
        return HTMLResponse('<meta http-equiv="Refresh" content="0; url=\'/docs\'" />')

    async def get_version(self) -> JSONResponse:
        return JSONResponse({"FastAPI version": self.version})


if __name__ == "__main__":
    url = "/"
    app = imports(
        title="Распознавания форм",
        description=f"Source: <a href='{docs}'>Stack Overflow</a>",
    )
    uvicorn.run(app, host="127.0.0.1", port=8000)

