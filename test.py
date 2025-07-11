from solution import DivarContest

api_token = "tpsg-f59gl7lRIU1HrGweCwRgBlIRE30DWfW"
agent = DivarContest(api_token)
question = "call {https://divar-contest.darkube.app/pending-ads/ad-public-931582.json} and fetch the pending ads, review the fetched ads and choose the correct tag for each one. It is guaranteed that only one of the issues exists in the ads."
result = agent.capture_the_flag(question)
print(result) 