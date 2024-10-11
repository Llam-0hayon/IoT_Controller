import paho.mqtt.client as mqtt

class IoT_Controller:
    client = None
    #TODO: support for collections of conditions leading to single outputs
    rules = [
        	{
                	"condition" {"topic": "house/temp", "comparison":">", "value": 30}:, #anything inside "" is a key or value (key is before the : )
                	"action":{"message":"its too hot, turn on ac", "topic":"room/AC", "value":"on"}
        	},
        	{
                	"condition" {"topic": "house/temp", "comparison":"<", "value": 20}:, #anything inside "" is a key or value (key is before the : )
                	"action":{"message":"its too cold, turn on heat", "topic":"room/AC", "value":"on"} #key is like a variable and value is a value
        	}

	]
    def configure():
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
        print(topic, value) # based on the value(s) on the topic(s) received trigger an action

#                {
 #                       "condition" {"topic": "house/temp", "comparison":">", "value": 30}:, #anything inside "" is a key or value (key is before the : )
  #                      "action":{"message":"its too hot, turn on ac", "topic":"room/AC", "value":"on"}
   #             }

        #loop throught the rules
        for rule in IoT_controller.rules:
             condition = rule["condition"]
             if topic == rule ["condition"]["action"]and condition_met(value,condition["comparison"],condition["value"]):
            	#action
                action = rule["action"]
            	print(action["message"])
            	IoT_Controller.client.publish(action["topic"],action["value"])

    def condition_met(value,comp_operator,comp_value):
        if comp_operator == ">":
            return > comp_value
        if comp_operator == ">=":
            return >= comp_value
        if comp_operator == "<=":
            return <= comp_value
        if comp_operator == "<":
            return < comp_value
        if comp_operator == "==":
            return == comp_value


    def run():
        IoT_Controller.client.loop_forever() #equivalent of calling loop function in arduino

def main():
    IoT_Controller.configure()
    IoT_Controller.run()

if __name__ == "__main__":
    main()
