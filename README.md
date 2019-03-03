### GROUP INFO
Members:
- Joni Heikkilä 
- Matti Valkeinen
- Heidi Vulli


### INTRODUCTION 
Our project is to create a web-app where one can add, play and buy games. This document will
go through the implementation of the project. We will keep this updated during the project.

##### LINK TO PROJECT

https://polar-anchorage-77658.herokuapp.com/

##### FEATURES WE'RE GOING TO IMPLEMENT
- Authentication
     * With email validation
     * Django authentication
- Basic player functionalities
- Basic developer functionalities
- Game/service interaction
- Own JavaScript game
- Save/load and resolution feature (Extra feature)
- Mobile friendly (Extra feature)

- We'll add more extra feature's once we are done with current ones

##### VIEWS
- Home
     * Everyone sees this
     * Has all games link which leads to search result with all games listed
- Register/Login
- Header
     * Has search, register, login and home as default links
     * Header is loaded into every page
          @ Different headers for player and developer
          @ Player has log out and your games instead of register & login
          @ Developer has log out game sales and add game instead of register & login
- Your games (player)
     * List of owned games
- Game sales (developer)
     * List of developed games
- Game window (player)
     * Has high scores, description and buy/play button depending on does player own the game
          @ If buy is activated then simple payment herokuapp is shown
          @ If play is activated then iframe is opened in the window with game's URL
- Game window (developer)
     * Has sale statistics of game and edit/remove button
     * Can't play games
- Add game (developer)
     * Has form for game's title, description, price & URL

##### MODELS
UPDATED FOR THE FINAL SUBMISSION
- User
     * username
     * isDeveloper (bool, if true user is developer)
     * isPlayer (bool, if true user is player
     * password
     * email
     * games (ManyToManyField)
     * emailConfirmed (default = False, when activaton link is used, True)
     * isActive
- Game
     * game_url
     * name
     * description
     * price
     * price_currency
     * developer_name
- Sales (created when game is added to shopcart)
     * player (foreign key to player)
     * date
     * games (ManyToManyField to games bougth)
     * totPrice (total price of the games)
     * status (default = "pending", when transaction complete then "ready")
- GameState
     * game (Foreign key to game)
     * player (Foreign key to player)
     * gamestate (contain all information in game state)
- GameScore
     * score
     * game (Foreign key to game)
     * player (Foreign key to player)

We added Project_plans.jpg in docs folder which shows connection of models and views.

##### ORDER OF PRODUCTION FOR FEATURES
- Creating templates for every window
     * The header will be shared layout for every page
- Creating models
     * Player, Developer, Game & Sales
- Navigation between windows
- Registration
     * Adding player/developer to database
     * Allow certain pages to certain people
- Adding games
- Playing games
- Buying games
- High scores of the games
- Search

##### PROJECT PRODUCTION PLAN
- We will try to meet up every week to discuss current stage of the project and what will try to do next
- Version control: Git
- Day-to-day communication: Telegram (joniheidimatti123!)
- We'll try to focus on own tasks that will not interfere with others' work
     * We'll make sure that everyone gets to try everything in the project


##### WEEKLY MEETINGS
21.3.
- Installed required tools to start the project for all group members.

26.3.
- Desided what should be done during Easter holidays.
     * Joni: Login template and back-end
     * Matti: Game template and back-end
     * Heidi: The base of other templates
6.4.
- Discussed what to do next:
     * Player: adding games to your_games (buying) (JONI)
          * Change your_games -> my_games
     * Names: change all names to correspond with projects name fex. game_window -> gamewindow (JOKU TM)
     * Game Window: make so that game_window checks if the player owns the game and fetches the
       game from User.games (fex. /gamestore/gamewindow?game=this-game fetches this-game and sets
       it to iframe) (HEIDI)
          * Apply responsive web desing for game windows iframe
     * NEW MODEL GameState: has unique_together in META so that user and game combined is the key
       and has gamestate data as json (MATTI)
          * Apply load request, load & save to gamewindow
     * If we have time we can think about highscores (JOKU TM)
     * Update README to correspond with the current project (MATTI)

13.4.
- Test and write a report on other group's games by Sunday (Matti&Joni)
- Discussed what to do:
     * Sales class is going to go through a rework -> ManyToManyField to games, purchase date, 
       etc (Joni)
          * Game statistics from this class to developer (Joni)
     * Existing game's modifying/deleting (Matti)
     * Email validation for user (JOKU TM)
     * Fix views.game_window to redirect to 404 if player does not own the game (JOKU TM)
     * Add buttons for playing games (Heidi)
          * Fix buttons for games you own (Heidi)
     * Scores (Matti)
     * Matti comments his code! (Matti)

23.4.
- Discussed the current state of the project
     * Button for playing games (HEIDI)
     * Make functions for search bar (MATTI)
     * Removing games from shopcart (JONI)
     * On can play without accepting the email link (JONI)
     * Documentation

### 26.4. The final meetings

In this chapter discussed how we did on our project, what went well, what did not go so well, what was our justification in our decisions in project and how the workload divided between members.

#### What went well
We succeeded to implement all major features we wanted and we managed to stay in schedule. We also learned lot from django and web programming. Alltogether we did pretty well, the website works and our team is still intact.

#### Difficulties
One of our group member had problems with PostgreSQL whole time. We also had many other projects at the same time, so we did not have enough time polish all the details of our project that we would have wanted.

#### Reasons behind design choises
There were only few bigger desing choices considering the project and we will not list any of the minor ones here. First of all we decided that we made a separate sales model where we keep track of the transactions instead of keeping track of them with foreign keys in game. We decided to use Django's built in templates and forms to avoid unnecessary code. We used bootstraps also to avoid repeat the code (copy-paste). We took advantage of the project work handout so we managed to avoid some of the necessary decicions.

#### Who did what
Heidi focused on the frontside of the project because she had problems with the postgres on her computer and she's also interested in the field. Joni made the authetication, statistics and buying. Matti made game window, adding and modifying of the games and search. Everyone also did something little things but those were the main responsibilities of the project. We think that the work load was equally divided.