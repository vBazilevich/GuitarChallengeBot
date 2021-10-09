# GuitarChallengeBot

[![codecov](https://codecov.io/gh/vBazilevich/GuitarChallengeBot/branch/master/graph/badge.svg?token=5IGPWEISYZ)](https://codecov.io/gh/vBazilevich/GuitarChallengeBot)
## Table of content

- [Project description](#desc)  
- [ Business goals and objectives ](#bus)
- [Use process](#usage)
- [Features](#feat)
- [Documentation](#doc)
- [How to deploy](#howto)
- [Technical stack](#tech)
- [Design decisions](#design)
- [Contibution](#contribute)
- [Licence](#license)
- [Authors](#authors)
 
<a id="desc"></a>
## Project Description
**[@DailyGuitarChallengeBot](https://t.me/DailyGuitarChallengeBot)**
A telegram bot that sends music scores to all users daily. Users can submit their performance in the form of audio or video messages. This sample will be forwarded to another user who will provide peer feedback:

-   approve that the music sample is exactly the melody as in the scores
-   give a numerical score for that sample

![img](https://drive.google.com/file/d/1qUiB97G5JKhsPkqO1zy5nbC7le_TXio7/view?usp=sharing)


### What problems it solves
This project is an opportunity to put knowledge into practice. A person is immersed in an environment of people with common interests, which helps to quickly implement new knowledge, try things out, and see immediate results and feedback from the community.

### Intended User
-   People interested in music, who lack practice and do not have the like-minded in their social circle.
-   People who want to share their experiences.

### Unique Selling Point
-   Subscription free
-   Get modern and actual music scores
-   In time feedback from people with the same interests
-   Random tracks from multiple genres, so the learning is never boring.

### Competitors
**Direct:** @easyguitarbot.
**Indirect:** @vocalolklipp, @iLyricsBot

### Potential Client (Business owner)
-   Organizers of *festivals*, *forums* where people come for the training program. They can use the bot as an extension of further interaction between forum participants.

-   Owners of *guitar training schools* (offline/online) where a person has a systematic business and can share a bot as a way of attracting new customers (not even that: give access to old students and they will just show their surroundings)

<a id="bus"></a>
##  **Business Goals and Objectives**

- We want to establish a new music community.

- We want a platform that will allow people to share their music skills.

- We want the platform to have a way to provide and receive peer feedback.

- We want the platform to provide daily challenges and engage the user to improve their learning and practicing.

- We want the platform to be a telegram-bot

<a id="usage"></a>
## Use process
1. Start the bot via */start* command
2. Use */help* command to get a list of commands with their description
3. Setup your schedule via */set_schedule* command. Schedule defines the time bot can send you messages. 
4. Check your schedule via *my_schedule* command
5. Get the new song score (notes) as a challenge via */next* command
6. Play a song and record it as an audio message
7. Get a full song name, after the audio recording is send 
8. Receive a numerical feedback from another user
9. Move to step 5

<a id="feat"></a>
## Features
### Current Features

- Users can setup their schedule
- Users can use help command
- Users can receive music score to play
- Users can send recorded music sample

### Future Features

- Users can receive a music score from another user for assessment
- Users can give and receive feedback
- Users can get the full song of a score name after they send their recording

### Futher Elaboration

Full use process and system behaviour can be found in the artifact 
available in the documentation section

<a id="doc"></a>
## Documentation
All development documentation can be found [here](https://drive.google.com/drive/folders/13jpxi0CbkD1b5aZgj5kuZGlEyuSJq9r5?usp=sharing)
###  Supplementary content of the Artifact
- Glossary
- Roles and responsibilities
- Requirement Analysis and Specifications
- Features
- User Stories
- Acceptance Criteria
- Non-functional requirements
- Software Development plan
- Constraints
- Software development plan
- System architecture

<a id="howto"></a>
## How to deploy?
1. Fork this repository
2. Create heroku application [link](https://devcenter.heroku.com/articles/creating-apps#creating-a-named-app)
3. Install Heroku PostgreSQL addon [link](https://www.heroku.com/postgres)
4. Create MongoDB cluster
5. Setup environment variables [link](https://devcenter.heroku.com/articles/config-vars)
6. Create PostgreSQL database using command:
 `heroku pg:psql -a <your-heroku-app-name> -f SQL/tables_creation.sql`
7. Register PostgreSQL functions using command:
 `heroku pg:psql -a <your-heroku-app-name> -f SQL/functions.sql`
9. Upload your scores using this [tool](https://github.com/vBazilevich/GuitarChallengeBot-scoresManagement) 
10. Go to your Heroku application and setup auto-deploy from the master branch of your fork.
11. Activate the dyno

### Environment variables explained
Obligatory environment variables:
* `TELEGRAM_API_TOKEN` - your bots' token. Here you can find detailed instructions on how to create a bot via a [link](https://core.telegram.org/bots#6-botfather)
* `MONGO_URL` - link to your MongoDB cluster. You can find it in connection settings of your cluster.

Environment variables required for running the bot locally:
* `DATABASE_URL` - by default Heroku sets it up when you add PostgreSQL addon to your application. However, there is no this variable
on your machine when you are running it locally.

Optional environment variables:
* `ADMIN_ID` - Telegram User ID that you can set up if you want to be notified on some events (for example, when one of the users has
finished all levels)

<a id="tech"></a>
## Technical Stack

Programming languages **- Python**

Databases **- postgreSQL, MongoDB**

Cloud CI platform **- Heroku.**

<a id="design"></a>
## Design Decisions

 **Hosting platform**

We have chosen Heroku as a hosting platform due to the following reasons:

1.  It is very popular, thus there are a lot of tutorials and already answered questions
2.  Free hobby plans
3.  Ease of deployment from the git repository
4.  Many useful addons

  

  **Images storage**

The product needs some storage where moderators can upload new Music Scores. That storage should be also accessed by the Bot to send those scores to end-users.

  

Two options were considered: AWS S3 and MongoDB. MongoDB was chosen due to the following reasons:

1.  No need for manually setting up the data replication
2.  Metadata can be stored in the same BSON object as image

  

However, the free tier MongoDB cluster has a limitation of 500MB. Therefore, we decided to move textual metadata (like the name of the song, the author, and the description) to a PostgreSQL database.

**User data storage**

For storing data storage we decided to use PostgreSQL due to the following reasons:

1.  Prior experience with PostgreSQL
2.  User-Assessor interactions can be naturally described by relations
3.  Heroku provides every application with a free PostgreSQL database limited to 1GB of size

<a id="contribute"></a>
## Contribution

Should you have any concern regarding contribution to this project, there are some options available:
1. Create a GitHub issue with a comprehensive bug description
2. Fork the repository, make your changes and create a pull request

<a id="license"></a>
## License

This product is licensed under **Apache 2.0** license. For further information about third party product licenses, please, refer to NOTICE file in the main repository.

<a id="authors"></a>
## Authors
Vladimir Bazilevich

Vladimir Bliznyukov



