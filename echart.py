import requests
from bs4 import BeautifulSoup
import re

from sympy import print_rcode


def is_float(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def extract_chart_data(url):
    try:
        # Fetch the HTML content from the URL
        response = requests.get(url, timeout=10)
        response.raise_for_status()  # Ensure the request was successful
        soup = BeautifulSoup(response.text, 'html.parser')

        # Find all <script> tags
        script_tags = soup.find_all('script')
        matched_sections = []
        find1 = 0
        find2 = 2

        for script in script_tags:
            if script.string:  # Ensure the script has content
                # Check if the script contains an element ID like "TDGraph<number>"
                tdgraph_match = re.search(r'getElementById\("TDGraph(\d+)"\)', script.string)
                if tdgraph_match:
                    find2 = 0

        for script in script_tags:

            # Check if the script contains `var myCharta = echarts.init`
            if "var myCharta = echarts.init" in script.text:
                script_content = script.text

                # Check for the presence of `var data_date` and `var data_value`
                if "var data_date" in script_content and "var data_value" in script_content:
                    # Extract the values of data_date and data_value
                    title_match = re.search(r"var title\s*=\s*'(.*?)';", script_content)
                    date_match = re.search(r"var data_date\s*=\s*'(.*?)';", script_content)
                    value_match = re.search(r"var data_value\s*=\s*'(.*?)';", script_content)


                    if title_match and date_match and value_match:
                        title = title_match.group(1)
                        data_date_raw = date_match.group(1)
                        data_value_raw = value_match.group(1)

                        # Ensure both are non-empty
                        if data_date_raw and data_value_raw:
                            # Convert to lists
                            data_date = data_date_raw.split(',')
                            data_value = [float(v) if v.replace('.', '', 1).lstrip('-').isdigit() else None for v in data_value_raw.split(',')]

                            # matched_sections.append({
                            #     'script': script_content,
                            #     'data_date': data_date,
                            #     'data_value': data_value
                            # })

                            find1 = 1
                            # print(data_date)
                            # print(data_value)

            if script.string:  # Ensure the script has content
                # Check if the script contains an element ID like "TDGraph<number>"
                tdgraph_match = re.search(r'getElementById\("TDGraph(\d+)"\)', script.string)
                if tdgraph_match:
                    # Extract all "data" fields from the matched script
                    data_matches = re.findall(r'"data":\s*\[(.*?)\]', script.string, re.DOTALL)
                    if data_matches:
                        # Save data fields with the corresponding TDGraph ID
                        classes = data_matches[0].split(",")
                        classes = [item.strip('"') for item in classes]
                        # date = data_matches[3].split(',')
                        # date = [item.strip('"') for item in date]
                        # print(classes)
                        # print(data_matches[1])
                        data1 = [float(num) for num in data_matches[1].split(',')]
                        if is_float(data_matches[2].split(',')[0]):
                            data2 = [float(num) for num in data_matches[2].split(',')]
                        else:
                            data2 = []
                        # print(date)
                        # print(data1)
                        # print(data2)
                        find2 = 1

                        if find1 == 0:
                            print("Tracking Error: ")
                            print(f"The return of {classes[0]} is",data1)
                            print(f"The return of {classes[1]} is", data1)

            if find1>0 and find2>0:

                find1 = 0
                if find2 != 2:
                    find2 = 0
                if find2 != 2:
                    print("Section for share class: ", classes[0])
                else:
                    print("Section for share class: ", title)
                # print(len(data_date))
                print("The date (X-AXIS) is: ",data_date)
                print("Returns Chart:")
                # print(len(data_value))
                print("The return is: ", data_value)

                # print(len(date))
                # print(date)
                # print(len(data1))
                if find2 != 2:
                    print("Historical NAVs Chart""")
                    print(f"The NAV of line {classes[0]} is: ", data1)
                    if data2:
                        print(f"The NAV of line {classes[1]} is: ", data2)
                print("\n")



    except requests.exceptions.RequestException as e:
        print(f"Failed to fetch the webpage: {e}")
        return None






if __name__ == "__main__":
    # Target URL
    url = ""

    extract_chart_data(url)


