# yeet hay（熱氣）

This device allows horses to decide when they want to receive food, allocating a portion of a horse's daily feed when it taps a sensor.

![](readme.png)

## Inspiration
If you have a lot of horses to feed, and each needs a certain nutritional profile, it takes a long time. When humans are controlling the feeding process, it also forces the horses to eat at given times. According the the helpful folks of [Platinum Performance](https://www.platinumperformance.com/horses), it is better for them to eat when they are hungry, as they are smart enough to know when the ideal time to eat was. 

We automated the process by giving each horse a coded profile, such that when a horse walks up to a sensor on the feeding box, the feeding box will automatically mix in the necessary nutrients. It will track how much nutrition supplements that are being put into the horse's feed, so that it does not overdose on certain medicines. 

## Specifications
### Hardware

*Key Functionality - Arudino + Servo Motor + Cardboard + Box Cutter*

We used an Arudino to rotate the servo motor, that was attached to a platform that allowed food to fall through. Ideally, in a production level model, the food would fall into the cup sitting under into it, and there would be no gaps such that once rotating away from a cup (which would be a tube of feed/nutrition), no food would fall through into the cup following that. 

[![Video Demo](https://img.youtube.com/vi/ZS6azAeMG58/maxresdefault.jpg)](https://youtu.be/ZS6azAeMG58)

### Software

**Front End**: *Key Functionality - HTML/CSS, iOS Native, Google Vision API*

In terms of frontend, we created a website using vanilla HTML/CSS, that connected to our backend to store data about horses. 

We also created an iOS application that used the [Google Cloud Vision OCR API](https://cloud.google.com/vision/) (Optical Character Recognition)to read text from a horse's tag. To ensure that a horse was close enough for it to intend to want feed, there would be no other text detected in the background, as it would mean the horse was right in front of the sensor, which would be attached to the side of the feeder at a reasonable height. When the right code was scanned, the iOS application interacted with the Flask server for the processing functionality. 

**Back End**: *Key Functionality - Google Firebase Datastore, Flask*

In terms of backend, we used the [Google Firebase Datastore](https://firebase.google.com/docs/database/) to store the coded information in our database. 

*Firebase Datastore - Sample Horse Schema*

    horse_name: {
	    "vitamin_2"         : {
	    	"max": 2,
	    	"taken": 0
	    },
	    ...
	   	 "vitamin_10"         : {
	    	"max": 3,
	    	"taken": 0
	    }
    }
    
The Firebase Datastore API interfaced with our Flask server, such that data would be written and read through it. 

**Major Routes**

1. GET /horse - Gets all information about horse and executes action on the Arudino

	*Parameters: @horse - horse code to retrieve information*

2. GET /check_vitamin_dose - Check if a horse needs more vitamins for the day

	*Parameters: @horse_code - horse code to retrieve information, @vitamin_name - vitamin to check if max consumption has been reached*
	
**Dependencies**

1. flask - Flask, request, render_template
2. requests
3. firebase_admin - credentials, db
4. google.cloud - firestore
5. gcloud - pubsub
