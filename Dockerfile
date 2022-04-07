from python:3.8

WORKDIR /app
COPY csrf_attacker.py /app/app.py
COPY csrf_attacker.html /app/index.html

RUN pip install -i https://pypi.tuna.tsinghua.edu.cn/simple flask
EXPOSE 8000

CMD ["python" "./app.py"]


