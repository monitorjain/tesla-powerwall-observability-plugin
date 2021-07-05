# tesla-powerwall-observability-plugin
This is a fun observability project themed Dynatrace plugin for Tesla product owners

Think this is difficult, think again. Its super straightforward to observe and manage your Tesla Powerwall with this Python service

Outcomes:

![smart electricity Dashboard](https://user-images.githubusercontent.com/45892212/124455528-095c2500-ddcd-11eb-95e1-fc64c8f884bc.png)

Solution Architecture:

![Tesla Powerwall smart storm watcher architecture](https://user-images.githubusercontent.com/45892212/124455542-0d884280-ddcd-11eb-9492-09ee11dd5676.png)

Pre-requisites:
1. Dynatrace Platform or another Observability Platform access & metrics API Token access
2. OpenWeatherAPIs or other similar weather API service
3. Tesla Product Auth app on iOs or Android for Token generation
4. Tesla Products - Powerwall or Car (any model works)

How to execute this plugin:
1. If you don't have Dynatrace access, simply create a trial account at https://www.dynatrace.com/trial/
2. Once you've adjusted the code as per inline comments and recommendations, simply run the code with this command: **python3 main.py**

Raise an issue if you need help with your own metrics based extension or service, happy to guide you or support you as best as I can. 

Hit the star button, if you like this solution. 
