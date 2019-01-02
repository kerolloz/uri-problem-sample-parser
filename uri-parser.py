import re
import sys
import urllib.request
import os

try:
    from bs4 import BeautifulSoup
except Exception as e:
    raise e


def problem_link_checker(url):
    link_format = 'https://www.urionlinejudge.com.br/repository/UOJ_{number}_en.html'
    number = re.findall("[0-9]\d+", url)
    if len(number) == 1:
        return link_format.format(number=''.join(number)), number[0]
    return None


def get_tags_contents(html_souped, tag_name, class_name=None):
    return [tag for tag in html_souped.find_all(tag_name, class_name)]


def write_tags_to_files(tags_list, file_name="tag.txt"):
    counter = 1
    for tag in tags_list:
        if tag.p is not None:
            with open(str(counter) + file_name, 'w') as output_file:
                for line in tag.p.contents:
                    line = line.strip()  # clear all lines
                    line += '\n'  # add new line to the right
                    output_file.write(line.lstrip())
                    # lstrip = strip the left part(if the line is empty it will remove the added new line)

                counter += 1


def main():
    problem_link = sys.argv[1]
    problem_link, number = problem_link_checker(problem_link)
    # print(">> Please wait while downloading the submission content")
    try:
        my_request = urllib.request.urlopen(problem_link)
        my_html = my_request.read()
    except Exception as __connection_error__:
        print(">> Something went wrong while reading the submission link!", __connection_error__)
        return -1
    html_souped = BeautifulSoup(my_html, 'lxml')

    # replace <br> tags with new lines
    # so writing tags to files work properly
    for br_tag in html_souped.find_all("br"):
        br_tag.replace_with('')

    os.mkdir(number)
    os.chdir(number)
    all_td_tags_list = get_tags_contents(html_souped, tag_name='td')
    input_td_tags = get_tags_contents(html_souped, tag_name='td', class_name='division')
    # trim white spaces in test cases
    output_td_tags = list(set(all_td_tags_list) - set(input_td_tags))

    write_tags_to_files(input_td_tags, '.in')
    write_tags_to_files(output_td_tags, '.out')


if __name__ == '__main__':
    main()
