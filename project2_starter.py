# SI 201 HW4 (Library Checkout System)
# Your name: Peixi Shi 
# Your student id: 34338917
# Your email: peixishi@umich.edu
# Who or what you worked with on this homework (including generative AI like ChatGPT): myself
# If you worked with generative AI also add a statement for how you used it.
# e.g.:
# Asked ChatGPT for hints on debugging and for suggestions on overall code structure
#
# Did your use of GenAI on this assignment align with your goals and guidelines in your Gen AI contract? If not, why?
#
# --- ARGUMENTS & EXPECTED RETURN VALUES PROVIDED --- #
# --- SEE INSTRUCTIONS FOR FULL DETAILS ON METHOD IMPLEMENTATION --- #

from bs4 import BeautifulSoup
import re
import os
import csv
import unittest
import requests  # kept for extra credit parity


# IMPORTANT NOTE:
"""
If you are getting "encoding errors" while trying to open, read, or write from a file, add the following argument to any of your open() functions:
    encoding="utf-8-sig"
"""


def load_listing_results(html_path) -> list[tuple]:
    """
    Load file data from html_path and parse through it to find listing titles and listing ids.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples containing (listing_title, listing_id)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    with open(html_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f, "html.parser")

    results = []
    seen_ids = set()

    listing_titles = soup.find_all(attrs={"data-testid": "listing-card-title"})

    for title_tag in listing_titles:
        listing_title = title_tag.get_text(strip=True)

        parent = title_tag.find_parent(attrs={"data-testid": "card-container"})
        if parent is None:
            continue

        link_tag = parent.find("a", href=True)
        if link_tag is None:
            continue

        match = re.search(r"/rooms/(\d+)", link_tag["href"])
        if match is None:
            continue

        listing_id = match.group(1)

        if listing_id not in seen_ids:
            results.append((listing_title, listing_id))
            seen_ids.add(listing_id)

    return results
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def get_listing_details(listing_id) -> dict:
    """
    Parse through listing_<id>.html to extract listing details.

    Args:
        listing_id (str): The listing id of the Airbnb listing

    Returns:
        dict: Nested dictionary in the format:
        {
            "<listing_id>": {
                "policy_number": str,
                "host_type": str,
                "host_name": str,
                "room_type": str,
                "location_rating": float
            }
        }
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    base_dir = os.path.abspath(os.path.dirname(__file__))
    file_path = os.path.join(base_dir, "html_files", f"listing_{listing_id}.html")

    with open(file_path, "r", encoding="utf-8-sig") as f:
        soup = BeautifulSoup(f, "html.parser")

    page_text = soup.get_text(" ", strip=True)

    policy_number = "Pending"
    host_type = "regular"
    host_name = ""
    room_type = "Entire Room"
    location_rating = 0.0

    if "Superhost" in page_text:
        host_type = "Superhost"

    host_tag = soup.find("div", string=re.compile(r"Hosted by"))
    if host_tag is not None:
        host_text = host_tag.get_text(strip=True)
        host_name = host_text.replace("Hosted by ", "").strip()

    subtitle_tag = soup.find(string=re.compile(r"(Entire|Private|Shared)"))
    subtitle_text = ""
    if subtitle_tag is not None:
        subtitle_text = str(subtitle_tag)

    if "Private" in subtitle_text:
        room_type = "Private Room"
    elif "Shared" in subtitle_text:
        room_type = "Shared Room"
    else:
        room_type = "Entire Room"

    all_text = soup.get_text("\n", strip=True)
    location_match = re.search(r"Location\s*([0-9]\.[0-9])", all_text)
    if location_match:
        location_rating = float(location_match.group(1))

    policy_match = re.search(r"Policy number\s*([A-Za-z0-9\-]+|Pending|Exempt)", all_text, re.IGNORECASE)
    if policy_match:
        raw_policy = policy_match.group(1).strip()
        if raw_policy.lower() == "pending":
            policy_number = "Pending"
        elif raw_policy.lower() == "exempt":
            policy_number = "Exempt"
        else:
            policy_number = raw_policy

    return {
        listing_id: {
            "policy_number": policy_number,
            "host_type": host_type,
            "host_name": host_name,
            "room_type": room_type,
            "location_rating": location_rating
        }
    }

    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def create_listing_database(html_path) -> list[tuple]:
    """
    Use prior functions to gather all necessary information and create a database of listings.

    Args:
        html_path (str): The path to the HTML file containing the search results

    Returns:
        list[tuple]: A list of tuples. Each tuple contains:
        (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    listing_results = load_listing_results(html_path)
    database = []

    for listing_title, listing_id in listing_results:
        details = get_listing_details(listing_id)[listing_id]

        row = (
            listing_title,
            listing_id,
            details["policy_number"],
            details["host_type"],
            details["host_name"],
            details["room_type"],
            details["location_rating"]
        )

        database.append(row)

    return database
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def output_csv(data, filename) -> None:
    """
    Write data to a CSV file with the provided filename.

    Sort by Location Rating (descending).

    Args:
        data (list[tuple]): A list of tuples containing listing information
        filename (str): The name of the CSV file to be created and saved to

    Returns:
        None
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    sorted_data = sorted(data, key=lambda x: x[6], reverse=True)
    with open(filename, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)

        writer.writerow([
            "listing_title",
            "listing_id",
            "policy_number",
            "host_type",
            "host_name",
            "room_type",
            "location_rating"
        ])

        for row in sorted_data:
            writer.writerow(row)
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def avg_location_rating_by_room_type(data) -> dict:
    """
    Calculate the average location_rating for each room_type.

    Excludes rows where location_rating == 0.0 (meaning the rating
    could not be found in the HTML).

    Args:
        data (list[tuple]): The list returned by create_listing_database()

    Returns:
        dict: {room_type: average_location_rating}
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    ratings = {}

    for row in data:
        room_type = row[5]
        location_rating = row[6]

        if location_rating == 0.0:
            continue

        if room_type not in ratings:
            ratings[room_type] = []

        ratings[room_type].append(location_rating)

    avg_dict = {}
    for room_type in ratings:
        avg = sum(ratings[room_type]) / len(ratings[room_type])
        avg_dict[room_type] = round(avg, 1)

    return avg_dict
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


def validate_policy_numbers(data) -> list[str]:
    """
    Validate policy_number format for each listing in data.
    Ignore "Pending" and "Exempt" listings.

    Args:
        data (list[tuple]): A list of tuples returned by create_listing_database()

    Returns:
        list[str]: A list of listing_id values whose policy numbers do NOT match the valid format
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    invalid_listings = []

    for row in data:
        listing_id = row[1]
        policy_number = row[2]

        if policy_number in ["Pending", "Exempt"]:
            continue

        if not re.fullmatch(r"STR-\d+", policy_number):
            invalid_listings.append(listing_id)

    return invalid_listings
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


# EXTRA CREDIT
def google_scholar_searcher(query):
    """
    EXTRA CREDIT

    Args:
        query (str): The search query to be used on Google Scholar
    Returns:
        List of titles on the first page (list)
    """
    # TODO: Implement checkout logic following the instructions
    # ==============================
    # YOUR CODE STARTS HERE
    # ==============================
    url = "https://scholar.google.com/scholar"

    params = {
        "q": query
    }

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, params=params, headers=headers)

    soup = BeautifulSoup(response.text, "html.parser")

    titles = []

    for item in soup.find_all("h3", class_="gs_rt"):
        title = item.get_text(strip=True)
        if title:
            titles.append(title)

    return titles
    # ==============================
    # ==============================
    # YOUR CODE ENDS HERE
    # ==============================


class TestCases(unittest.TestCase):
    def setUp(self):
        self.base_dir = os.path.abspath(os.path.dirname(__file__))
        self.search_results_path = os.path.join(self.base_dir, "html_files", "search_results.html")

        self.listings = load_listing_results(self.search_results_path)
        self.detailed_data = create_listing_database(self.search_results_path)

    def test_load_listing_results(self):
        # TODO: Check that the number of listings extracted is 18.
        self.assertEqual(len(self.listings), 18)
        # TODO: Check that the FIRST (title, id) tuple is  ("Loft in Mission District", "1944564").
        self.assertEqual(self.listings[0], ("Loft in Mission District", "1944564"))

    def test_get_listing_details(self):
        html_list = ["467507", "1550913", "1944564", "4614763", "6092596"]

        # TODO: Call get_listing_details() on each listing id above and save results in a list.
        results = []
        for listing_id in html_list:
            results.append(get_listing_details(listing_id))

        # TODO: Spot-check a few known values by opening the corresponding listing_<id>.html files.
        # 1) Check that listing 467507 has the correct policy number "STR-0005349".
        # 2) Check that listing 1944564 has the correct host type "Superhost" and room type "Entire Room".
        # 3) Check that listing 1944564 has the correct location rating 4.9.
        self.assertEqual(
            results[0]["467507"]["policy_number"],
            "STR-0005349"
        )

        self.assertEqual(
            results[2]["1944564"]["host_type"],
            "Superhost"
        )
        self.assertEqual(
            results[2]["1944564"]["room_type"],
            "Entire Room"
        )

        self.assertAlmostEqual(
            results[2]["1944564"]["location_rating"],
            4.9
        )

    def test_create_listing_database(self):
        # TODO: Check that each tuple in detailed_data has exactly 7 elements:
        # (listing_title, listing_id, policy_number, host_type, host_name, room_type, location_rating)
        for row in self.detailed_data:
            self.assertEqual(len(row), 7)

        # TODO: Spot-check the LAST tuple is ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8).
        self.assertEqual(
            self.detailed_data[-1],
            ("Guest suite in Mission District", "467507", "STR-0005349", "Superhost", "Jennifer", "Entire Room", 4.8)
    )

    def test_output_csv(self):
        out_path = os.path.join(self.base_dir, "test.csv")

        # TODO: Call output_csv() to write the detailed_data to a CSV file.
        # TODO: Read the CSV back in and store rows in a list.
        # TODO: Check that the first data row matches ["Guesthouse in San Francisco", "49591060", "STR-0000253", "Superhost", "Ingrid", "Entire Room", "5.0"].

        os.remove(out_path)

    def test_avg_location_rating_by_room_type(self):
        # TODO: Call avg_location_rating_by_room_type() and save the output.
        # TODO: Check that the average for "Private Room" is 4.9.
        pass

    def test_validate_policy_numbers(self):
        # TODO: Call validate_policy_numbers() on detailed_data and save the result into a variable invalid_listings.
        # TODO: Check that the list contains exactly "16204265" for this dataset.
        pass


def main():
    detailed_data = create_listing_database(os.path.join("html_files", "search_results.html"))
    output_csv(detailed_data, "airbnb_dataset.csv")


if __name__ == "__main__":
    main()
    unittest.main(verbosity=2)