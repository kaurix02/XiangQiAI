#!/bin/bash

((python3 scriptplay.py 3 3) || : ) && 
((python3 scriptplay.py 3 2) || : ) && 
((python3 scriptplay.py 1 3) || : ) && 
((python3 scriptplay.py 3 4) || : )
