import pandas as pd

try:
    # Load predictions CSV
    df = pd.read_csv("predictions.csv")

    # Ensure 'prediction' column exists
    if "prediction" not in df.columns:
        raise ValueError("CSV does not contain a 'prediction' column.")

    # Fill missing or NaN predictions with default category
    df["prediction"] = df["prediction"].fillna("Result Not Published").astype(str)

    # Normalize text
    df["prediction"] = df["prediction"].str.strip().str.title()

    # Count occurrences of each category
    category_counts = df["prediction"].value_counts()

    # Total posts (ensure integer, fallback to 0)
    total_posts = len(df) if df is not None else 0

    # Safely get counts, fallback to 0 if missing or None
    qualified_count = category_counts.get("Qualified") or 0
    not_qualified_count = category_counts.get("Not Qualified") or 0
    result_not_published_count = category_counts.get("Result Not Published") or 0

    # Calculate percentages safely
    qualified_pct = (qualified_count / total_posts * 100) if total_posts > 0 else 0
    not_qualified_pct = (
        (not_qualified_count / total_posts * 100) if total_posts > 0 else 0
    )
    result_not_published_pct = (
        (result_not_published_count / total_posts * 100) if total_posts > 0 else 0
    )

    # Print summary
    print(f"Total Posts: {total_posts}")
    print(f"Qualified: {qualified_count} ({qualified_pct:.2f}%)")
    print(f"Not Qualified: {not_qualified_count} ({not_qualified_pct:.2f}%)")
    print(
        f"Result Not Published: {result_not_published_count} ({result_not_published_pct:.2f}%)"
    )

except FileNotFoundError:
    print("[-] predictions.csv file not found.")
except pd.errors.EmptyDataError:
    print("[-] predictions.csv is empty.")
except Exception as e:
    print(f"[-] An error occurred: {e}")
