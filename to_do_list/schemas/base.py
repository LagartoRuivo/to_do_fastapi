from pydantic import BaseModel


class Message(BaseModel):
    message: str


class CustomBaseModel(BaseModel):
    def dict(self, *args, **kwargs):
        d = super().dict(*args, **kwargs)
        d = {k: v for k, v in d.items() if v is not None}
        return d
