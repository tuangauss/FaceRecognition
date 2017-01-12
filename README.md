# Facial_recognition

Project implemented in Python and Flask that allows users to identify which celebrities they resemble the most by using Microsoft Cognitive Service API to analyze a photo

This readme.md provides concise information about the project. To have a better idea of the overall design and implementation, please kindly refer to ```documentation.txt``` , ```design.txt``


## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.

### Prerequisites

Project uses many external resources, as supplements and inspiration, notably:
* Microsoft Cognitive Service API
* Dropbox API
* webcam.js
* Flask
* Yale/Harvard CS50's HTML design

To run the program, you need to register to have a Microsoft Cognitive Service API key and Dropbox API key.

Then, export the key to your environment
```
export Microsoft_key=your_key
```

```
export Dropbox_key=your_key
```

### Running:

There are several steps you have to do before you can actually test the program. They are as follows:
1. Export your keys
2. Configure dropbox
3. Build your database of faces in SQL
4. Up and running

Please refer to ```documentation.txt``` , ```design.txt`` for more details

* <i>The result will look more or less like this: </i>
![picture alt](https://dl.dropboxusercontent.com/s/bgm5afv60y80iie/15271969_1182880761758998_8380260523108213761_o.jpg)

* I have made a short Youtube [video](https://youtu.be/-9il1HhM4F4)
## Authors

* **Tuan Nguyen Doan** - *Initial work* - [tuangauss](https://github.com/tuangauss)

This is a self-learning project and I hope to learn from the expertise of the community. Please reach out to me if you have any suggestion or ideas.


## Acknowledgments
This is a self-learning project and I am proud to present the following sources as my reference (and inspiration):
* Microsoft Cognitive Service
* CS50 resources: for HTML template, advise and suggestion
* Dropbox API
* Webcam.js



