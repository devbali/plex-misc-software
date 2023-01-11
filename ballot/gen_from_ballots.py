import pandas as pd
import matplotlib.pyplot as plt
import os

weights = {
    "Exec": 0.25,
    "Leader": 0.25,
    "General": 0.5
}

def pie_chart(filename, df):
    # Pie chart, where the slices will be ordered and plotted counter-clockwise:
    labels = df.index
    sizes = df["total_weighted"]
    explode = [0.1] + [0 for i in range(len(df)-1)] # Top candidate explodes out a bit

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
    fig1.savefig(filename)

def valid_vote (vote):
    try:
        intvote = int(vote)
        return False if intvote <= 0 else intvote
    except:
        return False

def get_single_round (ballots):
    candidates = list(ballots.columns)[1:] # Candidate name strings
    quotalabel = list(ballots.columns)[0] # String used for the quota column header

    votes_by_quota = {quota: {candidate: 0 for candidate in candidates} for quota in weights}
    for _, row in ballots.iterrows():
        quota = row[quotalabel]
        # This is one vote
        assert quota in weights # Make sure quota for this vote is counted for
        ranks = {candidate: valid_vote(row[candidate]) for candidate in candidates if valid_vote(row[candidate])} # All candidates in play
        if ranks:
            preferred = min(ranks, key=ranks.get) # The preferred candidate, lowest rank not 0
            votes_by_quota[quota][preferred] += 1

    final_df = pd.DataFrame({quota: [votes_by_quota[quota][candidate] for candidate in candidates] for quota in weights}, index=candidates)
    
    for quota in weights:
        total_quota = final_df[quota].sum()
        final_df[f"{quota}_weighted"] = weights[quota] * 100 * final_df[quota] / total_quota
    
    final_df["total_weighted"] = sum([final_df[f"{quota}_weighted"] for quota in weights])
    final_df["total_raw"] = sum([final_df[quota] for quota in weights])
    return final_df.sort_values(["total_weighted","total_raw"], ascending=False)

def get_full_election_winner (ballots_df):
    rounds = []
    while not rounds or (len(rounds[-1]) > 2 and rounds[-1].iloc[0]["total_weighted"] < 50):
        if rounds: ballots_df = ballots_df.drop(rounds[-1].iloc[-1].name, axis=1) # Drop the lowest in the previous round
        rounds.append(get_single_round(ballots_df))

    return rounds[-1].iloc[0].name, rounds

def get_election_with_runnersup (ballots_df):
    candidates = list(ballots_df.columns)[1:]

    candidate_ranks = []
    rounds_data = []
    while candidates:
        winner, rounds = get_full_election_winner (ballots_df)
        candidate_ranks.append(candidates.pop(candidates.index(winner))) # remove winner from candidates and add to candidate_ranks
        rounds_data.append(rounds)
        
        if len(candidates) == 1:
            candidate_ranks.append(candidates.pop())
        else:
            ballots_df = ballots_df.drop(winner, axis=1)
    
    return candidate_ranks, rounds_data

def run_file (ballot_file, graphout="out", printout="out"):
    ballots_df = pd.read_csv(ballot_file, sep="\t").fillna(0)
    winners, rounds = get_election_with_runnersup(ballots_df)

    winnerstr = "\n".join([str(index+1) + ": " + winners[index] for index in range(len(winners))])
    electionstr = lambda rounds: "\n".join(["Round " + str(index+1) + ":\n" + rounds[index].to_csv(sep="\t",float_format="%.2f") for index in range(len(rounds))])
    roundstr = "\n\n".join(["Election " + str(index+1) + ":\n" + electionstr(rounds[index]) for index in range(len(rounds))])

    with open(printout,"w") as f:
        print(f'Winners:\n{winnerstr}\n\nElection Data:\n{roundstr}')
        print(f'Winners:\n{winnerstr}\n\nElection Data:\n{roundstr}', file=f)
    
    """
    for ei in range(len(rounds)):
        election = rounds[ei]
        for ri in range(len(election)):
            round = election[ri]
            pie_chart(f"{graphout}/Election {ei+1} - Round {ri+1}.png", round)
    """

if __name__ == "__main__":
    for f in os.listdir("ballots"):
        run_file(f"ballots/{f}", printout=f"results/{f.split('.')[0]}.txt")
