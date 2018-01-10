#!/bin/bash

((python3 scriptplay.py 1 1) || : ) && 
((python3 scriptplay.py 4 3) || : ) && 
((python3 scriptplay.py 4 2) || : ) && 
((python3 scriptplay.py 3 5) || : )
