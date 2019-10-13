#!/bin/bash
docker build -t boi_parser:latest .
docker run -d -p 8080:5000 --name boi_parser --restart=always boi_parser