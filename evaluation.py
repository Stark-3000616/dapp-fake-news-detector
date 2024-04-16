import subprocess
import matplotlib.pyplot as plt

def run_simulation(num_of_voters, trustworthy_pct, malicious_pct, num_of_news_items):
    command = f"python3 usage.py {num_of_voters} {trustworthy_pct} {malicious_pct} {num_of_news_items}"
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    output_lines = result.stdout.split('\n')
    accuracy_line = [line for line in output_lines if line.startswith("News prediction accuracy")][0]
    accuracy = float(accuracy_line.split(': ')[1].split('%')[0]) / 100
    return accuracy

def main():
    num_of_voters = 30
    trustworthy_pct_values = range(0,21,10)
    num_of_news_items = 100
    malicious_pct_values = range(0, 81, 10)

    for trustworthy_pct in trustworthy_pct_values:

        accuracies = []
        for malicious_pct in malicious_pct_values:
            accuracy = run_simulation(num_of_voters, trustworthy_pct, malicious_pct, num_of_news_items)
            accuracies.append(accuracy)

        # Visualize the data
        plt.plot(malicious_pct_values, accuracies, marker='o', label=f'Trusted voters= {trustworthy_pct}%')
    plt.xlabel('Malicious Voters Percentage')
    plt.ylabel('Accuracy')
    plt.title('Fake News Detection Accuracy vs. Malicious Voters Percentage')
    plt.grid(True)
    plt.legend()
    plt.savefig('results.png')

if __name__ == "__main__":
    main()
