from sys import displayhook
from typing import Any, Text, Dict, List
from pyparsing import nestedExpr

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

from . import spotify
from . import wiki

class ActionArtist(Action):

    def name(self) -> Text:
        return "action_get_similar_artist"

    def run(self, dispatcher, tracker, domain):
        #search ist die Variable "search", die vom Bot übergeben wird; sie repräsentiert das, was der user suchen will
        search = tracker.latest_message["text"]
        start = str(search).find('"')
        end = str(search).find('"', start+1)
        search = str(search)[start:end].strip('"')

        print(search)

        if str(search).strip('"').strip() == None:
            #Antwort, wenn nichts eingegeben wurde
            dispatcher.utter_message("Du hast doch noch garnichts eingegeben") #Fehlermeldung, wenn nichts eingegeben wurde
        else:
            result1, result2, result3, result4, result5, result6 = spotify.getRelatedArtist(search)

            if "error" in result1:
                #Fehlermeldung, wenn Artist nicht existiert
                dispatcher.utter_message("Wow! Nicht einmal ich kenne den Artist :o Versuche bitte einen anderen Namen.")
            elif "No similar" in result1:
                #Fehlermeldung, wenn es nichts Ähnliches zur Suche gibt
                dispatcher.utter_message("Ich kenne leider nichts ähnliches dazu") 
            else:
                #--------------------------------------------
                #Antwort bei erfolgreicher Anfrage
                answer = f"Ich hätte das hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}"
                if result2 != "":
                    answer = f"Ich hätte die hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}\n{result2[0]} {result2[2]} {result2[1]}"
                if result3 != "":
                    answer = f"Ich hätte die hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}\n{result2[0]} {result2[2]} {result2[1]}\n{result3[0]} {result3[2]} {result3[1]}"
                if result4 != "":
                    answer = f"Ich hätte die hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}\n{result2[0]} {result2[2]} {result2[1]}\n{result3[0]} {result3[2]} {result3[1]}\n{result4[0]} {result4[2]} {result4[1]}"
                if result5 != "":
                    answer = f"Ich hätte die hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}\n{result2[0]} {result2[2]} {result2[1]}\n{result3[0]} {result3[2]} {result3[1]}\n{result4[0]} {result4[2]} {result4[1]}\n{result5[0]} {result5[2]} {result5[1]}"
                if result6 != "":
                    answer = f"Ich hätte die hier für dich gefunden:\n{result1[0]} {result1[2]} {result1[1]}\n{result2[0]} {result2[2]} {result2[1]}\n{result3[0]} {result3[2]} {result3[1]}\n{result4[0]} {result4[2]} {result4[1]}\n{result5[0]} {result5[2]} {result5[1]}\n{result6[0]} {result6[2]} {result6[1]}"
                #--------------------------------------------
                #Ausgabe der Antwort, wenn die Anfrage erfolgreich war
                dispatcher.utter_message(answer)

        return []

class ActionTrack(Action):

    def name(self) -> Text:
        return "action_get_similar_track"

    def run(self, dispatcher, tracker, domain):
        #search ist die Variable "search", die vom Bot übergeben wird; sie repräsentiert das, was der user suchen will
        search = tracker.latest_message["text"]
        start = str(search).find('"')
        end = str(search).find('"', start+1)
        search = str(search)[start:end].strip('"')

        print(search)

        if str(search).strip('"').strip() == None:
            #Antwort, wenn nichts eingegeben wurde
            dispatcher.utter_message("Du hast doch noch garnichts eingegeben")
        else:
            #Ausgabe der Antwort, wenn die Anfrage erfolgreich war
            dispatcher.utter_message("Hier gibt es noch nichts zu sehen.\n\n\nIst halt nur ein Prototyp. In der Vollversion wäre das hier auch verfügbar.")

        return []

class ActionInfo(Action):

    def name(self) -> Text:
        return "action_get_info"

    def run(self, dispatcher, tracker, domain):
        #search ist die Variable "search", die vom Bot übergeben wird; sie repräsentiert das, was der user suchen will
        search = tracker.latest_message["text"]
        start = str(search).find('"')
        end = str(search).find('"', start+1)
        search = str(search)[start:end].strip('"')

        print(search)

        if str(search).strip('"').strip() == None:
            #Antwort, wenn nichts eingegeben wurde
            dispatcher.utter_message("Du hast doch noch garnichts eingegeben")
        else:
            result = wiki.getInfo(search)
            if "error" in result:
                dispatcher.utter_message("Soweit reicht mein Wissensstand leider auch nicht.")
            else:
                #Ausgabe der Antwort, wenn die Anfrage erfolgreich war
                dispatcher.utter_message(result)

        return []