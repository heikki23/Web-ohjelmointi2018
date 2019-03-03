$ GROUP INFO $
Members: 
- Joni Heikkilä 234035 joni.heikkila@student.tut.fi
- Matti Valkeinen 246396 matti.valkeinen@student.tut.fi 
- Heidi Vulli 240098 heidi.vulli@student.tut.fi
Group name: g-023

$ INTRODUCTION $
Our project is to create a web-app where one can add, play and buy games. This document will
go through the implementation of the project. We will keep this updated during the project.

$ FEATURES WE’RE GOING TO IMPLEMENT $
- Authentication
     * With email validation
     * Django authentication
- Basic player functionalities
- Basic developer functionalities
- Game/service interaction
- Own JavaScript game
- Save/load and resolution feature (Extra feature)
- Mobile friendly (Extra feature)

- We’ll add more extra feature’s once we are done with current ones

$ VIEWS $
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
          @ If play is activated then iframe is opened in the window with game’s URL
- Game window (developer)
     * Has sale statistics of game and edit/remove button
     * Can’t play games 
- Add game (developer)
     * Has form for game’s title, description, price & URL

$ MODELS $
- Player
     * Name
     * Username
     * Email
     * Password
     * Games
- Developer
     * Name
     * Username
     * Email
     * Password
     *Games
- Game
     * URL
     * Name
     * Description
     * Price
     * High score
- Sales
     * Foreign key to game
     * Buyer (foreign key to player)
     * Date
We added Project_plans.jpg which shows connection of models and views.

$ ORDER OF PRODUCTION FOR FEATURES $
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

$ PROJECT PRODUCTION PLAN $
- We will try to meet up every week to discuss current stage of the project and what will try to do next
- Version control: Git
- Day-to-day communication: Telegram (joniheidimatti123!)
- We’ll try to focus on own tasks that will not interfere with others’ work
     * We’ll make sure that everyone gets to try everything in the project

$ WEEKLY MEETINGS $
21.3.
- Installed required tools to start the project for all group members.
26.3.
- Desided what should be done during Easter holidays. 
     * Joni: Login template and back-end
     * Matti: Game template and back-end
     * Heidi: The base of other templates