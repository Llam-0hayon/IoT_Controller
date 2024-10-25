import paho.mqtt.client as mqtt
import json
import time

class IoT_Controller:
    client = None
    #TODO: support for collections of conditions leading to single outputs
    #JSON: JavaScipt Object Notation is the format used for the rules below
    # [] lists of items go between []
    # {} losts  of key-values pairs go between {} (dictionnaries)
    rules = []
    # to rememebr the message we sent out
    message_log = []

    mqtt_data = {} # where received data  is logged

    def configure():
        filename = "rules.json"
        with open(filename,'r') as file:
            IoT_Controller.rules = json.load(file)

        IoT_Controller.client = mqtt.Client()
        #pass the reference to the callback function to handle incoming messages
        IoT_Controller.client.on_message = IoT_Controller.on_message
        #must connect to the MQTT message broker at "localhost" on port 1883
        IoT_Controller.client.connect("localhost",1883) #to connect to mqtt broker
        #IoT_Controller.client.subscribe("*") # * means all topics
        #IoT_Controller.client.subscribe("+") # + is a wild card for a Single level will sub to one and only one
        IoT_Controller.client.subscribe("#") # # is a wild card for a Multi level will sub to multiple

    def on_message(client, userdata, message):
        #this is where we handle the messages
        try:
            value = float(message.payload.decode("utf-8"))
        except ValueError:
            print("String")
            value = message.payload.decode("utf-8")
        topic = message.topic #the only action is the printout
        IoT_Controller.mqtt_data[topic] = value #write most recent value of dta to topic -->  records the received data in our dictiary tplacing any older value fro the same topic 
	#        IoT_Controller.mqtt_data[topic] = value
        # if IoT_Controller.message_log contains an entry
        for entry in IoT_Controller.message_log:
           if entry["time"] < time.time() - 5:
            #delete old entries
            IoT_Controller.message_log.remove(entry) 
           elif entry["topic"] == topic and entry["value"] == value:
                return #stops sending message
            
        print(topic, value) # based on the value(s) on the topic(s) received trigger an action

#                {
 #                       "condition" {"topic": "house/temp", "comparison":">", "value": 30}:, #anything inside "" is a key or value (key is before the : )
  #                      "action":{"message":"its too hot, turn on ac", "topic":"room/AC", "value":"on"}
   #             }

        #loop throught the rules
        #THis is where we evaluate if value metts parameters
        for rule in IoT_Controller.rules:
             conditions = rule["conditions"] #changed from condition: condition = rule["condition"]
             conditions_met = True

             for condition in conditions:
              topic = condition["topic"]

              try:
                  value = IoT_Controller.mqtt_data[topic] #extrct va;ues ffrom shhet of paper
                  condition_met = IoT_Controller.condition_met(value,condition["comparison"],condition["value"]) #if something on sheet of papaer compare then true f conditionis met

              except KeyError:
                  value = None
                  condition_met = False
              conditions_met = condition_met and conditions_met

              #action
             if conditions_met:
              #use the topic from the sondition to access the value in the mqtt_data dictionary
                action = rule["action"]
                print(action["message"])
                IoT_Controller.client.publish(action["topic"],action["value"])
                # Record that the message has been sent
                entry = {"time":time.time(),"topic":action["topic"], "value":action["value"]}
                IoT_Controller.message_log.append(entry)#add message to the end of the list

    def condition_met(value,comp_operator,comp_value):
        if comp_operator == ">":
            return value  > comp_value
        if comp_operator == ">=":
            return value  >= comp_value
        if comp_operator == "<=":
            return value <= comp_value
        if comp_operator == "<":
            return value < comp_value
        if comp_operator == "==":
            return value  == comp_value


    def run():
        IoT_Controller.client.loop_forever() #equivalent of calling loop function in arduino

def main():
    IoT_Controller.configure()
    IoT_Controller.run()

if __name__ == "__main__":
    main()






