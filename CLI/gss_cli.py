from ..Core import core as mycore
import argparse


# Preparing the parser
def prs():
    parser = argparse.ArgumentParser()
    parser.add_argument("-u", "--url", required=True, help="Specify URL search url you want to scrape ")
    parser.add_argument("-n", "--name", required=False, help="The file name you wish to save the result in")

    return parser.parse_args()


# The main
if __name__ == '__main__':
    args = prs()
    filename = "result"

    if not args.name:
        print("\n the results will be saved as 'result.json' .\n")

    search_url = args.url

    mycore.convert_2_json(mycore.scrape_all_pages(search_url), filename)
