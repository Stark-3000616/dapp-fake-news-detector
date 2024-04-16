
# Design of DApp and Simulation - Fake news Detection
### This is an assignment for CS765 course (Introduction to Blockchain) in CSE, IIT Bombay

## Overview

This is a design of a decentralised application (DApp) for fake news detection in which any user can register as a voter and vote for a news being fake or real. Every voter has to deposit some money before making a vote and if the vote turns out be in majority, the voter is incentivised. Along with the pseudocode in solidity a code for simulation is provided in python.

## Requirements

- Python 3.x
- 

## Usage

python3 usage.py `<num_of_voters>` `<trustworthy_voter_%>` `<malicious_voter%>` `<num_of_news_items>`

## Description

The python script generates a simulation of fake news detection by creating voters with varying levels of trustworthiness. It then creates news items with random truth values and evaluates the detection of fake news based on the voters' opinions. 

## Parameters

- `numofvoters`: Total number of voters in the simulation.
- `trustworthy_voter_%`: Percentage of voters considered trustworthy.
- `malicious_voter%`: Percentage of voters considered malicious.
- `num_of_news_items`: Number of news items to be generated for the simulation.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
