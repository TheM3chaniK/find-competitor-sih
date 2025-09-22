from ai import AI
import sys
from scrapper import Scrapper
import pandas as pd

model = AI()


def save_results(results, filename="predictions.csv"):
    if results:
        df = pd.DataFrame(results)
        df.to_csv(filename, index=False, encoding="utf-8")
        print(f"[+] Predictions saved to {filename}")
    else:
        print("[-] No results to save.")


def main():
    print("[+] Scrapper Process Started")
    results = []

    try:
        scraper = Scrapper()
        scraper.login()
        scraper.search()
        captions = scraper.scrap()
        del scraper
        print("[+] Scrapping Successful")

        print("\n[+] Sending captions to the model....")

        for item in captions:
            try:
                username = item["username"]
                caption = item["caption"]

                # send caption to model and get prediction
                prediction = model.get_prdiction(caption)

                results.append(
                    {"username": username, "caption": caption, "prediction": prediction}
                )
                print(f"[+] {username}: {prediction}")

            except Exception as e:
                print(f"[-] Error processing caption: {e}")
                continue  # skip this caption and continue

        print("[+] All predictions done!")
        save_results(results)

    except KeyboardInterrupt:
        print("\n[!] KeyboardInterrupt detected. Saving progress...")
        save_results(results)
        sys.exit(0)

    except Exception as e:
        print(f"[-] Oops something went wrong. Error: {e}")
        save_results(results)
        sys.exit(1)


if __name__ == "__main__":
    main()
