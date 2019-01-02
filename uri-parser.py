import

def problem_link_checker(url):
    link_format = 'https://www.urionlinejudge.com.br/repository/UOJ_{number}_en.html'
    number = re.findall("[0-9]\d+", url)
    if len(number) == 1:
        return link_format.format(number=''.join(number))
    return None

def main


if __name__ == '__main__':
    main()
