#!/bin/bash

((python3 scriptplay.py 2 4) || : ) && 
((python3 scriptplay.py 4 4) || : ) && 
((python3 scriptplay.py 4 5) || : ) && 
((python3 scriptplay.py 3 0) || : )
