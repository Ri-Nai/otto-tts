from pydantic import BaseModel, Field

class TTSRequest(BaseModel):
    text: str = Field(..., description="要输出的文字")
    inYsddMode: bool = Field(True, description="匹配到特定文字时使用原声大碟")
    pitchMult: float = Field(1.0, description="音调偏移程度，大于1升高音调，小于1降低音调，建议[0.5, 2]")
    speedMult: float = Field(1.0, description="播放速度，大于1加速，小于1减速，建议[0.5, 2]")
    reverse: bool = Field(False, description="频音的成生放倒")
    norm: bool = Field(False, description="统一所有字音量")
