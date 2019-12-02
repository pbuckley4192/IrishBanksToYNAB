#!/bin/bash
docker build -t bank_parser:latest .
docker run -d -p 8080:5000 --name bank_parser --restart=always bank_parser