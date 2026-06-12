import fastf1

session = fastf1.get_session(2023, "Monaco", "R")
session.load()

results = session.results

print(results[["Abbreviation", "FullName", "TeamName", "Position"]])
