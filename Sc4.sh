#!/bin/bash

((python3 scriptplay.py 3 1) || : ) && 
((python3 scriptplay.py 4 1) || : ) && 
((python3 scriptplay.py 4 4) || : ) &&
((python3 scriptplay.py 2 1) || : )
