from pydantic import BaseModel


class CreateTaskResponseResult(BaseModel):
    task_id: str
    task_token: str


class CreateTaskResponse(BaseModel):
    qid: str
    result: CreateTaskResponseResult


class AddChunkResponseResult(BaseModel):
    text: str


class AddChunkResponse(BaseModel):
    qid: str
    result: AddChunkResponseResult


class ResultResultResponse(BaseModel):
    text: str
    status: str


class ResultResponse(BaseModel):
    qid: str
    result: ResultResultResponse
