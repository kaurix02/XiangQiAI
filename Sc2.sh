#!/bin/bash

((python3 scriptplay.py 4 4) || : ) && 
((python3 scriptplay.py 6 4) || : )
