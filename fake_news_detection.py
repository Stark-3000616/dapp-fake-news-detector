import random
class Voter:
    def __init__(self, id, identity, balance):
        self.id=id
        self.identity=identity
        self.rating = 0.5
        self.balance = balance
        self.correct_votes=0
        self.total_votes=0

class NewsItem:
    def __init__(self, id, real):
        self.id=id
        self.evaluated = False
        self.real_weight = 0
        self.fake_weight = 0
        self.total_voters = 0
        self.real = real
        self.voted_real = []
        self.voted_fake = []
    
    def generate_probability(self, k):
        return random.random() < k

    def vote_for_news(self, voter, truthvalue):
        voter.balance-=5
        voter.total_votes+=1
        vote=truthvalue
        if voter.identity=='trusted':
            vote=vote and self.generate_probability(0.9)
        elif voter.identity=='malicious':
            vote=not vote
        else:
            vote=vote and self.generate_probability(0.7)
        
        self.total_voters+=1
        if(vote):
            self.real_weight+=voter.rating
            self.voted_real.append(voter)
        else:
            self.fake_weight+=voter.rating
            self.voted_fake.append(voter)
    
    def evaluate_news(self):
        self.real= self.real_weight>self.fake_weight
        self.evaluated=True

    def update_reputation_and_balance(self):
        if(self.real):
            for voter in self.voted_real:
                voter.balance+=10
                voter.correct_votes+=1
                voter.rating+=(voter.correct_votes/voter.total_votes)/100
                voter.rating=min([1.0, voter.rating])
            for voter in self.voted_fake:
                voter.rating-=((voter.total_votes-voter.correct_votes)/voter.total_votes)/100
                voter.rating=max([0.0, voter.rating])
        else:
            for voter in self.voted_fake:
                voter.balance+=10
                voter.correct_votes+=1
                voter.rating+=(voter.correct_votes/voter.total_votes)/100
                voter.rating=min([1.0, voter.rating])
            for voter in self.voted_real:
                voter.rating-=((voter.total_votes-voter.correct_votes)/voter.total_votes)/100
                voter.rating=max([0.0, voter.rating])

class FakeNewsDetection:
    def __init__(self, voters, news_items):
        self.voters = voters
        self.news_items = news_items
        self.total_num_of_voters = len(voters)
        self.total_news_items = len(news_items)

    def start_simulation(self, truth):
        for news in self.news_items:
            random.shuffle(self.voters)
            i=1
            for voter in self.voters:
                if voter.balance>=5:
                    news.vote_for_news(voter, truth[news.id-1])
                    i+=1
                else:
                    continue
                if i>int(self.total_num_of_voters*0.66):
                    break
            news.evaluate_news()
            news.update_reputation_and_balance()
    
    def display_and_evaluation(self, truth):
        with open("voter_information.txt", "w") as file:
            for voter in self.voters:
                file.write("{:.2f}".format(voter.rating) + " " + str(voter.balance) + " " + voter.identity + " " + str(voter.total_votes) + " " + str(voter.correct_votes)+"\n")
        
        with open("news_information.txt", "w") as file:
            false_prediction=0
            for news in self.news_items:
                file.write(str(news.total_voters) + " " + str(news.real_weight) +" "+ str(news.fake_weight) + " " + str(news.real) +" "+ str(truth[news.id-1])+"\n")
                if news.real != truth[news.id-1]:
                    false_prediction+=1
            print("Number of false predictions=",false_prediction)
            print("Total number of news=", self.total_news_items)
            print("News prediction accuracy for the simulation:", "{:.2f}".format((self.total_news_items-false_prediction)*100/self.total_news_items), "%")
        
        

