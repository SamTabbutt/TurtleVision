# TurtleVision
This is very much so a work in progress.

  TurtleVision is a project that is an effort to accomplish multiple goals through one web-application.

  The most important function of the site is to collect and analyze marine ecology data via the process of deep neural network   learning.  

  The website will have one broad backend function: to take in data input stored from users and classify the hundreds of hours   of video data we have.The website is constructed with postgreSQL on a django framework. It makes use of CV2 and pillow to       gather matrices from mp4 videos and uses MXNET GLUON to achieve deep neural network learning. 

Program structure:

  The code is structured in a Django framework. Their are three main functions: Upload, Train, and Trust. 

  Upload -- The user is able to upload entire TurtleCam sessions with an assiociated CSV log which was created along with the     TurtleCam footage. This creates an instance of Second Data for each second in the session-- This is an unesecarry step along   the way which doesn't need to exist. The creation of second data could rather be created in the DataAnalyze layer of the       program. 

  Train -- the user is able to log example frames of "breath" or "apnea" to be used as training data for the neural network

  Trust -- the user is able to run a training loop for all the collected data to create a neural network through MXNet gluon.     The user is then able to apply the neural network model to the entire session to get a label for each second which declares     the "breath status" for each second
  
  The structure of the python backend is not "air-tight", but is based on the concept of having separate layers which             communicate with other specific individual layers. The urls direct to the view patterns, which are meant to interact with the   data manage pattern which is meant to interact with the SQLite database and the data Analyze layer, which is meant to           interact with the SQLite database. As it currently stands there are many "leaks" in this system.
  
  Each interaction with the backend from the user interface is meant to communicate through jQuery Ajax requests or "vanilla"     HTTP requests through Django's request-response libraries.

If you have come across this repository please feel free to reach out to me at samtabbutt@gmail.com with any questions or suggestions.
