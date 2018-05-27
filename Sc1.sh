#!/bin/bash

((python3 scriptplay.py 4 5) || : ) &&
((python3 scriptplay.py 5 4) || : ) &&
((python3 scriptplay.py 4 0) || : ) && 
((python3 scriptplay.py 4 1) || : ) && 
((python3 scriptplay.py 4 2) || : ) && 
((python3 scriptplay.py 4 3) || : )
