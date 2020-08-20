**Course:** CSE 6581 (Soft Error Tolerance) Khulna University of Engineering and Technology

# Introduction

Implemented for all possible combination of data-word for both single and double error detection and correction.

**IEEE Journal Name:** Unequal-Error-Protection Error Correction Codes for the Embedded Memories in Digital Signal Processors 

# Getting Stated

## Setup Environment

Install Python3 and PIP and then within project root directory
 
    pip install -r requirements.txt
    
## Execute

    python main.py

# Execution Result

## Environment

- Processor: Core i5 10th Gen 1035G1
- Memory: 8GB 
- Python: 3.8

## Output

**DataWord Size:** 32bit

| Error Type | Corrected | Failed | Percentage Corrected | Average Time |
| ---------- | --------- | ------ | -------------------- | ------------ |
| **Single Error** | 32 | 0 | 100.0 | 0.09372830390930176 ms |
| **Double Error** | 360 | 168 | 0.6818181818181818 | 0.15723795601815888 ms |

# Reference

- https://ieeexplore.ieee.org/document/7334457/
