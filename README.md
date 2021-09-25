# GuitarChallengeBot
[![codecov](https://codecov.io/gh/vBazilevich/GuitarChallengeBot/branch/master/graph/badge.svg?token=5IGPWEISYZ)](https://codecov.io/gh/vBazilevich/GuitarChallengeBot)

## Project description
This bot sends a piece of music in form of scores to all users every day.

User can submit his or her performance in form of audio or video message.
This message will be forwarded to another user who will approve that first user
plays exactly the same melody as in the scores. Reviewer can also provide a feedback.

## Documentation
All development documentation can be found [here](https://drive.google.com/drive/folders/13jpxi0CbkD1b5aZgj5kuZGlEyuSJq9r5?usp=sharing)

## How to deploy?
1. Fork this repository
2. [Create heroku application](https://devcenter.heroku.com/articles/creating-apps#creating-a-named-app)
3. [Install Heroku PostgreSQL addon](https://www.heroku.com/postgres)
4. Create MongoDB cluster
5. [Setup environment variables](https://devcenter.heroku.com/articles/config-vars)
6. Create PostgreSQL database using command `heroku pg:psql -a <your-heroku-app-name> -f SQL/tables_creation.sql`
7. Register PostgreSQL functions using command `heroku pg:psql -a <your-heroku-app-name> -f SQL/functions.sql`
8. Upload your scores using this [tool](https://github.com/vBazilevich/GuitarChallengeBot-scoresManagement) 
9. Go to your Heroku application and setup auto-deploy from the master branch of your fork.
10. Activate the dyno

### Environment variables explained
Obligatory environment variables:
* `TELEGRAM_API_TOKEN` - your bots' token. Here you can find detailed [instructions](https://core.telegram.org/bots#6-botfather) on how to create a bot.
* `MONGO_URL` - link to your MongoDB cluster. You can find it in connection settings of your cluster.

Environment variables required for running the bot locally:
* `DATABASE_URL` - by default Heroku sets it up when you add PostgreSQL addon to your application. However, there is no this variable
on your machine when you are running it locally.

Optional environment variables:
* `ADMIN_ID` - Telegram User ID that you can set up if you want to be notified on some events (for example, when one of the users has
finished all levels)

## Authors
Vladimir Bazilevich

Vladimir Bliznyukov
