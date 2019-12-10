FROM python:3.7-alpine


RUN mkdir ServerChan
COPY ServerChan ServerChan
RUN apk add --no-cache gcc libffi-dev libc-dev \
            python-dev linux-headers openssl-dev