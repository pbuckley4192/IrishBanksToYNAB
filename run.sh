#!/bin/bash
docker stop bank_parser
docker rm bank_parser
docker build -t bank_parser:latest .
docker run -d -p 8080:5000 --name bank_parser --restart=always bank_parser