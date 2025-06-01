import titlerepeat as tp

def main():
    csv_path = "data/amazon_books_1995_2024_top10.csv"
    # csv_path = "data/amazon_books_1995_2024_top100.csv"
    tp.plot_repeated_titles(csv_path)

if __name__ == "__main__":
    main()
