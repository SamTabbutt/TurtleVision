# TurtleVision
Another attempt at establishing backend for turtlevision


TurtleVision is a project that is an effort to accomplish multiple goals through one web-experiment.

The most important function of the site is to get TurtleCam footage (owned by Nathan J. Robinson PhD) on the internet in an accessible and interactive way.

Not only is the site an opportunity to get the experience of a sea turtle on to everyone's home computer, but it is also to experiment with the prospect of 
collecting and analyzing marine ecology data via the process of deep neural network learning. The scientific field of marine ecology is an incredibly qualitative field,
and we are curious of the quantitative opportunities held within those qualities which are analyzed. 

The website will have one broad backend function: to take in data input stored from users and classify the hundreds of hours of video data we have.
The website is constructed with postgreSQL on a django framework. It makes use of CV2 and pillow to gather matrices from mp4 videos and uses MXNET GLUON to achieve
deep neural network learning. 

In its current state, the website is in need of some crucial aspects before it is ready to be deployed and marketed to schools around the world.

If you have come across this repository please feel free to reach out to me at samtabbutt@gmail.com with any questions or suggestions.
