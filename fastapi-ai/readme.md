启动
```
uvicorn main:app --host=127.0.0.1 --port=8010 --reload
```

debug
```
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python Debugger: FastAPI",
      "type": "debugpy",        
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "main:app",
        "--host", "127.0.0.1",
        "--port", "8000"
        // 注意：调试时建议先移除 "--reload"
      ],
      "jinja": true,
      "justMyCode": false,
      "env": {
        "PYTHONPATH": "${workspaceFolder}" 
      }     
    }
  ]
}
```