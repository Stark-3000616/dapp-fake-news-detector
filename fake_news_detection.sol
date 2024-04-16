// SPDX-License-Identifier: MIT
pragma solidity >=0.7.0 <0.9.0;

contract FakeNewsDetection{

    struct Voter{
        bool registered;
        mapping (string => uint256) trustRating;
    }

    struct newsItem{
        bool evaluated;
        string topic;
        string text;
        uint256 realweight;
        uint256 fakeweight;
        uint256 totalvoters;
        bool real;
        address[] votedreal;
        address[] votedfake;
    }

    mapping (address => Voter) public voters;
    mapping (uint256 => newsItem) public news;

    uint256 totalNumofVoters=0;
    uint256 totalNewsItems=0;

    event Voted(address indexed voter, uint256 newsid, bool real);
    event Evaluated(uint256 newsid, bool real);

    function register() public{
        require(!voters[msg.sender].registered, "Already Registered");
        voters[msg.sender].registered = true;
        totalNumofVoters++;
    }

    function submitNews(string memory top, string memory txt) public returns (uint256){
        totalNewsItems++;
        uint256 newsId=totalNewsItems;
        news[newsId].topic=top;
        news[newsId].text=txt;
        news[newsId].evaluated=false;
        news[newsId].realweight=0;
        news[newsId].fakeweight=0;
        news[newsId].totalvoters=0;
        return newsId;
    }

    function viewNews(uint256 newsId) public view returns (string memory){
        require(newsId<=totalNewsItems, "NewsId does not exist.");
        return news[newsId].text;
    }

    function vote(uint256 newsId, bool real) public{
        require(voters[msg.sender].registered, "Not registered to vote.");
        require(!news[newsId].evaluated, "News already evaluated.");
        string memory topic=news[newsId].topic;
        if(voters[msg.sender].trustRating[topic]==0)
        {
            voters[msg.sender].trustRating[topic]=50;
        }
        if(real)
        {
            news[newsId].realweight+=voters[msg.sender].trustRating[topic];
            news[newsId].votedreal.push(msg.sender);
        }
        else
        {
            news[newsId].fakeweight+=voters[msg.sender].trustRating[topic];
            news[newsId].votedfake.push(msg.sender);
        }
        news[newsId].totalvoters++;
        emit Voted(msg.sender, newsId, real);
        if(news[newsId].totalvoters>= (totalNumofVoters*2)/3 && news[newsId].realweight!=news[newsId].fakeweight)
        evaluateNews(newsId);
    }

    function evaluateNews(uint256 newsId) internal{
        news[newsId].evaluated=true;
        news[newsId].real= news[newsId].realweight> news[newsId].fakeweight;
        emit Evaluated(newsId, news[newsId].real);
        updateReputation(newsId);
    }

    function updateReputation(uint256 newsId) internal{
        if(news[newsId].real)
        {
            for(uint256 i=0; i<news[newsId].votedreal.length; i++)
            voters[news[newsId].votedreal[i]].trustRating[news[newsId].topic]+=2;
            for(uint256 i=0; i<news[newsId].votedfake.length; i++)
            voters[news[newsId].votedfake[i]].trustRating[news[newsId].topic]-=5;
        }
        else {
            for(uint256 i=0; i<news[newsId].votedreal.length; i++)
            voters[news[newsId].votedreal[i]].trustRating[news[newsId].topic]-=5;
            for(uint256 i=0; i<news[newsId].votedfake.length; i++)
            voters[news[newsId].votedfake[i]].trustRating[news[newsId].topic]+=2;
        }
    }

}