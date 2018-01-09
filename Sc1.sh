#!/bin/bash

((python3 scriptplay.py 0 3) || : ) && 
((python3 scriptplay.py 0 4) || : ) && 
((python3 scriptplay.py 0 5) || : ) && 
((python3 scriptplay.py 1 4) || : ) && 
((python3 scriptplay.py 1 3) || : )
