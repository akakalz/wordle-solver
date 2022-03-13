FROM python:3.9 as base

WORKDIR /src
COPY ./requirements.txt ./
RUN pip install -r requirements.txt

FROM base as tester
COPY ./test-requirements.txt ./
RUN pip install -r test-requirements.txt
COPY ./tests/ /src/tests/
COPY ./src ./

ENTRYPOINT [ "/src/tests/run_tests.sh" ]


FROM base as builder
COPY ./src ./

ENTRYPOINT [ "python", "app.py" ]
