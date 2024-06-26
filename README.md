# briend
a tool to help you keep your bookmarks in one place, analyze their content, and get the post on the tip of your tongue

this tool uses semantic search on text from social media platforms (twitter for now, image recognition and classification coming soon down the line).

## how it works

posts from x were scraped (through totally cool and non api usage terms violating ways, but message me if you want to know) then were extracted for the text content only, embedded, then stored in a db using postgres. 

we take the embedded text posts (using a local instance of nomic v-1.5) and run them against the embedded query after analyzing the user's intent from their first query, iteratively refining the query through prompting using chain of thought and in-context learning through optional clarifying questions presented to the user to be translated into a sql lookup query. this is not the intended final method to refine queries, as string-based prompts are unreliable at generating the target sql query at times--i plan to integrate dspy for a greater degree of controllability.

right now, the project uses only lexical lookup, with semantic search still in progress. 

the challege for right now is identifying the relevant metadata: traditional markers like timestamps and other baseline post metadata aren't enough to grab meaningful results through common search strategies like bm25--i'm using a similiarity score that often yields low accuracy results for the metric i want to measure for, which is user subjective intent. 

a post may have a very non-descript text that features the image as the main feature, and that in and of itself isn't straight-cut either... memespeak is hard to codify and often, it's in the collective knowledge of a certain ingroup (lol) that understands the signficance of the meme and what it's referring to. take this meme for example:

![Meme](/Users/gene/briend/samplepic/IMG_6822.JPG)

so if i were to run this with ocr, it'd recognize a
-boy
-a topological map
and read "shut up! my dad works for and can sell you overpriced n toolboxes h"
the fuck are you supposed to do with that? 

if you feed it to gpt4o, it'll get it, no sweat. the problem is reliably extracting the different elements from the picture through structured output that can then be funneled into the db to run a context-aware search.

but we don't want to use gpt4o, we wanna make some shit at home. i'm most likely going to end up several different tools and frameworks to address each element.

all that being said, if you happened to find this project and still want to run it even in its pre pre pre alpha state:

## set up:
> get a copy of ur data. for this version, we're grabbing x posts only (tiktok soon, in which case, go ahead and request your data through them, should take a couple of days. looking into proess to automate data exports rn)
> clone this repo
> start a python venv
> ```pip install requirements.txt```
> note where you saved your data, then run a couple of the cleaning scripts in src/data_ingestion/data_processing/cleaning. i got lazy. point the scripts to your where your data's located yourself brother. i should put up a one shot cleaning script soon, but just separate the metadata fields in the json and run it through some extra regex.
> grab a postgres db and put the details in a .env, change the filepath. run a couple sql queries to set up the schema or modify the code to just check if the fields are there and create it if it doesn't exist. again, LaZy
> run ``` python data_in.py ``` after changing the file path, it'll upload your data so you can run your first search
> grab a groq api key, or use your lm inference endpoint of your choice. they just use openai chat completions template anyway
>run ```python main_ai.py```, have fun 