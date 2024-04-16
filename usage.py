
from fake_news_detection import FakeNewsDetection
# from fake_news_detection import Message
from fake_news_detection import Voter
from fake_news_detection import NewsItem
import sys
import random
   
try:
    num_of_voters=0
    p=0
    q=0
    num_of_news_items=0
    if len(sys.argv)==5:
        num_of_voters=int(sys.argv[1])
        p=int(sys.argv[2])
        q=int(sys.argv[3])
        num_of_news_items=int(sys.argv[4])
    else:
        print(f'Usage: python3 {sys.argv[0]} <numofvoters> <trustworthy_voter_%> <malicious_voter%>')
        sys.exit(1)

    num_of_trustyvoters=int(p*num_of_voters/100)
    num_of_maliciousvoters=int(q*num_of_voters/100)

    voters=[]
    for i in range(1,num_of_voters+1):
        voter=None
        if i<=num_of_trustyvoters:
            voter=Voter(i, 'trusted', 50)
        elif i<=num_of_trustyvoters+num_of_maliciousvoters:
            voter=Voter(i,'malicious', 50)
        else:
            voter=Voter(i,'honest', 50)
        voters.append(voter)
    
    random.shuffle(voters)
    
    truth=random.choices([False, True], k=num_of_news_items)
    news_items=[]
    for i in range(1,num_of_news_items+1):
        newsitem=NewsItem(i, truth[i-1])
        news_items.append(newsitem)


    fake_news_detection = FakeNewsDetection(voters, news_items)
    fake_news_detection.start_simulation(truth)
    fake_news_detection.display_and_evaluation(truth)
    
except Exception as e:
    print("Error:", str(e))