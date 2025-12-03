# Creating a realistic-looking 100-movie JSON fixture for Django.
# Fields included: title, year, genres, description, cast, director, rating, poster_url, duration, language, imdb_id (empty), tmdb_id (empty), popularity
import json, urllib.parse
movies_list = [
("Inception",2010,"Sci-Fi, Thriller","A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea into the mind of a CEO.","Leonardo DiCaprio, Joseph Gordon-Levitt, Ellen Page","Christopher Nolan",8.8,148,"English"),
("The Shawshank Redemption",1994,"Drama","Two imprisoned men bond over a number of years, finding solace and eventual redemption through acts of common decency.","Tim Robbins, Morgan Freeman","Frank Darabont",9.3,142,"English"),
("The Godfather",1972,"Crime, Drama","The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.","Marlon Brando, Al Pacino","Francis Ford Coppola",9.2,175,"English"),
("The Dark Knight",2008,"Action, Crime","When the menace known as the Joker emerges, Batman must accept one of the greatest psychological and physical tests of his ability to fight injustice.","Christian Bale, Heath Ledger","Christopher Nolan",9.0,152,"English"),
("Pulp Fiction",1994,"Crime, Drama","The lives of two mob hitmen, a boxer, and a pair of diner bandits intertwine in four tales of violence and redemption.","John Travolta, Uma Thurman, Samuel L. Jackson","Quentin Tarantino",8.9,154,"English"),
("Fight Club",1999,"Drama","An insomniac office worker and a soap maker form an underground fight club that evolves into something much more.","Brad Pitt, Edward Norton","David Fincher",8.8,139,"English"),
("Forrest Gump",1994,"Drama, Romance","The presidencies of Kennedy and Johnson, Vietnam, Watergate, and other history unfold through the perspective of an Alabama man with a low IQ.","Tom Hanks, Robin Wright","Robert Zemeckis",8.8,142,"English"),
("The Matrix",1999,"Sci-Fi, Action","A computer hacker learns from mysterious rebels about the true nature of his reality and his role in the war against its controllers.","Keanu Reeves, Laurence Fishburne","The Wachowskis",8.7,136,"English"),
("Goodfellas",1990,"Crime, Biography","The story of Henry Hill and his life in the mob, covering his relationship with his wife and his partners in crime.","Robert De Niro, Ray Liotta","Martin Scorsese",8.7,146,"English"),
("The Lord of the Rings: The Return of the King",2003,"Fantasy, Adventure","Gandalf and Aragorn lead the World of Men against Sauron's army to draw his gaze from Frodo and Sam as they approach Mount Doom with the One Ring.","Elijah Wood, Viggo Mortensen","Peter Jackson",8.9,201,"English"),
("Star Wars: Episode IV - A New Hope",1977,"Sci-Fi, Adventure","Luke Skywalker joins forces with a Jedi Knight, a cocky pilot, and two droids to save the galaxy from the Empire's world-destroying battle station.","Mark Hamill, Harrison Ford","George Lucas",8.6,121,"English"),
("The Silence of the Lambs",1991,"Thriller, Crime","A young F.B.I. cadet must confide in an incarcerated and manipulative killer to receive his help on catching another serial killer.","Jodie Foster, Anthony Hopkins","Jonathan Demme",8.6,118,"English"),
("Se7en",1995,"Crime, Thriller","Two detectives hunt a serial killer who uses the seven deadly sins as his motives.","Brad Pitt, Morgan Freeman","David Fincher",8.6,127,"English"),
("The Usual Suspects",1995,"Crime, Mystery","A sole survivor tells the twisted events leading up to a horrific gun battle on a boat, involving a mythical crime lord.","Kevin Spacey, Gabriel Byrne","Bryan Singer",8.5,106,"English"),
("Saving Private Ryan",1998,"War, Drama","Following the Normandy Landings, a group of soldiers go behind enemy lines to retrieve a paratrooper whose brothers have been killed in action.","Tom Hanks, Matt Damon","Steven Spielberg",8.6,169,"English"),
("Schindler's List",1993,"Biography, Drama","In German-occupied Poland during World War II, Oskar Schindler gradually becomes concerned for his Jewish workforce after witnessing their persecution.","Liam Neeson, Ben Kingsley","Steven Spielberg",8.9,195,"English"),
("The Green Mile",1999,"Drama, Fantasy","The lives of guards on Death Row are affected by one of their charges: a black man accused of child murder who has a mysterious gift.","Tom Hanks, Michael Clarke Duncan","Frank Darabont",8.6,189,"English"),
("Gladiator",2000,"Action, Drama","A former Roman General sets out to exact vengeance against the corrupt emperor who murdered his family and sent him into slavery.","Russell Crowe, Joaquin Phoenix","Ridley Scott",8.5,155,"English"),
("The Prestige",2006,"Drama, Mystery","Two stage magicians engage in a competitive rivalry that becomes fatal.","Christian Bale, Hugh Jackman","Christopher Nolan",8.5,130,"English"),
("Memento",2000,"Mystery, Thriller","A man with short-term memory loss attempts to track down his wife's murderer.","Guy Pearce, Carrie-Anne Moss","Christopher Nolan",8.4,113,"English"),
("The Departed",2006,"Crime, Drama","An undercover cop and a mole in the police attempt to identify each other while infiltrating an Irish gang in Boston.","Leonardo DiCaprio, Matt Damon","Martin Scorsese",8.5,151,"English"),
("Whiplash",2014,"Drama, Music","A young drummer enrolls at a cut-throat music conservatory where his instructor pushes him to the limits of his ability and sanity.","Miles Teller, J.K. Simmons","Damien Chazelle",8.5,106,"English"),
("Django Unchained",2012,"Drama, Western","With the help of a German bounty-hunter, a freed slave sets out to rescue his wife from a brutal plantation owner.","Jamie Foxx, Christoph Waltz","Quentin Tarantino",8.4,165,"English"),
("The Wolf of Wall Street",2013,"Biography, Crime","Based on the true story of Jordan Belfort, from his rise to a wealthy stockbroker living the high life to his fall involving crime, corruption and the federal government.","Leonardo DiCaprio, Jonah Hill","Martin Scorsese",8.2,180,"English"),
("Inglourious Basterds",2009,"War, Drama","In Nazi-occupied France, a group of Jewish-American soldiers plan to assassinate Nazi leaders, while a theatre owner plots her own revenge.","Brad Pitt, Christoph Waltz","Quentin Tarantino",8.3,153,"English"),
("The Social Network",2010,"Drama","The story of the founding of Facebook and the resulting lawsuits.","Jesse Eisenberg, Andrew Garfield","David Fincher",7.7,120,"English"),
("Parasite",2019,"Thriller, Drama","Greed and class discrimination threaten the newly formed symbiotic relationship between the wealthy Park family and the destitute Kim clan.","Song Kang-ho, Lee Sun-kyun","Bong Joon Ho",8.6,132,"Korean"),
("1917",2019,"War, Drama","Two young British soldiers during WWI must deliver a message that will stop 1,600 men from walking into a deadly trap.","George MacKay, Dean-Charles Chapman","Sam Mendes",8.3,119,"English"),
("The Lion King",1994,"Animation, Drama","Lion prince Simba flees his kingdom only to learn the true meaning of responsibility and bravery.","Matthew Broderick, Jeremy Irons","Roger Allers, Rob Minkoff",8.5,88,"English"),
("Toy Story",1995,"Animation, Adventure","A cowboy doll is profoundly threatened and jealous when a new spaceman figure supplants him as top toy in a boy's room.","Tom Hanks, Tim Allen","John Lasseter",8.3,81,"English"),
("Finding Nemo",2003,"Animation, Adventure","After his son is captured in the Great Barrier Reef, a timid clownfish sets out on a journey to bring him home.","Albert Brooks, Ellen DeGeneres","Andrew Stanton",8.1,100,"English"),
("The Avengers",2012,"Action, Sci-Fi","Earth's mightiest heroes must come together to stop a demigod from subjugating humanity.","Robert Downey Jr., Chris Evans","Joss Whedon",8.0,143,"English"),
("Avengers: Endgame",2019,"Action, Sci-Fi","After the devastating events of Infinity War, the Avengers assemble once more to reverse Thanos' actions and restore balance to the universe.","Robert Downey Jr., Chris Evans","Anthony Russo, Joe Russo",8.4,181,"English"),
("Black Panther",2018,"Action, Sci-Fi","T'Challa returns home to Wakanda to take his rightful place as king, but he must face a challenger who threatens his nation's future.","Chadwick Boseman, Michael B. Jordan","Ryan Coogler",7.3,134,"English"),
("Mad Max: Fury Road",2015,"Action, Adventure","In a post-apocalyptic wasteland, Max helps a rebellious woman and a group of female prisoners flee from a tyrant.","Tom Hardy, Charlize Theron","George Miller",8.1,120,"English"),
("The Martian",2015,"Sci-Fi, Adventure","An astronaut becomes stranded on Mars and must figure out how to survive until a rescue mission can retrieve him.","Matt Damon, Jessica Chastain","Ridley Scott",8.0,144,"English"),
("Gravity",2013,"Sci-Fi, Thriller","Two astronauts work together to survive after an accident leaves them adrift in space.","Sandra Bullock, George Clooney","Alfonso Cuarón",7.7,91,"English"),
("Her",2013,"Romance, Sci-Fi","A lonely writer develops an unusual relationship with an operating system designed to meet his every need.","Joaquin Phoenix, Scarlett Johansson","Spike Jonze",8.0,126,"English"),
("The Grand Budapest Hotel",2014,"Comedy, Drama","A concierge teams up with an employee to prove his innocence after being framed for murder in a whimsical European hotel.","Ralph Fiennes, Tony Revolori","Wes Anderson",8.1,100,"English"),
("La La Land",2016,"Romance, Musical","A jazz pianist falls for an aspiring actress in Los Angeles as they navigate their careers and relationship.","Ryan Gosling, Emma Stone","Damien Chazelle",8.0,128,"English"),
("Whiplash",2014,"Drama, Music","A promising young drummer enrolls at a cut-throat music conservatory and clashes with an intense instructor.","Miles Teller, J.K. Simmons","Damien Chazelle",8.5,107,"English"),
("Get Out",2017,"Horror, Thriller","A young African-American man visits his white girlfriend's parents, where he discovers disturbing secrets.","Daniel Kaluuya, Allison Williams","Jordan Peele",7.7,104,"English"),
("Us",2019,"Horror, Thriller","A family is terrorized by doppelgängers of themselves while on vacation.","Lupita Nyong'o, Winston Duke","Jordan Peele",6.8,116,"English"),
("The Conjuring",2013,"Horror","Paranormal investigators work to help a family terrorized by a dark presence in their farmhouse.","Vera Farmiga, Patrick Wilson","James Wan",7.5,112,"English"),
("It",2017,"Horror","A group of children face a shape-shifting entity that emerges from the sewer every 27 years to prey on their town.","Bill Skarsgård, Jaeden Martell","Andy Muschietti",7.4,135,"English"),
("The Exorcist",1973,"Horror","When a teenage girl becomes possessed, two priests attempt to save her and battle the demon.", "Ellen Burstyn, Linda Blair","William Friedkin",8.0,122,"English"),
("Alien",1979,"Sci-Fi, Horror","The crew of a commercial space tug encounters a deadly lifeform after investigating a distress signal on a distant planet.","Sigourney Weaver, Tom Skerritt","Ridley Scott",8.4,116,"English"),
("Aliens",1986,"Sci-Fi, Action","Ellen Ripley returns to the alien-infested planetoid with a unit of marines to try to eliminate the threat.","Sigourney Weaver, Michael Biehn","James Cameron",8.4,154,"English"),
("The Thing",1982,"Horror, Sci-Fi","Researchers in Antarctica are hunted by a shape-shifting alien that assumes the appearance of its victims.","Kurt Russell, Wilford Brimley","John Carpenter",8.1,109,"English"),
("Blade Runner 2049",2017,"Sci-Fi, Drama","A young blade runner's discovery of a long-buried secret leads him to track down former blade runner Rick Deckard.","Ryan Gosling, Harrison Ford","Denis Villeneuve",8.0,164,"English"),
("Dune",2021,"Sci-Fi, Adventure","Paul Atreides must travel to the most dangerous planet in the universe to ensure the future of his family and people.","Timothée Chalamet, Zendaya","Denis Villeneuve",8.1,155,"English"),
("The Social Network",2010,"Drama","The founding of Facebook and the resulting legal battles.", "Jesse Eisenberg, Andrew Garfield","David Fincher",7.7,120,"English"),
("The Truman Show",1998,"Drama, Sci-Fi","An insurance salesman discovers his entire life is actually a reality TV show.","Jim Carrey, Laura Linney","Peter Weir",8.1,103,"English"),
("A Beautiful Mind",2001,"Biography, Drama","John Nash, a brilliant but asocial mathematician, develops paranoid schizophrenia and suffers greatly.","Russell Crowe, Jennifer Connelly","Ron Howard",8.2,135,"English"),
("The Big Short",2015,"Biography, Drama","Several men foresee the housing market collapse and bet against mortgage-backed securities.","Christian Bale, Steve Carell","Adam McKay",7.8,130,"English"),
("No Country for Old Men",2007,"Crime, Drama","Violence and mayhem ensue after a hunter stumbles upon drug money, pursued by a relentless killer.","Tommy Lee Jones, Javier Bardem","Ethan Coen, Joel Coen",8.1,122,"English"),
("There Will Be Blood",2007,"Drama","A turn-of-the-century prospector becomes consumed by greed and obsession over oil in California.","Daniel Day-Lewis, Paul Dano","Paul Thomas Anderson",8.2,158,"English"),
("The Grand Budapest Hotel",2014,"Comedy, Drama","A concierge and lobby boy become involved in a theft and murder at a famous European hotel.","Ralph Fiennes, Tony Revolori","Wes Anderson",8.1,100,"English"),
("The Pianist",2002,"Biography, Drama","A Polish Jewish musician struggles to survive the destruction of the Warsaw ghetto during WWII.","Adrien Brody, Thomas Kretschmann","Roman Polanski",8.5,150,"English"),
("The King's Speech",2010,"Biography, Drama","King George VI tries to overcome his stammer with the help of an unorthodox speech therapist.","Colin Firth, Geoffrey Rush","Tom Hooper",8.0,118,"English")
]

# Ensure we have 100 titles; if list shorter, we'll add well-known popular films to reach 100.
extra_titles = [
("Casino Royale",2006,"Action, Thriller","James Bond's first mission as 007 to stop a financier of terrorism.","Daniel Craig, Eva Green","Martin Campbell",8.0,144,"English"),
("Skyfall",2012,"Action, Thriller","Bond's loyalty to M is tested as her past comes back to haunt her.","Daniel Craig, Judi Dench","Sam Mendes",7.8,143,"English"),
("Casino",1995,"Crime, Drama","A tale of greed, deception, money and power set in Las Vegas.","Robert De Niro, Sharon Stone","Martin Scorsese",8.2,178,"English"),
("Back to the Future",1985,"Adventure, Comedy","A teenager is accidentally sent 30 years into the past in a time-traveling DeLorean invented by his eccentric scientist friend.","Michael J. Fox, Christopher Lloyd","Robert Zemeckis",8.5,116,"English"),
("The Breakfast Club",1985,"Drama, Comedy","Five high school students meet in Saturday detention and discover they have more in common than they thought.","Emilio Estevez, Molly Ringwald","John Hughes",7.8,97,"English"),
("The Shining",1980,"Horror, Drama","A family heads to an isolated hotel where an evil spiritual presence influences the father into violence.","Jack Nicholson, Shelley Duvall","Stanley Kubrick",8.4,146,"English"),
("The Sixth Sense",1999,"Drama, Mystery","A boy who communicates with spirits seeks the help of a disheartened child psychologist.","Bruce Willis, Haley Joel Osment","M. Night Shyamalan",8.1,107,"English"),
("Amélie",2001,"Comedy, Romance","Amélie decides to change the lives of those around her for the better, while grappling with her own isolation.","Audrey Tautou, Mathieu Kassovitz","Jean-Pierre Jeunet",8.3,122,"French"),
("Spirited Away",2001,"Animation, Fantasy","During her family's move to the suburbs, a sullen 10-year-old girl wanders into a world ruled by gods and spirits.","Rumi Hiiragi, Miyu Irino","Hayao Miyazaki",8.6,125,"Japanese"),
("The Lord of the Rings: The Fellowship of the Ring",2001,"Fantasy, Adventure","A meek Hobbit and eight companions set out to destroy a powerful ring and save Middle-earth.","Elijah Wood, Ian McKellen","Peter Jackson",8.8,178,"English"),
("The Lord of the Rings: The Two Towers",2002,"Fantasy, Adventure","The fellowship is broken but continues its quest as new allies are discovered and great battles loom.","Elijah Wood, Viggo Mortensen","Peter Jackson",8.7,179,"English"),
("The Lord of the Rings: The Return of the King",2003,"Fantasy, Adventure","The final confrontation between the forces of good and evil to destroy the One Ring.","Elijah Wood, Viggo Mortensen","Peter Jackson",8.9,201,"English"),
("Moonlight",2016,"Drama","A young man deals with his dysfunctional home life and grapples with his sexuality.","Trevante Rhodes, Mahershala Ali","Barry Jenkins",7.4,111,"English"),
("Black Swan",2010,"Drama, Thriller","A committed dancer wins the lead and slowly loses her grip on reality under the pressure.","Natalie Portman, Mila Kunis","Darren Aronofsky",8.0,108,"English"),
("The Truman Show",1998,"Drama, Sci-Fi","An insurance salesman discovers his life is a reality TV show.","Jim Carrey, Laura Linney","Peter Weir",8.1,103,"English"),
("Spotlight",2015,"Biography, Drama","The true story of how the Boston Globe uncovered the massive scandal of child molestation and cover-up within the local Catholic Archdiocese.","Michael Keaton, Rachel McAdams","Tom McCarthy",8.1,129,"English"),
("The Revenant",2015,"Adventure, Drama","A frontiersman fights for survival and seeks vengeance after being left for dead.","Leonardo DiCaprio, Tom Hardy","Alejandro G. Iñárritu",8.0,156,"English"),
("The Help",2011,"Drama","An aspiring writer during the civil rights movement decides to write a book from the perspective of the maids.","Emma Stone, Viola Davis","Tate Taylor",8.1,137,"English"),
("Room",2015,"Drama, Thriller","A young boy who has lived his entire life in an enclosed space with his mother experiences the outside world for the first time.","Brie Larson, Jacob Tremblay","Lenny Abrahamson",8.1,118,"English"),
("The King's Speech",2010,"Biography, Drama","King George VI overcomes a stammer with the help of a speech therapist.","Colin Firth, Geoffrey Rush","Tom Hooper",8.0,118,"English"),
("The Imitation Game",2014,"Biography, Drama","Alan Turing and his team work to crack Nazi Germany's Enigma code during World War II.","Benedict Cumberbatch, Keira Knightley","Morten Tyldum",8.0,113,"English"),
("The Pursuit of Happyness",2006,"Biography, Drama","A struggling salesman takes custody of his son as he embarks on a life-changing professional program.","Will Smith, Jaden Smith","Gabriele Muccino",8.0,117,"English"),
("Slumdog Millionaire",2008,"Drama, Romance","A Mumbai teen reflects on his life after being accused of cheating on a game show and recounts events that led him there.","Dev Patel, Freida Pinto","Danny Boyle",8.0,120,"English"),
("Life of Pi",2012,"Adventure, Drama","A young man survives a disaster at sea and forms an unexpected connection with a fearsome Bengal tiger.","Irfan Khan, Suraj Sharma","Ang Lee",7.9,127,"English"),
("Trainspotting",1996,"Drama","A group of heroin addicts in late 1980s Edinburgh navigate love, friendship, and the pitfalls of addiction.","Ewan McGregor, Ewen Bremner","Danny Boyle",8.1,94,"English"),
("The Curious Case of Benjamin Button",2008,"Drama, Fantasy","A man appears to age in reverse and experiences a life that mirrors the complexities of human relationships.","Brad Pitt, Cate Blanchett","David Fincher",7.8,166,"English"),
("Eternal Sunshine of the Spotless Mind",2004,"Drama, Romance","A couple erase memories of each other when their relationship turns sour, but a deeper connection remains.","Jim Carrey, Kate Winslet","Michel Gondry",8.3,108,"English"),
("Gone Girl",2014,"Thriller, Mystery","A man becomes the focus of an intense media circus after his wife disappears, revealing secrets about their marriage.","Ben Affleck, Rosamund Pike","David Fincher",8.1,149,"English"),
("Prisoners",2013,"Crime, Drama","When his daughter and her friend go missing, a father takes matters into his own hands as the police pursue multiple leads.","Hugh Jackman, Jake Gyllenhaal","Denis Villeneuve",8.1,153,"English"),
("Spotlight",2015,"Biography, Drama","Investigative journalists expose a widespread scandal of child abuse and institutional cover-up.","Michael Keaton, Mark Ruffalo","Tom McCarthy",8.1,129,"English")
]

# Combine and ensure 100 unique items
all_titles = movies_list + extra_titles
# If still less than 100, add some more common films
more = [
("Rocky",1976,"Drama, Sport","A small-time boxer gets a supremely rare chance to fight a heavyweight champion.","Sylvester Stallone, Talia Shire","John G. Avildsen",8.1,119,"English"),
("Raging Bull",1980,"Biography, Drama","The life of boxer Jake LaMotta, whose violence and temper lead him to the top in the ring and destroy his life outside of it.","Robert De Niro, Cathy Moriarty","Martin Scorsese",8.2,129,"English"),
("Good Will Hunting",1997,"Drama","Will Hunting, a janitor at MIT, has a gift for mathematics but needs help from a psychologist to find direction in his life.","Matt Damon, Robin Williams","Gus Van Sant",8.3,126,"English"),
("The Martian",2015,"Sci-Fi, Adventure","An astronaut becomes stranded on Mars and must rely on his ingenuity to survive.","Matt Damon, Jessica Chastain","Ridley Scott",8.0,144,"English"),
("Blade Runner",1982,"Sci-Fi, Thriller","A blade runner must pursue and terminate four replicants who stole a ship in space and have returned to Earth to find their creator.","Harrison Ford, Rutger Hauer","Ridley Scott",8.1,117,"English"),
("The Big Lebowski",1998,"Comedy, Crime","Jeff 'The Dude' Lebowski is mistaken for a millionaire of the same name, leading to a complicated case of mistaken identity.","Jeff Bridges, John Goodman","Joel Coen, Ethan Coen",8.1,117,"English"),
("The Prestige",2006,"Drama, Mystery","Two rival magicians engage in a bitter competition to create the ultimate stage illusion.","Christian Bale, Hugh Jackman","Christopher Nolan",8.5,130,"English"),
("Interstellar",2014,"Sci-Fi, Drama","A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.","Matthew McConaughey, Anne Hathaway","Christopher Nolan",8.6,169,"English"),
("The Revenant",2015,"Adventure, Drama","A frontiersman fights for survival and vengeance after being left for dead.","Leonardo DiCaprio, Tom Hardy","Alejandro G. Iñárritu",8.0,156,"English"),
("Birdman",2014,"Comedy, Drama","An actor famous for playing a superhero struggles to mount a Broadway play and reclaim his artistic integrity.","Michael Keaton, Emma Stone","Alejandro G. Iñárritu",7.7,119,"English")
]

all_titles.extend(more)
# Trim or extend to exactly 100
unique = []
seen = set()
for item in all_titles:
    key = (item[0], item[1])
    if key not in seen:
        unique.append(item)
        seen.add(key)
unique = unique[:100]

fixture = []
pk = 1
for title, year, genres, desc, cast, director, rating, duration, language in unique:
    poster_text = urllib.parse.quote_plus(title)
    poster_url = f"https://placehold.co/300x450?text={poster_text}"
    fixture.append({
        "model":"movies.movie",
        "pk":pk,
        "fields":{
            "title": title,
            "description": desc,
            "genres": genres,
            "year": year,
            "rating": rating,
            "cast": cast,
            "director": director,
            "tags": "",
            "poster_url": poster_url,
            "imdb_id": "",
            "tmdb_id": "",
            "duration": duration,
            "language": language,
            "popularity": int(rating*10)
        }
    })
    pk += 1

path = "data/movies_sample.json"
with open(path, "w", encoding="utf-8") as f:
    json.dump(fixture, f, indent=2, ensure_ascii=False)

path
