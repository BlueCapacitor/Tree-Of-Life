# Tree of Life
This project computes and visually displays evolutionary relationships between organisms in a phylogenetic tree of life.
This is my school science fair project. For more information, here is [my poster](https://docs.google.com/presentation/d/1ZFbB2NnCSu-uEfBxhHiZNMwZ4gwRRBCNIpv-P3tdPbo/edit?usp=sharing).

## Running the program
The program takes the input from a csv file called `TestProteins.csv`. This file should be formatted with species per line and each line formatted as:

    OrganismName,DNA(proteins),Classification

Note that there are no quotes and no spaces after commas. The classification is used to color the phylogenetic tree. All of the classifications should be in the file named `Colors.csv`. This file should be similarly formatted:

    Classification,Color

To run the program, execute `Main.py` with python3:
> python3 Main.py

It will first ask you whether you want color enabled "*Color?:* ". Color only works on some terminals. Please answer `y` or `n`.

Because comparing all of the genes is a very time consuming step, once computed, the differences in the genes can be saved in `Differences.csv`. The program will ask you whether you want to use the differences in `Differences.csv`. If you want to use previously cached differences, answer `y`, otherwise answer `n`.

If you answered `no`, the program should now start calculating the difference table. When it is done, it will ask you if you want to save (or overwrite) the differences in `Differences.csv`.

Next, the program will ask you if you want it to display the difference table. This will take a long time and will not display properly if the table is too large. You can still view it in `Differences.csv` if you saved it there. The table may not display until you have finished the rest of these steps.

Lastly, the program will ask you if you want it to draw the phylogenetic tree of life. If you answer `y`, it will draw the tree in a new window. There should also be a small blank window.
To move the tree of life around, shift your computer's focus to that blank window. You should be able to move the tree with the arrow keys. You can also reset the view to the original position with the `r` key.

![image](https://user-images.githubusercontent.com/32907199/149603621-51d8fb4d-8eae-4888-a416-1dee7b9c3f8a.png)
