## Functionalities
### Data Analysis and Collection 
#### 1.Ranking of Individual Dishes by users
  Users click on a dish (affiliated with a dining hall), rate it, specify school and insert comments if desired
  *	Ranking scale: 1-5 
     1. represented by forks 
  *	Specify school affiliation  
     1. Select out of 5 possible choices 
     2. Used while no login system exists
  * Specific comment  
     1. 150 chars max  
     
#### 2.Ranking of individual Dining Halls by users
  Users click on a dinning hall, rate overall experience and leave additional comments  
  *	Ranking scale: 1-5 
    1. represented by forks 
  * Specify school affiliation
    1. Used while no login system exists 
    
#### 3.Display of data (Specifics TBD)
   Based on a specific query, user will be able to see certain data.     
  * Graphs with info based on query 
  * Info based on where students of a certain school eat 
  	1. Heat map of locations
  * Check for interesting patterns (?) 
#### 4.Recomendations (LEAST PRIORITY)
  System will give the user its own recomendations 
  * Need login system to implement 
  
    

###	 Queries (TBU)
Based on the certain queries, our system should return infon to the user 
#### 1.	Time/Meal 
   * What is open at a certain time/ certain meal (breakfast, dinner etc)
        1. Return Dining halls and specific menus for that time
#### 2.  Dish
   * Return when and where a certain dish is being served 
   * Return Bool with ingredients for a specfic dish (Does frary pasta contain flower?)
#### 3.	Ratings
  *	Return what are the best rated dining halls, dishes, meals 
#### 4. Dining Halls 
  * Return times of operation 
  * Return best rated meal per dining hall 
  * Return Menu for a dining hall at a specific day or time 

		
## Data Storage Info/Discussion
#### 1. Dishes
  Since there’s a ‘fixed’ number of actual dishes that can be served (IE: chicken, poke, tortellini)  dishes should be its separate table 
  * Each dinning hall serves a different dish (IE: Frary sushi != Frank Sushi) 
  * Specific dish attributes will be based off what can be scrapped (TBD) 
  * Each dish will have ingredients coming from ingredient table. 
    1.Probably some type of binary related to dish (corn, !cheese)
  * Ideally, each dish entry will be inputted with the scraper, but we might have to input info manually 
  * Dishes will link to rating and comment table 
  
#### 2. Ingredients 
  Since there’s a fixed number of ingredients by dish, these should be their own table
   * As of now, input these by hand. Could be helped with scraper. 
   * Brainstorm better ways of doing this
   * Link these with each specific dishes 
		
#### 3.	Dining Halls 
  Have these as their own table (Easy to do)
  * Store hours of operation
  * Link to ratings and comments 

#### 4. Ratings
  Stored as its own table
  *	Will have an ID 
  * Linked to a dish or dinning hall
  * Rating (1-5) + Comments
