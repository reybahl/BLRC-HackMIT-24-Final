import requests

class LLMTranscript:
    def __init__ (self, elements):
        self.string = ""
        self.individual_strings = []
        self.times = []
        self.summary = ""
        for x in elements:
            self.string += x["content"]
            self.individual_strings.append(x["content"])
            self.times.append(x["timestamp_start"])
        
    def summarize(self):

        model_id = "7qkpp7dw"
        baseten_api_key = "Us98UpGt.GfMVx8t9i7EN5Tr2oS13ZhtPhtY3uWag"

        data = {
            "prompt": f"""Summarize the following text in \emphasize{{no more than 300 words}}. Focus on the key points, main arguments, and essential details. Your summary should capture the core ideas without including unnecessary explanations or examples. \emphasize{{Do not exceed the word limit}}. Provide only the summary \emphasize{{without additional context or commentary}}. You should only include the summary. \emphasize{{Do not}} include other words. Below is the text to summarize.

            {self.string}
        """,
            "stream": True,
            "max_tokens": 1024
        }

        # Call model endpoint
        res = requests.post(
            f"https://model-{model_id}.api.baseten.co/production/predict",
            headers={"Authorization": f"Api-Key {baseten_api_key}"},
            json=data,
            stream=True
        )

        generated_string = ""
        # Print the generated tokens as they get streamed
        for content in res.iter_content():
            generated_string += content.decode("utf-8")

        self.summary = generated_string
        return generated_string
    def q_a(self, label, timestamp, question):
        model_id = "7qkpp7dw"
        baseten_api_key = "Us98UpGt.GfMVx8t9i7EN5Tr2oS13ZhtPhtY3uWag"
        start = timestamp - 10
        end = timestamp + 10
        context_string = ""
        if timestamp < 20:
            end = timestamp + 30

        for i, x in enumerate(self.times):
            if(start < x and x < end):
                context_string += self.individual_strings[i]

        data = {
            "prompt": f"""Answer the question at the bottom given the following information. The answer can be of any length as long as it \emphasize{{does not exceed 300 words}}. 
            The topic is: {label}
            
            The context in the video to be considered is:
                {context_string}
                
            The summary of the full transcript is:
               {self.summary}. 

            Here is the question for you to answer: 
            {question}
        """,
            "stream": True,
            "max_tokens": 1024
        }

        # Call model endpoint
        res = requests.post(
            f"https://model-{model_id}.api.baseten.co/production/predict",
            headers={"Authorization": f"Api-Key {baseten_api_key}"},
            json=data,
            stream=True
        )

        generated_string = ""
        # Print the generated tokens as they get streamed
        for content in res.iter_content():
            generated_string += content.decode("utf-8")

        return generated_string

    
transcript_obj = LLMTranscript([{"content" : """
Before we dive into Week 2, I want to share why many in the league were talking about training camp over the past couple days.
We saw some teams come out of the gate looking conditioned and fierce — like the Chiefs (https://www.nytimes.com/athletic/nfl/team/chiefs/), Steelers (https://www.nytimes.com/athletic/nfl/team/steelers/), and Lions (https://www.nytimes.com/athletic/nfl/team/lions/), who are all known for their brutally tough practices (not to mention, Patrick Mahomes (https://www.nytimes.com/athletic/nfl/player/patrick-mahomes-WWwiw0IQD5ozgrHf/) and Travis Kelce (https://www.nytimes.com/athletic/nfl/player/travis-kelce-4wuXOfkjv6uJbT7O/) didn’t miss one practice all summer). Compare that to teams that lost their Week 1 games because they looked out of shape, didn’t seem in sync, or — in cases like the Browns (https://www.nytimes.com/athletic/nfl/team/browns/) — looked like they didn’t want to be there based on body language.
Cleveland was one of the last teams to put on pads this summer. Many team executives and coaches are still trying to figure out if there is a correlation between early-season success and how teams are practicing all summer. For teams that didn’t play their starters in the preseason, like Green Bay (https://www.nytimes.com/athletic/nfl/team/packers/) and Atlanta (https://www.nytimes.com/athletic/nfl/team/falcons/), September is the new preseason, which could catch up to them in December.

Sam Darnold (https://www.nytimes.com/athletic/nfl/player/sam-darnold-3Nxpcb3Oda9xKjNY/) for MVP! The Bears (https://www.nytimes.com/athletic/nfl/team/bears/) offense stinks! Mike McCarthy is Coach of the Year!
None of this is true after one game, but I’m thrilled to get through a week of overreaction. I trust most of us know that opening weekend is a lie, but we may have seen some snippets of truth. Let’s touch on two as we head into Week 2 …
Love’s timeline, what Willis brings
Packers coach Matt LaFleur has kept the door open for Jordan Love (https://www.nytimes.com/athletic/nfl/player/jordan-love-hKoINpSJMsyZAYt3/) to possibly return for Sunday’s game against the Colts (https://www.nytimes.com/athletic/nfl/team/colts/), listing him as questionable. Though I’m told: “That’s not happening.” Love has an MCL sprain and has not been medically cleared to play.
The Packers are trying to keep all competitive advantages intact, which includes forcing opponents to prepare for all their QBs. While they hope Love’s is a week-to-week injury, the reality is that next week’s game against the Titans (https://www.nytimes.com/athletic/nfl/team/titans/) is considered by those in the know to be “a long shot.” The most optimistic timeline would have him back for Week 4 against the Vikings (https://www.nytimes.com/athletic/nfl/team/vikings/) if there are no snags. (The Packers face the Rams (https://www.nytimes.com/athletic/nfl/team/rams/) Week 5.)
Love is expected to wear a knee brace when he does return, for the protection and function of the knee. The quarterback has been seen around the building and at practice, taking mental reps. Meanwhile, less than three weeks ago Green Bay acquired QB Malik Willis (https://www.nytimes.com/athletic/nfl/player/malik-willis-SwMtBEALZsNIlnxh/) from the Titans. The Packers have used draft capital in three straight drafts on quarterbacks, selecting Sean Clifford (https://www.nytimes.com/athletic/nfl/player/sean-clifford-1K5peQmbHcWOMXaO/) (2023 fifth round) and Michael Pratt (https://www.nytimes.com/athletic/nfl/player/michael-pratt-USXddABsrjsowJMe/) (2024 seventh round, now with the Bucs practice squad after Green Bay released him), and acquiring Willis (for a 2025 seventh-round pick). They made this move believing Willis is a better option than Clifford, despite the second-year Packer having more time with LaFleur’s playbook.
""", "timestamp_start" : 0}, {"content" : """
GO DEEPER
Jones: Dolphins must exercise ultimate caution for Tua Tagovailoa's sake
 (https://www.nytimes.com/athletic/5765478/2024/09/13/tua-tagovailoa-health-future-dolphins-nfl/)
Saquon was almost a Texan
We all know the story by now (https://www.nytimes.com/athletic/5651393/2024/07/23/saquon-barkley-new-york-giants-hard-knocks-eagles/) — and if you don’t, go catch up on HBO’s “Hard Knocks” in which cameras followed Giants (https://www.nytimes.com/athletic/nfl/team/giants/) general manager Joe Schoen this past offseason. Giants owner John Mara probably won’t ever forget it either, telling Schoen, “I will lose sleep if we lose Barkley to the Eagles (https://www.nytimes.com/athletic/nfl/team/eagles/).” Well, Mara must not be getting much sleep these days (though for a few reasons).
Saquon Barkley (https://www.nytimes.com/athletic/nfl/player/saquon-barkley-NJxDrUdY0dwJPjnk/) left the New York Giants as a free agent and signed with their division rival. Then we saw his electric debut with Philadelphia (three touchdowns, named NFC Offensive Player of the Week). GM Howie Roseman gave the running back a three-year deal, worth almost $13 million annually. It was big money for the Penn State alum, who tested the free-agent market for the first time and won.
But Philly wasn’t the only team pushing to get Barkley in the building. The Houston Texans were aggressive in trying to land Barkley, but eventually were priced out. No worries for Houston; they traded for Joe Mixon (https://www.nytimes.com/athletic/nfl/player/joe-mixon-sKnyZX3WQEWatJVj/) from the Bengals instead.
Houston knew the Bengals had plans to release Mixon. To avoid losing him to the waiver wire, Houston traded a seventh-round draft pick. The RB also received a new three-year, $27 million contract that included $13 million guaranteed with a $6 million signing bonus. In his Texans debut, Mixon ran for 159 yards and a touchdown, taking AFC Offensive Player of the Week honors while the Bengals scored 10 points in an upset loss to the New England Patriots (https://www.nytimes.com/athletic/nfl/team/patriots/). Tough start for the exes.

Chase held in during training camp, but started Week 1 even without a new contract. (Jason Mowry / Getty Images)
Still no deal, but Ja’Marr Chase (https://www.nytimes.com/athletic/nfl/player/jamarr-chase-ToHiDqo1AnUHYTWK/) in ‘good spirits’
The Bengals didn’t s
pend any time wallowing around the building or practice field this week, fixating on the 77 yards of first-half offense they had in their home loss to New England.

Self-awareness is not an issue in that locker room.

The Bengals know the offense looked out of sync, that they couldn’t run the ball, and that the tackling was awful (they gave up 170 rushing yards). They know that won’t cut it against Patrick Mahomes and the Chiefs’ revamped wide receiver room.

Cincinnati’s own star receiver, 
Ja’Marr Chase (https://www.nytimes.com/athletic/nfl/player/jamarr-chase-ToHiDqo1AnUHYTWK/)
, played Week 1 despite not getting the big payday he’d been holding in for all of training camp. Chase was said to be in “good spirits” and practicing all week in Cincinnati. However, still no deal. We’ll see if they can get this finished soon.

As for this game, the Bengals’ ability to slow down a Chiefs offense that mirrors the 2021 edition will be the game plan of defensive coordinator Lou Anarumo. He’s done pretty well flustering Mahomes over the years, so much so fans have been donning 
“The Loufather” tees (https://newstripecity.com/products/the-loufather)
.

The Bengals are 3-2 against the Chiefs since 2022, and Anarumo’s defenses are a big reason why. In the past, he has successfully figured out how to simulate pressures, vary the looks and make Kansas City’s offense earn every yard. The same approach will be applied on Sunday, with red zone defense critical in forcing the Chiefs to kick field goals. The Chiefs see the Bengals as older and, at this moment, not built to lock up and defend, but they do believe Cincinnati has enough in its arsenal to mix coverages and pressures to force the Chiefs to earn their points via long scoring drives.
                              """, "timestamp_start" : 20}])

print(transcript_obj.summarize())

q_a_obj = "Based off the article, which quarterback seems to be projected to have the best season?"
print(transcript_obj.q_a('football', 10, q_a_obj))
