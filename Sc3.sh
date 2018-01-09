#!/bin/bash

((python3 scriptplay.py 1 2) || : ) && 
((python3 scriptplay.py 2 2) || : ) && 
((python3 scriptplay.py 2 3) || : ) && 
((python3 scriptplay.py 4 0) || : )
