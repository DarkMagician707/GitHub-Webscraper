import requests
from bs4 import BeautifulSoup

def scraper_users(username):
    URL = "https://github.com/"+username
    # username = "geohot"
    #here we request all the html code from the web page we scrape
    page = getResponse(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    user_info = {}
    if soup.find() != None:
        company_classifier = soup.find('meta', attrs={'name':'hovercard-subject-tag'})
        if company_classifier is None:     
            names_info = soup.find("h1", class_ = "vcard-names")

            # print(names_info)
            login = soup.find("span", class_ = "p-nickname vcard-username d-block")
            if login is None:
                login = None
            else:
                login = login.text.strip()
            user_info['login'] = login

            id = soup.find('meta', attrs={'name':'octolytics-dimension-user_id'})['content']
            if id is None:
                id = None
            user_info['id'] = int(id)

            profile_pic = soup.find("div", class_ = "position-relative d-inline-block col-2 col-md-12 mr-3 mr-md-0 flex-shrink-0").find("a").get('href')
            if profile_pic is None:
                profile_pic = None
            user_info['avatar_url'] = profile_pic

            user_info['url'] = "https://api.github.com/users/" + username
            user_info['html_url'] = "https://github.com/"+username

            user_info['type'] = "User"

            name_user = soup.find("span", class_ = "p-name vcard-fullname d-block overflow-hidden")
            if name_user is None or "":
                name_user = None
            else:
                name_user = name_user.text.strip()
            user_info['name'] = name_user

            company = soup.find("li", itemprop = "worksFor")
            if company is None:
                company = None
            else:
                company = company.text.strip()
            user_info['company'] = company

            blog = soup.find("li", itemprop = "url")
            if blog is None:
                blog = None
            else:
                blog = blog.find("a", rel = "nofollow me").get("href")
            user_info["blog"] = blog

            location = soup.find("li", itemprop = "homeLocation")
            if location is None:
                location = None
            else:
                location = location.text.strip()
            user_info['location'] = location

            bio = soup.find("div", class_ = "p-note user-profile-bio mb-3 js-user-profile-bio f4")
            if bio is None:
                bio = None
            else:
                bio = bio.text
            user_info['bio'] = bio

            twitter = soup.find("li", itemprop = "social")
            if twitter is None:
                twitter = None
            else:
                twitter = twitter.find("a", attrs={"class": "Link--primary"}).text
            user_info['twitter_username'] = twitter

            repos = soup.find("span", class_ = "Counter")
            if repos is None:
                repos = None
            else:
                repos = repos.text
            user_info['public_repos'] = int(repos)

            followers_href = f"https://github.com/{username}?tab=followers"
            following_href = f"https://github.com/{username}?tab=following"

            followers = soup.find("a", href = followers_href)
            if followers is None:
                followers = 0            
            else:
                followers = followers.find("span").text
                pos = followers.find(".")
                posk = followers.find("k")
                number = 0
                if pos is not -1:
                    elements = followers.split(".")
                    number = ""+elements[0]+elements[1].split("k")[0]
                    number = int(number)-1
                    number = number*100
                    pages = number/50                
                    count = 0                
                    followers_URL = f"https://github.com/{login}?page={pages}&tab=followers"
                    result = pageCounterUser(followers_URL)
                    while result is 50:
                        count += 1
                        followers_URL = f"https://github.com/{login}?page={pages+count}&tab=followers"
                        result = pageCounterUser(followers_URL)
                    number = number + result + (count-1)*50
                elif posk is not -1:
                    elements = followers.split("k")
                    number = ""+elements[0]
                    number = int(number)
                    number = number*1000
                    pages = number/50                
                    count = 0                
                    followers_URL = f"https://github.com/{login}?page={pages}tab=followers"
                    result = pageCounterUser(followers_URL)
                    while result is 50:
                        count += 1
                        followers_URL = f"https://github.com/{login}?page={pages+count}tab=followers"
                        result = pageCounterUser(followers_URL)
                    number = number + result + (count-1)*50
                else:
                    number = int(followers)
                followers = number
            user_info['followers'] = followers

            following = soup.find("a", href = following_href)
            if following is None:
                following = 0
            else:
                following = following.find("span").text
            user_info['following'] = int(following)
        
        
        # If the page is that of a company (since company pages have different layouts):
        else:        
            company_classifier = company_classifier['content']
            id = company_classifier.split(":")[1]

            login = soup.find("a", class_ = "Header-link")
            if login is None:
                login = None
            else:
                login = login.text.strip()
            user_info['login'] = login  

            user_info["id"] = int(id)

            avatar_url = soup.find("img", attrs={"class": "avatar flex-shrink-0 mb-3 mr-3 mb-md-0 mr-md-4"})
            if avatar_url is None:
                avatar_url = None
            else:
                avatar_url = avatar_url['src']
            user_info["avatar_url"] = avatar_url

            user_info['url'] = "https://api.github.com/users/" + username
            user_info['html_url'] = "https://github.com/"+username
            user_info['type'] = "Organization"

            name = soup.find("h1", attrs={'class': "h2 lh-condensed"})
            if name is None:
                name = None
            else:
                name = name.text.strip()
            user_info['name'] = name

            user_info['company'] = None

            blog = soup.find("a",attrs={"rel": "nofollow"})
            if blog is not None:
                blog = blog.get("href")
            user_info['blog'] = blog

            location = soup.find("span", itemprop = "location")
            if location is not None:
                location = location.text.strip()
            user_info['location'] = location

            bio = soup.find(lambda tag: tag.name == "div" and tag.get("class", []) == ["color-fg-muted"])
            if bio is not None:
                bio = bio.text.strip()
            if bio is "":
                bio = None
            user_info['bio'] = bio
            
            twitter = soup.find("li", attrs={"class": "mr-md-3 v-align-middle my-2 my-md-0 css-truncate css-truncate-target"})
            if twitter is not None:
                twitter = twitter.find("a", attrs={"class": "Link--primary"}).text
            user_info['twitter_username'] = twitter

            # repos_href = f"/orgs/{login}/repositories"
            # repos = soup.find("span", class_ = "Counter js-profile-repository-count")
            # if repos is None:
            #     repos = 0
            # else:
            #     repos = repos.text
            #     pos = repos.find(".")

            #     if pos is not -1:
            #         elements = repos.split(".")
            #         number = ""+elements[0]+elements[1].split("k")[0]
            #         number = int(number)-1
            #         number = number*100
            #         pages = number/50                
            #         count = 0                
            #         repos_URL = f"https://github.com/orgs/{login}/repositories?page={pages}"
            #         result = repoCounter(repos_URL)
            #         while result is 50:
            #             count += 1
            #             repos_URL = f"https://github.com/orgs/{login}/repositories?page={pages+count}"
            #             result = repoCounter(repos_URL)
            #         number = number + result + (count-1)*50
            #     else:
            #         number = int(repos)
            # repos = number
            # user_info['public_repos'] = repos

            repos = soup.find("meta", attrs={"name": "description"}).get("content")
            number = repos.split(f"{name} has ")[1].split(" ")[0]
            number = int(number)
            user_info['public_repos'] = number

            followers_href = f"/orgs/{login}/followers"
            followers = soup.find("a", href = followers_href)
            if followers is None:
                followers = 0            
            else:
                followers = followers.find("span").text
                pos = followers.find(".")
                posk = followers.find("k")
                if pos is not -1:
                    elements = followers.split(".")
                    number = ""+elements[0]+elements[1].split("k")[0]
                    number = int(number)-1
                    number = number*100
                    pages = number/50                
                    count = 0                
                    followers_URL = f"https://github.com/orgs/{login}/followers?page={pages}"
                    result = pageCounter(followers_URL)
                    while result is 50:
                        count += 1
                        followers_URL = f"https://github.com/orgs/{login}/followers?page={pages+count}"
                        result = pageCounter(followers_URL)
                    number = number + result + (count-1)*50
                elif posk is not -1:
                    elements = followers.split("k")
                    number = ""+elements[0]
                    number = int(number)
                    number = number*1000
                    pages = number/50                
                    count = 0                
                    followers_URL = f"https://github.com/orgs/{login}/followers?page={pages}"
                    result = pageCounter(followers_URL)
                    while result is 50:
                        count += 1
                        followers_URL = f"https://github.com/orgs/{login}/followers?page={pages+count}"
                        result = pageCounter(followers_URL)
                    number = number + result + (count-1)*50
                else:
                    number = int(followers)
                followers = number
            user_info['followers'] = int(followers)

            user_info['following'] = 0

        return user_info 
    else:
        return page
    
def pageCounter(fref):
    follower_page = getResponse(fref)
    follower_soup = BeautifulSoup(follower_page.content, "html.parser")
    fresult = len(follower_soup.find_all("div", class_ = "d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted"))
    return fresult   

def pageCounterUser(fref):
    follower_page = getResponse(fref)
    follower_soup = BeautifulSoup(follower_page.content, "html.parser")
    fresult = len(follower_soup.find_all("div", class_ = "d-table table-fixed col-12 width-full py-4 border-bottom color-border-muted"))
    return fresult  

def repoCounter(fref):
    repo_page = getResponse(fref)
    repo_soup = BeautifulSoup(repo_page.content, "html.parser")
    rresult = len(repo_soup.find_all("li", class_ = "Box-row"))
    return rresult 

def repoPageCounter(href):
    page = getResponse(href)
    soup = BeautifulSoup(page.content, "html.parser")
    repos_on_page = soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"})
    repo_count = len(repos_on_page.findAll("li", class_ = "col-12 d-flex flex-justify-between width-full py-4 border-bottom color-border-muted public source"))
    return repo_count

def getResponse(url, base_delay = 1):
    delay = base_delay
    while True:
        response = requests.get(url)
        if response.status_code != 429:
            return response
        print(f"Got 429 response. Retrying in {delay} seconds...")
        time.sleep(delay)
        delay=2*delay

# def scraper_repos(username):
#     URL = "https://github.com/"+username+"?tab=repositories"
#     page = requests.get(URL)
#     soup = BeautifulSoup(page.content, "html.parser")
#     repos_on_page = soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"})  
#     counter = 1
#     user_info = []
#     while repos_on_page is not None: 
#         repo_info =  scrape_repos_on_page(repos_on_page, soup, username)
#         user_info = user_info + repo_info
#         counter += 1
#         URL = f"https://github.com/{username}?page={counter}&tab=repositories"
#         page = requests.get(URL) 
#         soup = BeautifulSoup(page.content, "html.parser")
#         repos_on_page = soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"}) 

#     # print(counter)
#     return user_info

def scraper_repos(username, per_page, qpage):
    URL = "https://github.com/"+username
    page = getResponse(URL)
    soup = BeautifulSoup(page.content, "html.parser")    
    user_info = []
    if soup.find() != None:
        org = soup.find('meta', attrs={'name':'hovercard-subject-tag'})
        if org is None and per_page == 30:
            user_URL = f"https://github.com/{username}?tab=repositories&page={qpage}"
            user_page = getResponse(user_URL)
            user_soup = BeautifulSoup(user_page.content, "html.parser")
            repos_on_page = user_soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"})  
            if repos_on_page is not None:
                repo_info =  scrape_repos_on_page(repos_on_page, user_soup, username)    
                user_info = user_info + repo_info  

        elif org is None and per_page != 30:
            user_URL = f"https://github.com/{username}?tab=repositories&page={qpage}"
            user_page = getResponse(user_URL)
            user_soup = BeautifulSoup(user_page.content, "html.parser")
            counter = 1
            repos_on_page = user_soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"})
            while repos_on_page is not None: 
                repos_on_page = user_soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"})  
                if repos_on_page is not None:
                    repo_info =  scrape_repos_on_page(repos_on_page, user_soup, username)    
                    user_info = user_info + repo_info
                    counter += 1
                    URL = f"https://github.com/{username}?page={counter}&tab=repositories"
                    page = requests.get(URL) 
                    soup = BeautifulSoup(page.content, "html.parser")
                    repos_on_page = user_soup.find("ul", attrs={"data-filterable-for": "your-repos-filter"}) 

        elif org != None and per_page == 30:
            org_URL = f"https://github.com/orgs/{username}/repositories?&page={qpage}"
            org_page = getResponse(org_URL)
            org_soup = BeautifulSoup(org_page.content, "html.parser")
            repos_on_page_org = org_soup.find("ul", attrs={"data-view-component": "true"})
            if repos_on_page_org is not None:
                repo_info = scrape_repos_on_page_org(repos_on_page_org, org_soup, username, org)
                user_info = user_info + repo_info
        else:
            org_URL = f"https://github.com/orgs/{username}/repositories"
            org_page = getResponse(org_URL)
            org_soup = BeautifulSoup(org_page.content, "html.parser")
            counter = 1
            repos_on_page_org = org_soup.find("ul", attrs={"data-view-component": "true"})
            while repos_on_page is not None: 
                repos_on_page_org = org_soup.find("ul", attrs={"data-view-component": "true"})
                if repos_on_page_org is not None:
                    repo_info = scrape_repos_on_page_org(repos_on_page_org, org_soup, username, org)
                    user_info = user_info + repo_info
                counter += 1
                org_URL = f"https://github.com/orgs/{username}/repositories?page={counter}"
                org_page = getResponse(org_URL)
                org_soup = BeautifulSoup(org_page.content, "html.parser")
                repos_on_page_org = org_soup.find("ul", attrs={"data-view-component": "true"})

        return user_info
    else:
        return page

def scrape_repos_on_page(repos_on_page, soup, username):
    user_info = []
    repo_counter = 0
    all_repos = repos_on_page.find_all("li", itemprop = "owns")
    
    while repo_counter < len(all_repos):
        next_repo = all_repos[repo_counter]
        current_repo = {}
        name = next_repo.find("a", itemprop = "name codeRepository").text.strip()
        html_URL = "https://github.com/"+username+"/"+name
        repo_URL = html_URL
        current_page = getResponse(repo_URL)
        current_soup = BeautifulSoup(current_page.content, "html.parser")

        id = current_soup.find("meta", attrs={"name": "octolytics-dimension-repository_id"}).get("content")
        current_repo['id'] = int(id)
        current_repo['name'] = name
        current_repo['full_name'] = f"{username}/{current_repo['name']}"

        owner = {}
        login = soup.find("meta", attrs={"name": "octolytics-dimension-user_login"})['content']
        owner['login'] = login

        id = soup.find('meta', attrs={'name':'octolytics-dimension-user_id'})['content']
        if id is not None:
            owner['id'] = int(id)
        current_repo['owner'] = owner

        status = next_repo.find("span", class_ = "Label Label--secondary v-align-middle ml-1 mb-1")
        if status is None:
            status = next_repo.find("span", class_ = "Label Label--attention v-align-middle ml-1 mb-1")
        status = status.text

        if status.find("Public") != -1:
            current_repo['private'] = False
        else:
            current_repo['private'] = True
        
        current_repo['html_url'] = "https://github.com/"+current_repo['full_name']
        description =  next_repo.find("p", class_ = "col-9 d-inline-block color-fg-muted mb-2 pr-4")
        if description is not None:
            description = description.text.strip()
        current_repo['description'] = description
        
        fork = next_repo.find("span", attrs = {"class": "f6 color-fg-muted mb-1"})
        if fork is None:
            current_repo['fork'] = False
        else:
            current_repo['fork'] = True

        current_repo['url'] = "https://api.github.com/repos/"+current_repo['full_name']

        homepage = current_soup.find("span", attrs={"class": "flex-auto min-width-0 css-truncate css-truncate-target width-fit"})
        if homepage is not None:
            homepage = homepage.find("a", attrs={"class": "text-bold"}).get("href")
        current_repo['homepage'] = homepage

        language = next_repo.find("span", itemprop = "programmingLanguage")
        if language is not None:
            language = language.text
        current_repo['language'] = language

        forks_count = next_repo.find("a", href = f"/{username}/{current_repo['name']}/forks")
        if forks_count is not None:
            forks_count = forks_count.text.strip()
            if forks_count.find(",") != -1:
                elements = forks_count.split(",")
                forks_count = elements[0]+""+elements[1]
            current_repo['forks_count'] = int(forks_count)
        else:
            current_repo['forks_count'] = 0

        stargazers_count = next_repo.find("a", href = f"/{username}/{current_repo['name']}/stargazers")
        if stargazers_count is not None:
            stargazers_count = stargazers_count.text.strip()            
            if stargazers_count.find(",") != -1:
                elements = stargazers_count.split(",")
                stargazers_count = elements[0]+""+elements[1]
            current_repo['stargazers_count'] = int(stargazers_count)
        else:
            current_repo['stargazers_count'] = 0
        
        current_repo['watchers_count'] = current_repo['stargazers_count']

        default_branch = current_soup.find('summary', attrs={'class': 'btn css-truncate'}).find('span', attrs={'class': 'css-truncate-target'})
        if default_branch is not None:
            default_branch = default_branch.text.strip()
        else:
            default_branch = "main"
        current_repo['default_branch'] = default_branch

        issues_URL = f"https://github.com/{current_repo['full_name']}/issues"
        issues_requests = getResponse(issues_URL)
        issues_requests = BeautifulSoup(issues_requests.content, "html.parser")
        if issues_requests is not None:
            issues_requests = issues_requests.find("a", attrs = {"class": "btn-link selected"}).text.strip()
            elements = issues_requests.split(" ")
            if elements[0].find(",") != -1:
                elements = elements[0].split(",")
                issues_requests = int(elements[0] + "" + elements[1])
            else:
                issues_requests = int(elements[0])
        else:
            issues_requests = 0

        pull_URL = f"https://github.com/{current_repo['full_name']}/pulls"
        pull_requests = getResponse(pull_URL)
        pull_requests = BeautifulSoup(pull_requests.content, "html.parser")
        if pull_requests is not None:
            pull_requests = pull_requests.find("a", attrs = {"class": "btn-link selected"}).text.strip()
            elements = pull_requests.split(" ")
            if elements[0].find(",") != -1:
                elements = elements[0].split(",")
                pull_requests = int(elements[0] + "" + elements[1])
            else:
                pull_requests = int(elements[0])
        else:
            pull_requests = 0

        open_issues_count = issues_requests + pull_requests
        current_repo['open_issues_count'] = open_issues_count

        topics = []
        topics_scraped = current_soup.find_all("a", attrs={"data-ga-click": "Topic, repository page"})
        if topics_scraped is not None:
            for current_topic in topics_scraped:
                current_topic = current_topic.text.strip()
                topics.append(current_topic)
        topics = sorted(topics)
        current_repo['topics'] = topics


        issues = current_soup.find("span", attrs={'data-content': 'Issues'})
        if issues is not None:
            current_repo['has_issues'] = True
        else:
            current_repo['has_issues'] = False
        
        projects = current_soup.find("span", attrs={'data-content': 'Projects'})
        if projects is not None:
            current_repo['has_projects'] = True
        else:
            current_repo['has_projects'] = False

        discussions = current_soup.find("span", attrs={"data-content": "Discussions"})
        if discussions is not None:
            current_repo['has_discussions'] = True
        else:
            current_repo['has_discussions'] = False

        if status.find("archive") != -1:
            current_repo['archived'] = True
        else:
            current_repo['archived'] = False

        pushed_at = next_repo.find("relative-time", attrs={"class": "no-wrap"})
        if pushed_at is not None:
            pushed_at = pushed_at["datetime"]
        current_repo['pushed_at'] = pushed_at

        user_info.append(current_repo)
        repo_counter += 1
        
    return user_info

def scrape_repos_on_page_org(repos_on_page, soup, username, org):
    user_info = []
    repo_counter = 0
    all_repos = repos_on_page.find_all("li", attrs={"class": "Box-row"})
    
    while repo_counter < len(all_repos):
        #
        next_repo = all_repos[repo_counter]
        current_repo = {}
        name = next_repo.find("a", itemprop = "name codeRepository").text.strip()
        html_URL = "https://github.com/"+username+"/"+name
        repo_URL = html_URL
        current_page = getResponse(repo_URL)
        current_soup = BeautifulSoup(current_page.content, "html.parser")

        id = current_soup.find("meta", attrs={"name": "octolytics-dimension-repository_id"}).get("content")
        current_repo['id'] = int(id)
        current_repo['name'] = name
        current_repo['full_name'] = f"{username}/{current_repo['name']}"

        owner = {}
        #
        login = soup.find("a", attrs= {"class": "Header-link"})
        if login is not None:
            login = login.text.strip()
        owner['login'] = login
        #
        id = soup.find('meta', attrs={'name':'hovercard-subject-tag'})['content']
        if id is not None:
            id = id.split(":")[1]
            owner['id'] = int(id)
        current_repo['owner'] = owner
        
        #Check status:
        status = next_repo.find("span", class_ = "Label Label--secondary v-align-middle ml-1 mb-1")
        if status is None:
            status = next_repo.find("span", class_ = "Label Label--attention v-align-middle ml-1 mb-1")
        status = status.text

        if status.find("Public") != -1:
            current_repo['private'] = False
        else:
            current_repo['private'] = True
        #
        current_repo['html_url'] = "https://github.com/"+current_repo['full_name']
        description =  next_repo.find("p", class_ = "color-fg-muted mb-0 wb-break-word")
        if description is not None:
            description = description.text.strip()
        current_repo['description'] = description
        #
        fork = next_repo.find("span", attrs = {"class": "color-fg-muted mb-1 f6"})
        if fork is None:
            current_repo['fork'] = False
        else:
            current_repo['fork'] = True
        #
        current_repo['url'] = "https://api.github.com/repos/"+current_repo['full_name']

        #
        homepage = current_soup.find("span", attrs={"class": "flex-auto min-width-0 css-truncate css-truncate-target width-fit"})
        if homepage is not None:
            homepage = homepage.find("a", attrs={"class": "text-bold"}).get("href")
        current_repo['homepage'] = homepage
        #
        language = next_repo.find("span", itemprop = "programmingLanguage")
        if language is not None:
            language = language.text
        current_repo['language'] = language
        #
        forks_count = next_repo.find("a", href = f"/{username}/{current_repo['name']}/forks")
        if forks_count is not None:
            forks_count = forks_count.text.strip()
            if forks_count.find(",") != -1:
                elements = forks_count.split(",")
                forks_count = elements[0]+""+elements[1]
            current_repo['forks_count'] = int(forks_count)
        else:
            current_repo['forks_count'] = 0
        #
        stargazers_count = next_repo.find("a", href = f"/{username}/{current_repo['name']}/stargazers")
        if stargazers_count is not None:
            stargazers_count = stargazers_count.text.strip()            
            if stargazers_count.find(",") != -1:
                elements = stargazers_count.split(",")
                stargazers_count = elements[0]+""+elements[1]
            current_repo['stargazers_count'] = int(stargazers_count)
        else:
            current_repo['stargazers_count'] = 0
        #
        current_repo['watchers_count'] = current_repo['stargazers_count']

        #
        default_branch = current_soup.find('summary', attrs={'class': 'btn css-truncate'}).find('span', attrs={'class': 'css-truncate-target'})
        # default_branch = current_soup.find('span', attrs={'class': 'css-truncate-target'})
        if default_branch is not None:
            default_branch = default_branch.text.strip()
        else:
            default_branch = "main"
        current_repo['default_branch'] = default_branch
        #
        issues_URL = f"https://github.com/{current_repo['full_name']}/issues"
        issues_requests = getResponse(issues_URL)
        issues_requests = BeautifulSoup(issues_requests.content, "html.parser")
        if issues_requests is not None:
            issues_requests = issues_requests.find("a", attrs = {"class": "btn-link selected"}).text.strip()
            elements = issues_requests.split(" ")
            if elements[0].find(",") != -1:
                elements = elements[0].split(",")
                issues_requests = int(elements[0] + "" + elements[1])
            else:
                issues_requests = int(elements[0])
        else:
            issues_requests = 0
        #
        pull_URL = f"https://github.com/{current_repo['full_name']}/pulls"
        pull_requests = getResponse(pull_URL)
        pull_requests = BeautifulSoup(pull_requests.content, "html.parser")
        if pull_requests is not None:
            pull_requests = pull_requests.find("a", attrs = {"class": "btn-link selected"}).text.strip()
            elements = pull_requests.split(" ")
            if elements[0].find(",") != -1:
                elements = elements[0].split(",")
                pull_requests = int(elements[0] + "" + elements[1])
            else:
                pull_requests = int(elements[0])
        else:
            pull_requests = 0
        #
        open_issues_count = issues_requests + pull_requests
        current_repo['open_issues_count'] = open_issues_count
        #
        topics = []
        topics_scraped = current_soup.find_all("a", attrs={"data-ga-click": "Topic, repository page"})
        if topics_scraped is not None:
            for current_topic in topics_scraped:
                current_topic = current_topic.text.strip()
                topics.append(current_topic)
        topics = sorted(topics)
        current_repo['topics'] = topics
        #
        issues = current_soup.find("span", attrs={'data-content': 'Issues'})
        if issues is not None:
            current_repo['has_issues'] = True
        else:
            current_repo['has_issues'] = False
        #
        projects = current_soup.find("span", attrs={'data-content': 'Projects'})
        if projects is not None:
            current_repo['has_projects'] = True
        else:
            current_repo['has_projects'] = False
        #
        discussions = current_soup.find("span", attrs={"data-content": "Discussions"})
        if discussions is not None:
            current_repo['has_discussions'] = True
        else:
            current_repo['has_discussions'] = False
        #
        if status.find("archive") != -1:
            current_repo['archived'] = True
        else:
            current_repo['archived'] = False
        #
        pushed_at = next_repo.find("relative-time", attrs={"class": "no-wrap"})
        if pushed_at is not None:
            pushed_at = pushed_at["datetime"]
        current_repo['pushed_at'] = pushed_at

        user_info.append(current_repo)
        repo_counter += 1
        
    return user_info
