# Entropy Donuts

## Generating Data

To generate data, run `main.py` and be careful about the degree you specify for the polynomial. Degree `24` shown in this example consumes over 128GB of memory. The batch size (`-b`) and worker count (`-w`) will also rely on the available system memory/threads you have on your system. Use `-f` to specify the output file to save the data to.

```sh
python main.py -b 100000 -w 32 -d 24 -f roots_24.npy
```

## Generating Plot

To generate the plot, use `plot.py` and specify the data file (generated in the previous step), the size with `-s` in pixels, and the output image.

```sh
python plot.py roots_24.npy -s 20000 -o beauty_of_roots_large.png
```
