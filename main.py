import datavisualization as dv

def main():
    csv_path = "amazon_books_1995_2024_top10.csv"
    dv.avg_price_by_year(csv_path)
    dv.plot_avg_rating_trend(csv_path)
    dv.plot_repeated_authors(csv_path)
    dv.plot_author_repetition_donut(csv_path)
    dv.plot_repeated_titles(csv_path)
    dv.plot_title_repetition_donut(csv_path)
    dv.plot_format_pie(csv_path)

if __name__ == "__main__":
    main()
