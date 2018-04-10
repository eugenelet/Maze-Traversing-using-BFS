# Maze-Traversing-using-BFS

This project is designed solely for the Midterm Project of Integrated Circuit Laboratory (2018 Spring) of NCTU.

This is an implementation of Breath-First-Search on a generated maze. There'll be prizes in the maze which has to be collected in order to complete the game as shown below.

![Orig](https://github.com/eugenelet/Maze-Traversing-using-BFS/blob/master/demo.jpg)

To run this project, install all the required packages:
```
$ pip install -r requirements.txt
```

There are 3 files in this project:

`play.py` is the implementation of BFS which is used to solve the maze. Add arguement `--vis` to see how is the game played using BFS.

`test.py` is for users to test out the maze using their keyboards.

`generate.py` is used for generating new maze. `--vis` to see how is the maze contructed. `--vis2` to see the end results of the constructed maze. (will be released after assignment deadline)
