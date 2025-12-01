# Otto TTS API

基于 FastAPI 的电棍活字印刷术 TTS 后端。

## 项目结构

```
.
├── app/
│   ├── api/            # API 路由
│   ├── core/           # 核心 TTS 逻辑
│   ├── models/         # 数据模型
│   └── main.py         # FastAPI 应用入口
├── data/               # 数据文件 (字典, 配置, 音频源)
├── requirements.txt    # 依赖列表
└── run.sh              # 启动脚本
```

## 安装依赖

```bash
pip install -r requirements.txt
```

## 运行

```bash
uv run uvicorn app.main:app --reload
```
或者使用脚本：
```bash
./run.sh
```

## API 文档

启动服务后，访问 `http://localhost:8000/docs` 查看交互式 API 文档。

### 生成音频

**POST** `/api/v1/generate`

Request Body:
```json
{
  "text": "我是你跌",
  "inYsddMode": true,
  "pitchMult": 1.0,
  "speedMult": 1.0,
  "reverse": false,
  "norm": false
}
```

Response: Audio file (WAV)
