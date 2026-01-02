import numpy as np
from itertools import product
from tqdm import tqdm
from argparse import ArgumentParser
from concurrent.futures import ProcessPoolExecutor, as_completed

def compute_roots(poly):
    """Compute roots of a single polynomial."""
    return np.roots(poly)

def compute_roots_batch(batch):
    """Compute roots for a batch of polynomials."""
    return [np.roots(poly) for poly in batch]

def batch_generator(iterable, batch_size):
    """Yield successive batches from iterable."""
    for i in range(0, len(iterable), batch_size):
        yield iterable[i:i + batch_size]

def save_roots(degree, datafile, batch_size=10000, workers=None):
    n_terms = degree + 1
    total_polys = 2**n_terms
    roots = np.zeros((total_polys, degree), dtype=complex)

    # Generate the polynomials (keep your original slice logic)
    all_polys = list(product(*([[-1, 1]] * n_terms)[:total_polys // 2]))

    # Parallel batch processing
    batches = list(batch_generator(all_polys, batch_size))
    idx = 0
    with ProcessPoolExecutor(max_workers=workers) as executor:
        futures = [executor.submit(compute_roots_batch, batch) for batch in batches]
        for future in tqdm(as_completed(futures), total=len(futures), unit='batch'):
            batch_roots = future.result()
            for r in batch_roots:
                roots[idx] = r
                idx += 1

    # Save to file
    with open(datafile, 'wb') as f:
        np.save(f, roots.ravel())
    print(f"Saved {idx} roots to {datafile}")

def main():
    parser = ArgumentParser()
    parser.add_argument('-d', type=int, default=18,
                        help='polynomial degree')
    parser.add_argument('-f', type=str, default='data_test.npy',
                        help='output filename')
    parser.add_argument('-b', type=int, default=10000,
                        help='batch size for parallel processing')
    parser.add_argument('-w', type=int, default=None,
                        help='number of parallel workers')
    args = parser.parse_args()

    save_roots(args.d, args.f, batch_size=args.b, workers=args.w)


if __name__ == '__main__':
    main()
