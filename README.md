# dpDebugger
Visual debugger for the Dining Philosophers simulation.

Save an output of your program into this directory as `log.txt` and boot up the Tkinter tool for it to work. You can adjust how quickly frames pass through the animation with an entry widget. Might add more to this later.

In order for this to work, your output has to include single lines that display nothing but the state of the `chops[]` array; i.e., lines like `[-1, 1, 2]` that indicate that each philosopher has their left chopstick aside from philosopher 0 (assuming `-1` denotes a `NONE` state).

A workable example output looks like the following, where lines like `[-1, -1, -1]` allow dpDebugger to do its job:

```
$ mpic++ dp.cpp -o dp; mpirun -np 4 ./dp
P0: thinking
P1: thinking
P2: thinking
P0: picking up left
0 asks for left
-1 -1 -1 
L: assigning 0 to chop[0]
-1 -1 -1 

0 -1 -1 
P2: picking up left
2 asks for left
0 -1 -1 
L: assigning 2 to chop[2]
0 -1 -1 

0 -1 2 
P1: picking up left
1 asks for left
0 -1 2 
L: assigning 1 to chop[1]
0 -1 2 
```
